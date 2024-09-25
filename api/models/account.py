from db import db

class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    balance = db.Column(db.Float(precision=2), unique=False, default=0.00)
    created = db.Column(db.DateTime(), unique=False, nullable=False)
    last_login = db.Column(db.DateTime(), unique=False, nullable=True)
    intro_done = db.Column(db.Boolean(), unique=False, default=False)