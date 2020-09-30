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



class Product(UserMixin,db.Model):

    'Product model schema'

    __tablename__ = 'products'

    id = db.Column(db.Integer,primary_key = True)
    product_name = db.Column(db.String(255),unique = True,index = True)
    product_stock = db.Column(db.Integer)
    product_spoilt = db.Column(db.Integer,default = 0)
    product_buying_price = db.Column(db.Integer)
    product_selling_price = db.Column(db.Integer)

    def __repr__(self):
        return f'Product {self.product_name}'