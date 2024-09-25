import enum
from db import db

class revenue_enum(str, enum.Enum):
    income = "income"
    expenditure = "expenditure"

class RevenueModel(db.Model):
    __tablename__ = "Revenues"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unqiue=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    type = db.Column(db.Enum(revenue_enum), unique=False, nullable=False)
    amount = db.Column(db.Float(precision=2), unique=False, default=0.00)
    created = db.Column(db.DateTime(), unique=False, nullable=False)
    account_id = db.Column(db.Integer(), unique=False, nullable=False)
    category_id = db.Column(db.Integer(), unique=False, nullable=True)
