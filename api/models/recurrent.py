import enum
from db import db

class revenue_enum(str, enum.Enum):
    income = "income"
    expenditure = "expenditure"

class frequency_enum(str, enum.Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annualy = "annually"

class RecurrentModel(db.Model):
    __tablename__ = "recurrents"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    frequency = db.Column(db.Enum(frequency_enum), unique=False, nullable=False)
    type = db.Column(db.Enum(revenue_enum), unique=False, nullable=False)
    amount = db.Column(db.Float(precision=2), unique=False, default=0.00)
    effect_date = db.Column(db.Date(), unique=False, nullable=False)
    created = db.Column(db.DateTime(), unique=False, nullable=False)
    account_id = db.Column(db.Integer(), foreign_key=True, unique=False, nullable=False)
    category_id = db.Column(db.Integer(), foreign_key=True, unique=False, nullable=True)
