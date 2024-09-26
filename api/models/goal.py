from datetime import datetime

from db import db

class GoalModel(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    balance = db.Column(db.Float(precision=2), unique=False, default=0.00)
    goal_target = db.Column(db.Float(precision=2), unique=False, default=0.00)
    end_date = db.Column(db.Date(), unique=False, nullable=True)
    created = db.Column(db.Date(), unique=False, default=datetime.now())
    account_id = db.Column(db.Integer,
                           db.ForeignKey("accounts.id"),
                           unique=False,
                           foreign_key=True)
    account = db.relationship("AccountModel", back_populates="goals")