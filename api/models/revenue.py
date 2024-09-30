import enum
from datetime import datetime

from db import db

class revenue_enum(str, enum.Enum):
    income = "income"
    expenditure = "expenditure"

class RevenueModel(db.Model):
    __tablename__ = "revenues"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    type = db.Column(db.Enum(revenue_enum), unique=False, nullable=False)
    amount = db.Column(db.Float(precision=2), unique=False, default=0.00)
    created = db.Column(db.DateTime(), unique=False, default=datetime.now())
    account_id = db.Column(db.Integer(), 
                           db.ForeignKey("accounts.id"),
                           unique=False,
                           nullable=False)
    category_id = db.Column(db.Integer(),
                            db.ForeignKey("categories.id"),
                            unique=False,
                            nullable=True)
    recurrent_id = db.Column(db.Integer(),
                             db.ForeignKey("recurrents.id"),
                             unique=False,
                             nullable=True)
    account = db.relationship("AccountModel", back_populates="revenues")
    category = db.relationship("CategoryModel", back_populates="revenues")
    recurrent = db.relationship("RecurrentModel", back_populates="revenues")
