import uuid, datetime
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import goals
from schemas import GoalsSchema, GoalUpdateSchema

blp = Blueprint("goals", __name__, description="Operations on Goals")

@blp.route("/goals/<string:goal_id>")
class Goal(MethodView):
    def get(self, goal_id):
        try:
            return goals[goal_id]
        except KeyError:
            abort(404, message="Goal not found")

    @blp.arguments(GoalUpdateSchema)
    def put(self, goal_data, goal_id):
        try:
            goal = goals[goal_id]
            goal |= goal_data
            return {"message": "Goal updated"}
        except KeyError:
            abort(404, message="Goal not found")
    
    def delete(self, goal_id):
        try:
            del goals[goal_id]
            return {"message" : "Goal deleted"}
        except KeyError:
            abort(404, message="Goal not found")

@blp.route("/goals")
class GoalList(MethodView):
    def get(self):
        return {"goals": list(goals.items())}

    @blp.arguments(GoalsSchema)
    def post(self, goal_data):
        # TODO: validation that the information is as expected
        for goal in goals.values():
            if goal["name"] == goal_data["name"]:
                abort(400, message="Goal already exists with this name")
            if goal_data["balance"] < 0:
                abort(400, message="Goal balance cannot be less than 0")   
            if goal_data["goal_target"] < 0:
                abort(400, message="Goal target cannot be less than 0")
        
        goal_id = uuid.uuid4().hex
        goal_created = datetime.datetime.now()
        goal = {**goal_data, "id": goal_id, "created": goal_created}
        goals[goal_id] = goal

        return goal, 201