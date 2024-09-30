from datetime import date, timedelta

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RecurrentModel, AccountModel, RevenueModel
from schemas import RecurrentSchema, RecurrentUpdateSchema

blp = Blueprint("recurrents", __name__, description="Operations on Recurrence")

@blp.route("/recurrent/<int:rec_id>")
class Recurrent(MethodView):
    @jwt_required()
    @blp.response(200, RecurrentSchema)
    def get(self, rec_id):
        acc_id = get_jwt_identity()
        recurrence = RecurrentModel.query.get_or_404(rec_id)
        if not recurrence.account_id == acc_id:
            abort(409, message="Recurrence does not belong to account")
        return recurrence
    
    @jwt_required()
    @blp.arguments(RecurrentUpdateSchema)
    @blp.response(200, RecurrentSchema)
    def put(self, rec_data, rec_id):
        acc_id = get_jwt_identity()
        recurrence = RecurrentModel.query.get(rec_id)

        if not recurrence.account_id == acc_id:
            abort(409, message="Recurrence does not belong to account")

        if recurrence:
            # Update only the fields the client has posted
            for key in rec_data.keys():
                if hasattr(recurrence, key):
                    setattr(recurrence, key, rec_data[key])

        db.session.add(recurrence)
        db.session.commit()

        return recurrence
    
    @jwt_required()
    def delete(self, rec_id):
        acc_id = get_jwt_identity()
        recurrence = RecurrentModel.query.get_or_404(rec_id)
        if not recurrence.account_id == acc_id:
            abort(409, message="Recurrence does not belong to account")

        db.session.delete(recurrence)
        db.session.commit()

        return {"message": "Recurrence successfully deleted"}


@blp.route("/recurrent")
class RecurrentList(MethodView):
    @jwt_required()
    @blp.response(200, RecurrentSchema(many=True))
    def get(self):
        acc_id = get_jwt_identity()
        return RecurrentModel.query.filter(RecurrentModel.account_id == acc_id).all()
    
    @jwt_required()
    @blp.arguments(RecurrentSchema)
    @blp.response(201, RecurrentSchema)
    def post(self, rec_data):
        acc_id = get_jwt_identity()
        recurrence = RecurrentModel(account_id=acc_id, **rec_data)

        try:
            db.session.add(recurrence)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error whilst inserting recurrent into database")
        
        # If the effect date is today generate a revenue entry
        while recurrence.effect_date <= date.today():
            # add row to revenue
            revenue = RevenueModel(name=recurrence.name,
                                   description=recurrence.description,
                                   type=recurrence.type,
                                   amount=recurrence.amount,
                                   account_id=acc_id,
                                   category_id=recurrence.category_id,
                                   recurrent_id=recurrence.id)
            try:
                db.session.add(revenue)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="Error whilst inserting revenue into database")
            
            # add new effect date if frequency is not null
            if recurrence.frequency == "once":
                break
            if recurrence.frequency == "daily":
                recurrence.effect_date = recurrence.effect_date + timedelta(days=1)
            if recurrence.frequency == "weekly":
                recurrence.effect_date = recurrence.effect_date + timedelta(weeks=1)
            if recurrence.frequency == "monthly":
                recurrence.effect_date = recurrence.effect_date + timedelta(months=1)
            if recurrence.frequency == "yearly":
                recurrence.effect_date = recurrence.effect_date + timedelta(years=1)


        db.session.add(recurrence)
        db.session.commit()
    
        return recurrence