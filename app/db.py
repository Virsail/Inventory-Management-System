from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
db = SQLAlchemy()
Column = db.Column
ForeignKey = db.ForeignKey
String = db.String
Integer = db.Integer
relationship = db.relationship
Model = db.Model
DateTime = db.DateTime
backref = orm.backref
