from db import db

class CategoryModel(db.Model):
    __tablename__ = "Catorgories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    budget = db.Column(db.Float(precision=2), unique=False, nullable=True)
    created = db.Column(db.DateTime(), unique=False, nullable=False)
    account_id = db.Column(db.Integer(), unique=False, foreign_key=True)