import enum
from datetime import datetime

from db import db

class revenue_enum(str, enum.Enum):
    income = "income"
    expenditure = "expenditure"

class frequency_enum(str, enum.Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annually = "annually"

class RecurrentModel(db.Model):
    __tablename__ = "recurrents"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    frequency = db.Column(db.Enum(frequency_enum), unique=False, nullable=False)
    type = db.Column(db.Enum(revenue_enum), unique=False, nullable=False)
    amount = db.Column(db.Float(precision=2), unique=False, default=0.00)
    effect_date = db.Column(db.Date(), unique=False, nullable=False)
    created = db.Column(db.DateTime(), unique=False, default=datetime.now())
    account_id = db.Column(db.Integer(),
                           db.ForeignKey("accounts.id"),
                           unique=False,
                           nullable=False)
    category_id = db.Column(db.Integer(),
                            db.ForeignKey("categories.id"),
                            unique=False,
                            nullable=True)
    goal_id = db.Column(db.Integer(),
                        db.ForeignKey("goals.id"),
                        unique=False,
                        nullable=True)
    account = db.relationship("AccountModel", back_populates="recurrents")
    category = db.relationship("CategoryModel", back_populates="recurrents")
    goal = db.relationship("GoalModel", back_populates="recurrents")
    revenues = db.relationship("RevenueModel", 
                               back_populates="recurrent", 
                               lazy="dynamic")