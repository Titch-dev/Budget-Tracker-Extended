import uuid, datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import recurrents
from schemas import RecurrentSchema, RecurrentUpdateSchema

blp = Blueprint("Recurrents", __name__, description="Operations on Recurrence")

@blp.route("/recurrent/<string:rec_id>")
class Recurrent(MethodView):
    def get(self, rec_id):
        try:
            return recurrents[rec_id]
        except KeyError:
            abort(404, message="Recurrence not found")
    
    @blp.arguments(RecurrentUpdateSchema)
    def put(self, rec_data, rec_id):
        if rec_data["amount"] < 0:
            abort(400, message="Amount cannot be less than 0")

        try:
            recurrance = recurrents[rec_id]
            recurrance |= rec_data
            return {"message": "Recurrence updated"}
        except KeyError:
            abort(404, message="Recurrence not found")
    
    def delete(self, rec_id):
        try:
            del recurrents[rec_id]
            return {"message": "Recurrence deleted"}
        except KeyError:
            abort(404, "Recurrance not found")

@blp.route("/recurrent")
class RecurrentList(MethodView):
    def get(self):
        return {"Recurrents": list(recurrents.items())}
    
    @blp.arguments(RecurrentSchema)
    def post(self, rec_data):
        rec_id = uuid.uuid4().hex
        rec_created = datetime.datetime.now()
        recurrence = {**rec_data, "id":rec_id, "created": rec_created}
        recurrents[rec_id] = recurrence
        
        return recurrence, 201