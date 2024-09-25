from datetime import datetime

from db import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    budget = db.Column(db.Float(precision=2), unique=False, nullable=True)
    created = db.Column(db.DateTime(), unique=False, default=datetime.now())
    account_id = db.Column(db.Integer(), db.ForeignKey("accounts.id"), unique=False, nullable=False)
    account = db.relationship("AccountModel", back_populates="categories")
    recurrents = db.relationship("RecurrentModel", back_populates="category", lazy="dynamic")
    revenues = db.relationship("RevenueModel", back_populates="category", lazy="dynamic")