# -*- coding: utf-8 -*-

from flask_mongoalchemy import MongoAlchemy
import werkzeug.security

from main import app
db = MongoAlchemy(app)


#
# Database Models
#

class Phone(db.Document):
    countrycode = db.IntField()
    areacode    = db.IntField()
    number      = db.IntField()
    iswhatsapp  = db.BoolField()
    smscode     = db.IntField()
    isvalidated = db.BoolField()


class Merchant(db.Document):
    name = db.StringField()
    email = db.StringField()
    password = db.StringField()
    phone = db.DocumentField(Phone)
    active = db.BoolField()


class Category(db.Document):
    name = db.StringField()
    description = db.StringField()
    active = db.BoolField()


class Business(db.Document):
    owner = db.StringField()
    phone = db.DocumentField(Phone)
    category = db.DocumentField(Category)
    name = db.StringField()
    description = db.StringField()
    email = db.StringField()
    url_self = db.StringField()
    url_instagram = db.StringField()
    url_facebook = db.StringField()
    address = db.StringField()
    location = db.DictField(db.AnythingField())
    active = db.BoolField()


# uncomment to recreate data

# phone1 = Phone(countrycode=55, areacode=11, number=999999999, iswhatsapp=True, smscode=1234, isvalidated=True)
# phone2 = Phone(countrycode=55, areacode=11, number=888888888, iswhatsapp=False, smscode=1234, isvalidated=True)
# phone3 = Phone(countrycode=55, areacode=11, number=777777777, iswhatsapp=True, smscode=1234, isvalidated=False)
# phone4 = Phone(countrycode=55, areacode=11, number=666666666, iswhatsapp=True, smscode=1234, isvalidated=False)
# phone5 = Phone(countrycode=55, areacode=11, number=555555555, iswhatsapp=True, smscode=1234, isvalidated=False)
# phone6 = Phone(countrycode=55, areacode=11, number=444444444, iswhatsapp=True, smscode=1234, isvalidated=False)
#
# cat1 = Category(name='diversos', description='', active=True)
# cat1.save()
# cat2 = Category(name='alimentacao', description='delivery, salgadinhos, bolos, etc', active=True)
# cat2.save()
# cat3 = Category(name='idiomas', description='aulas de idiomas', active=True)
# cat3.save()
#
# merch1 = Merchant(name='Aessede', email='asd@gmail.com', password='8472d01a0bf5e4a5246fb982e974fe1aa8713948', phone=phone4, active=True)
# merch1.save()
# merch2 = Merchant(name='De Efege', email='dfg@gmail.com', password='8472d01a0bf5e4a5246fb982e974fe1aa8713948', phone=phone5, active=True)
# merch2.save()
# merch3 = Merchant(name='Query Silva', email='qwe@gmail.com', password='8472d01a0bf5e4a5246fb982e974fe1aa8713948', phone=phone6, active=True)
# merch2.save()
#
# business1 = Business(owner='asd@gmail.com', name='lojinha de variadades do Joao', email='email@dalojinha', description='tem de tudo nessa lojinha', phone=phone1, category=cat1, url_self='http://minhaurlcustomizada.com', url_instagram='http://instagram.com/sdfg', url_facebook="http://facebug.com/gserg", address='Rua das bananas 123', location={ 'type':'Point', 'coordinates':[-23.567439, -46.639446]}, active=True)
# business1.save()
# business2 = Business(owner='dfg@gmail.com', name ='cafe da Mila', email='emaild@docafe', description='cafezinho bao', phone=phone2, category=cat2, url_self='http://minhaurlcustomizada.com', url_instagram='http://instagram.com/sdfg', url_facebook="http://facebug.com/gserg", address='Rua das bananas 123', location={ 'type':'Point', 'coordinates':[-23.547439, -46.639446]}, active=True)
# business2.save()
# business3 = Business(owner='qwe@gmail.com', name='frances do joao', email='email@beto.com', description='le figaro', phone=phone3, category=cat3, url_self='http://minhaurlcustomizada.com', url_instagram='http://instagram.com/sdfg', url_facebook="http://facebug.com/gserg", address='Rua das bananas 123', location={ 'type':'Point', 'coordinates':[-23.527439, -46.639446]}, active=True)
# business3.save()

# asd = Merchant.query.filter(Merchant.name == 'Aessede').first()
# print(asd.phone.number)


def password_encode(password):
    h, method = werkzeug.security._hash_internal('sha1', app.config['SECRET_KEY'], password)
    return h

# Merchant Methods

def merchant_new(merchant):
    phone_new = Phone(countrycode=merchant['phone']['countrycode'], areacode=merchant['phone']['areacode'], number=merchant['phone']['number'], iswhatsapp=merchant['phone']['iswhatsapp'], smscode=merchant['phone']['smscode'], isvalidated=False)
    phone_new.save()
    merchant = Merchant(name=merchant['name'], email=merchant['email'], password=password_encode(merchant['password']), phone=phone_new, active=True)
    merchant.save()
    return True

def merchant_get_all():
    merchants = Merchant.query.all()
    if merchants:
        return merchants
    return False

def merchant_get_by_name(name):
    merchant = Merchant.query.filter(Merchant.name == name).first()
    if merchant:
        return merchant
    return False

def merchant_get_by_email(email):
    merchant = Merchant.query.filter(Merchant.email == email).first()
    print('yay')
    if merchant:
        print('found merchant: '+merchant.email)
        return merchant
    return False

def merchant_get_by_id(mongo_id):
    merchant = Merchant.query.filter(Merchant.mongo_id == mongo_id).first()
    if merchant:
        return merchant
    return False

def merchant_update(mongo_id, upd_merchant):
    # merchant = None
    # try:
        merchant = merchant_get_by_id(mongo_id)
        merchant.name = upd_merchant['name']
        merchant.email = upd_merchant['email']
        merchant.password = password_encode(upd_merchant['password'])
        merchant.phone.iswhatsapp = upd_merchant['phone']['iswhatsapp']
        merchant.phone.isvalidated = upd_merchant['phone']['isvalidated']
        merchant.phone.countrycode = upd_merchant['phone']['countrycode']
        merchant.phone.areacode = upd_merchant['phone']['areacode']
        merchant.phone.number = upd_merchant['phone']['number']
        #merchant.phone.smscode = upd_merchant['phone']['smscode']
        #safe nested_dict.get('dictA', {}).get('key_1')
        merchant.active = upd_merchant['active']
        merchant.save()
    # except:
    #     return False
    # return True

def merchant_delete(mongo_id):
    merchant = merchant_get_by_id(mongo_id)
    merchant.remove()

def merchant_check_pass(auth):
    try:
        merchant = merchant_get_by_email(auth['email'])
    except:
        return False
    if merchant:
        if merchant.password == password_encode(auth['password']):
            return merchant
        else:
            return False
    return False


# Business Methods

def business_new(business):
    phone_new = Phone(countrycode=business['phone']['countrycode'], areacode=business['phone']['areacode'], number=business['phone']['number'], iswhatsapp=business['phone']['iswhatsapp'], smscode=business['phone']['smscode'], isvalidated=False)
    category = Category.query.filter(Category.name == business['category']).first()
    business = Business(name=business['name'], owner=business['owner'], phone=phone_new, category=category, description=business['description'], email=business['email'], url_self=business['url_self'], url_instagram=business['url_instagram'], url_facebook=business['url_facebook'], address=business['address'], location=business['location'], active=True)
    business.save()
    return True

def business_get_all():
    businesses = Business.query.all()
    return businesses

def business_get_by_name(name):
    business = Business.query.filter(Business.name == name).first()
    return business

def business_get_by_id(mongo_id):
    business = Business.query.filter(Business.mongo_id == mongo_id).first()
    return business

def business_update(mongo_id, upd_business):
    business = business_get_by_id(mongo_id)
    business.owner = upd_business['owner']
    business.name = upd_business['name']
    business.email = upd_business['email']
    business.category.name = upd_business['category']['name']
    business.category.description = upd_business['category']['description']
    business.category.active = upd_business['category']['active']
    business.phone.iswhatsapp = upd_business['phone']['iswhatsapp']
    business.phone.isvalidated = upd_business['phone']['isvalidated']
    business.phone.countrycode = upd_business['phone']['countrycode']
    business.phone.areacode = upd_business['phone']['areacode']
    business.phone.number = upd_business['phone']['number']
    #business.phone.smscode = upd_business['phone']['smscode']
    business.description = upd_business['description']
    business.url_self = upd_business['url_self']
    business.url_instagram = upd_business['url_instagram']
    business.url_facebook = upd_business['url_facebook']
    business.address = upd_business['address']
    business.location = upd_business['location']
    business.active = upd_business['active']
    business.save()

def business_delete(mongo_id):
    business = business_get_by_id(mongo_id)
    business.remove()


def user_check_pass(email, password):
    user = Merchant.query.filter(Merchant.email == email).first()
    h, method = werkzeug.security._hash_internal('sha1', app.config['SECRET_KEY'], password)
    if user.password == h:
        return True
    else:
        return False


