from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import GoalModel
from schemas import GoalsSchema, GoalUpdateSchema

blp = Blueprint("goals", __name__, description="Operations on Goals")

@blp.route("/goals/<string:goal_id>")
class Goal(MethodView):
    @blp.response(200, GoalsSchema)
    def get(self, goal_id):
        goal = GoalModel.query.get_or_404(goal_id)
        return goal


    @blp.arguments(GoalUpdateSchema)
    @blp.response(201, GoalsSchema)
    def put(self, goal_data, goal_id):
        goal = GoalModel.query.get(goal_id)

        if goal:
            goal.name = goal_data["name"]
            goal.description = goal_data["description"]
            goal.balance = goal_data["balance"]
            goal.goal_target = goal_data["goal_target"]
            goal.end_date = goal_data["end_date"]
        else:
            goal = GoalModel(id=goal_id, **goal_data)
        
        db.session.add(goal)
        db.session.commit()

        return goal
    

    def delete(self, goal_id):
        goal = GoalModel.query.get_or_404(goal_id)
        raise NotImplementedError("Deleting goal not implemented.")


@blp.route("/goals")
class GoalList(MethodView):
    @blp.response(200, GoalsSchema(many=True))
    def get(self):
        return goals.values()


    @blp.arguments(GoalsSchema)
    @blp.response(201, GoalsSchema)
    def post(self, goal_data):
        goal = GoalModel(**goal_data)
        
        try:
            db.session.add(goal)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error whilst inserting goal into database")

        return goal