from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):

    'User model schema'

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    profile_pic_path = db.Column(db.String())
    role = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    ordersreceived = db.relationship('OrderReceived',backref = 'user',lazy = "dynamic")
    sales = db.relationship('Sale',backref = 'user',lazy = "dynamic")
    
    
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'



class Product(db.Model):

    'Product model schema'

    __tablename__ = 'products'

    id = db.Column(db.Integer,primary_key = True)
    product_name = db.Column(db.String(255),unique = True,index = True)
    product_stock = db.Column(db.Integer)
    product_spoilt = db.Column(db.Integer,default = 0)
    product_buying_price = db.Column(db.Integer)
    product_selling_price = db.Column(db.Integer)


    def save_product(self):
        db.session.add(self)
        db.session.commit()
    def __repr__(self):
        return f'Product {self.product_name}'


class OrderReceived(db.Model):

    'OrderReceived model schema'

    __tablename__ = 'ordersreceived'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    product_name = db.Column(db.String(255))
    order_quantity = db.Column(db.Integer)
    order_payment = db.Column(db.String(255))
    order_total_amount = db.Column(db.Integer)
    order_time = db.Column(db.DateTime,default=datetime.utcnow)


    def save_order(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'OrderReceived {self.id}'  


class Sale(db.Model):

    'Sale model schema'

    __tablename__ = 'sales'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    product_name = db.Column(db.String(255))
    sale_quantity = db.Column(db.Integer)
    sale_amount=db.Column(db.Integer)
    sale_time = db.Column(db.DateTime,default=datetime.utcnow)


    def save_sale(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Sale of {self.product_name}'                