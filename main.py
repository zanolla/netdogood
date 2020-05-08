# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import request, make_response, Blueprint
from flask_restplus import Resource, Api, fields
from functools import wraps
from datetime import datetime, timedelta
import jwt

import config
from database import *


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=365)
app.config['SECRET_KEY'] = config.appconfig.SECRET_KEY
app.config['MONGOALCHEMY_DATABASE'] = config.appconfig.DATABASE_NAME
app.config['MONGOALCHEMY_SERVER'] = config.appconfig.DATABASE_HOST
app.config['MONGOALCHEMY_PORT'] = config.appconfig.DATABASE_PORT

api = Api(app)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
app.register_blueprint(blueprint)


# Handlers

@app.errorhandler(404)
def not_found(error):
    app.logger.info(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


#
#  API - Models
#

location = api.model('Location', {
    'type': fields.String(description='Location type', default='Point'),
    'coordinates': fields.List(fields.Float)
})

category = api.model('Category', {
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(required=True, description='Category description'),
    'active': fields.Boolean,
})

phonerecord = api.model('Phone', {
    'countrycode': fields.Integer(required=True, description='Country code'),
    'areacode': fields.Integer(required=True, description='Area code'),
    'number': fields.Integer(required=True, description='Phone number'),
    'iswhatsapp': fields.Boolean(required=False, description='Is a whatsapp number'),
    'smscode': fields.Integer(required=True, description='SMS validation code'),
    'isvalidated': fields.Boolean(required=False, description='Number is validated'),
})

merchant = api.model('Merchant', {
    'mongo_id': fields.String(required=False, description='ID'),
    'name': fields.String(description='Merchant name'),
    'email': fields.String(required=True, description='Merchant email'),
    'password': fields.String(required=True, description='Merchant password'),
    'phone': fields.Nested(phonerecord),
    'active': fields.Boolean,
})

business = api.model('Business', {
    'mongo_id': fields.String(required=False, description='ID'),
    'owner': fields.String(description='Owners email (merchants email)'),
    'phone': fields.Nested(phonerecord),
    'category': fields.Nested(category),
    'name': fields.String(description='Business Fantasy name'),
    'description': fields.String(description='Business description'),
    'email': fields.String(description='Business email (may be different than merchants email)'),
    'url_self': fields.String(description='BackRef URL'),
    'url_instagram': fields.String(description='Instagram URL'),
    'url_facebook': fields.String(description='Facebook URL'),
    'address': fields.String(description='Freeform Address'),
    'location': fields.Nested(location),
    'active': fields.Boolean,
})


auth = api.model('Auth', {
    'email': fields.String(required=True, description='Merchant email'),
    'password': fields.String(required=True, description='Merchant password')
})


#
# API - decorator to require jwt token
#       use in protected routes or pay the price

def user_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            print('passou o token...')
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print('token data: '+data['email'])
            current_user = merchant_get_by_email(data['email'])
            print('->current_user = '+current_user.email)
        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator


#
# API = /authorization Namespace
#

ns_auth = api.namespace('authorization', description='Operations related to Authorization')
api.add_namespace(ns_auth)


@ns_auth.route('/login')
class AuthItem(Resource):

    @api.expect(auth)
    def post(self):
        """Gets a new JWT Token."""
        merchant = merchant_check_pass(request.json)
        if merchant:
            token = jwt.encode({'email': merchant.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'x-access-token': token.decode('UTF-8')})
        return None, 401


#
#  API - /merchant Namespace
#

ns_merchant = api.namespace('merchants', description='Operations related to Merchants')
api.add_namespace(ns_merchant)


@ns_merchant.route('/')
class MerchantsCollection(Resource):

    @api.marshal_with(merchant)
    def get(self):
        """Returns list of merchants."""
        return merchant_get_all()

    @api.response(201, 'Merchant created.')
    @api.expect(merchant)
    @api.marshal_with(merchant)
    def post(self):
        """Creates a new merchant."""
        merchant_new(request.json)
        return None, 201


@ns_merchant.route('/<string:id>')
@ns_merchant.response(404, 'Merchant not found.')
class MerchantItem(Resource):

    @api.marshal_with(merchant)

    def get(self, id):
        """Returns details of a merchant."""
        return merchant_get_by_id(id)

    @api.response(204, 'Merchant successfully updated.')
    @api.expect(merchant)
    @api.header('x-access-tokens', 'Token received upon authentication', required=True)
    @user_token_required
    def put(self, id):
        """Updates details of a merchant."""
        merchant_update(id, request.json)
        return None, 204

    @api.response(204, 'Merchant successfully deleted.')
    @api.header('x-access-tokens', 'Token received upon authentication', required=True)
    @user_token_required
    def delete(self, id):
        """Deletes merchant."""
        merchant_delete(id)
        return None, 204


#
#  API - /business Namespace
#

ns_business = api.namespace('businesses', description='Operations related to Businesses')
api.add_namespace(ns_business)


@ns_business.route('/')
class BusinessesCollection(Resource):

    @api.marshal_with(business)
    def get(self):
        """Returns list of businesses."""
        return business_get_all()

    @api.response(201, 'Business created.')
    @api.expect(business)
    @api.marshal_with(business)
    def post(self):
        """Creates a new business."""
        business_new(request.json)
        return None, 201


@ns_business.route('/<string:id>')
@ns_business.response(404, 'Business not found.')
class BusinessItem(Resource):

    @api.marshal_with(business)
    def get(self, id):
        """Returns details of a business."""
        return business_get_by_id(id)

    @api.response(204, 'Business successfully updated.')
    @api.expect(business)
    @api.header('x-access-tokens', 'Token received upon authentication', required=True)
    @user_token_required
    def put(self, id):
        """Updates details of a business."""
        business_update(id, request.json)
        return None, 204

    @api.response(204, 'Business successfully deleted.')
    @api.header('x-access-tokens', 'Token received upon authentication', required=True)
    @user_token_required
    def delete(self, id):
        """Deletes business."""
        business_delete(id)
        return None, 204


if __name__ == "__main__":
   app.run(debug=True, threaded=True, host='0.0.0.0', port='8888')


