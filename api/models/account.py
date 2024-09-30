from datetime import datetime

from db import db

class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float(precision=2), default=0.00)
    created = db.Column(db.DateTime(), default=datetime.now())
    last_login = db.Column(db.DateTime())
    intro_done = db.Column(db.Boolean())
    categories = db.relationship("CategoryModel", 
                                 back_populates="account", 
                                 lazy="dynamic", 
                                 cascade="all, delete")
    goals = db.relationship("GoalModel", 
                            back_populates="account", 
                            lazy="dynamic",
                            cascade="all, delete")
    recurrents = db.relationship("RecurrentModel",
                                 back_populates="account",
                                 lazy="dynamic",
                                 cascade="all, delete")
    revenues = db.relationship("RevenueModel", 
                               back_populates="account", 
                               lazy="dynamic",
                               cascade="all, delete")
