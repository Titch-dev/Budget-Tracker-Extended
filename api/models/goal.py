from datetime import datetime

from db import db

class GoalModel(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    balance = db.Column(db.Float(precision=2), default=0.00)
    goal_target = db.Column(db.Float(precision=2), default=0.00)
    end_date = db.Column(db.Date(), nullable=True)
    created = db.Column(db.Date(), default=datetime.now())
    account_id = db.Column(db.Integer,
                           db.ForeignKey("accounts.id"),
                           unique=False)
    account = db.relationship("AccountModel", back_populates="goals")
    recurrents = db.relationship("RecurrentModel", back_populates="goal")
    