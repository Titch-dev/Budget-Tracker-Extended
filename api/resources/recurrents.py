from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RecurrentModel
from schemas import RecurrentSchema, RecurrentUpdateSchema

blp = Blueprint("Recurrents", __name__, description="Operations on Recurrence")

@blp.route("/recurrent/<string:rec_id>")
class Recurrent(MethodView):
    @blp.response(200, RecurrentSchema)
    def get(self, rec_id):
        recurrence = RecurrentModel.query.get_or_404(rec_id)
        return recurrence
    

    @blp.arguments(RecurrentUpdateSchema)
    @blp.response(201, RecurrentSchema)
    def put(self, rec_data, rec_id):
        recurrence = RecurrentModel.query.get(rec_id)

        if recurrence:
            recurrence.name = rec_data["name"]
            recurrence.description = rec_data["description"]
            recurrence.frequency = rec_data["frequency"]
            recurrence.type = rec_data["type"]
            recurrence.amount = rec_data["amount"]
            recurrence.effect_date = rec_data["effect_date"]
            recurrence.category_id = rec_data["category_id"]
        else:
            recurrence = RecurrentModel(id=rec_id, **rec_data)

        db.session.add(recurrence)
        db.session.commit()

        return recurrence
    
    
    def delete(self, rec_id):
        recurrence = RecurrentModel.query.get_or_404(rec_id)
        db.session.delete(recurrence)
        db.session.commit()
        return {"message": "Recurrence successfully deleted"}


@blp.route("/recurrent")
class RecurrentList(MethodView):
    @blp.response(200, RecurrentSchema(many=True))
    def get(self):
        return RecurrentModel.query.all()
    

    @blp.arguments(RecurrentSchema)
    @blp.response(201, RecurrentSchema)
    def post(self, rec_data):
        recurrence = RecurrentModel(**rec_data)

        try:
            db.session.add(recurrence)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error whilst inserting recurrent into database")
        
        return recurrence