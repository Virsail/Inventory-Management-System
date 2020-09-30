from app.db import (
    Model, 
    String, 
    Integer, 
    ForeignKey,
    Column,
    DateTime,
    relationship,
    backref)
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

class Common(SerializerMixin):
    id = Column(
        Integer,
        primary_key = True
    )
    CREATED_AT = Column(
        DateTime,
        default = datetime.utcnow,
        nullable = False
    )
    UPDATED_AT = Column(
        DateTime,
        nullable=True
    )

class User(Common, Model):
    __tablename__ = 'users'
    name = Column(
        String,
        nullable=False
    )
    email = Column(
        String,
        nullable=False
    )
    role_id = Column(
        Integer,
        ForeignKey('roles.id')
    )
    store_id = Column(
        Integer,
        ForeignKey('stores.id')
    )
    status = Column(
        Integer,
        default=0
    )
    role = relationship('Role', uselist=False)
    store = relationship('Store', backref=backref('employees', uselist=True), uselist=False)


class Store(Common, Model):
    __tablename__='stores'
    name = Column(
        String,
        nullable=False
    )

class Role(Common,Model):
    __tablename__ = 'roles'
    name = Column(
        String,
        nullable=False
    )


class Product(Common, Model):
    __tablename__ = 'products'
    payment_status = Column(
        Integer,
        nullable = False
    )
    no_of_spoiled_items=Column(
        Integer,
        nullable = True
    )
    carriage_inwards = Column(
        Integer,
        default=1
    )
    spoilage = Column(
        Integer,
        default=0
    )
    buying_price = Column(
        Integer,
        nullable = False
    )
    selling_price = Column(
        Integer,
        nullable = False
    )
    supplier_id = Column(
        Integer,
        ForeignKey('suppliers.id')
    )
    category_id = Column(
        Integer,
        ForeignKey('categories.id')
    )
    store_id = Column(
        Integer,
        ForeignKey('stores.id')
    )
    store = relationship('Store',backref='products')
    supplier = relationship('Supplier', backref=backref('products',uselist=True),uselist = False)
    category = relationship('Category', backref=backref('products',uselist=True), uselist = False)

class Category(Common, Model):
    __tablename__ ='categories'
    name = Column(
        String,
        nullable=False
    )

class SupplyRequest(Common,Model):
    __tablename__ = 'supply_requests'
    product_id = Column(
        Integer,
        ForeignKey('products.id')
    )
    supplier_id = Column(
        Integer,
        ForeignKey('suppliers.id')
    )
    no_of_requested_items = Column(
        Integer,
        nullable=False
        
    )
    store_id = Column(
        Integer,
        ForeignKey('stores.id')
    )
    store = relationship('Store', backref=backref('supply_requests',uselist=True), uselist=False)
    supplier = relationship('Supplier', backref=backref('supply_requests',uselist=True),uselist = False)
    product = relationship('Product',uselist=False)

class Sale(Common, Model):
    __tablename__ = 'sales'
    product_id = Column(
        Integer,
        ForeignKey('products.id'),
        nullable = False
    )
    total_sales = Column(
        Integer,
        nullable=False
    )
    store_id = Column(
        Integer,
        ForeignKey('stores.id')
    )
    store = relationship('Store',backref=backref('sales',uselist=True),uselist=False)


class Supplier(Common,Model):
    __tablename__='suppliers'
    name = Column(
        String
    )
    email = Column(
        String
    )

    