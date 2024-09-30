from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import GoalModel
from schemas import GoalsSchema, GoalUpdateSchema

blp = Blueprint("goals", __name__, description="Operations on Goals")

@blp.route("/goals/<int:goal_id>")
class Goal(MethodView):
    @jwt_required()
    @blp.response(200, GoalsSchema)
    def get(self, goal_id):
        acc_id = get_jwt_identity()
        goal = GoalModel.query.get_or_404(goal_id)
        if not goal.account_id == acc_id:
            abort(409, message="Goal does not belog to account")
        return goal

    @jwt_required()
    @blp.arguments(GoalUpdateSchema)
    @blp.response(200, GoalsSchema)
    def put(self, goal_data, goal_id):
        acc_id = get_jwt_identity()
        goal = GoalModel.query.get_or_404(goal_id)
        if not goal.account_id == acc_id:
            abort(409, message="Goal does not belog to account")
        
        if goal:
            # Update only the fields the client has posted
            for key in goal_data.keys():
                if hasattr(goal, key):
                    setattr(goal, key, goal_data[key])
        
        db.session.add(goal)
        db.session.commit()

        return goal
    
    @jwt_required()
    def delete(self, goal_id):
        acc_id = get_jwt_identity()
        goal = GoalModel.query.get_or_404(goal_id)
        if not goal.account_id == acc_id:
            abort(409, message="Goal does not belong to account")
        db.session.delete(goal)
        db.session.commit()
        return {"message": "Goal successfully deleted"}
        


@blp.route("/goals")
class GoalList(MethodView):
    @jwt_required()
    @blp.response(200, GoalsSchema(many=True))
    def get(self):
        acc_id = get_jwt_identity()
        return GoalModel.query.filter(GoalModel.account_id == acc_id).all()

    @jwt_required()
    @blp.arguments(GoalsSchema)
    @blp.response(201, GoalsSchema)
    def post(self, goal_data):
        # Constraint on if goal name exists for account
        acc_id = get_jwt_identity()
        if GoalModel.query.filter(GoalModel.account_id == acc_id,
                                      GoalModel.name == goal_data["name"]).first():
            abort(400, message="Goal name already exists")
        goal = GoalModel(account_id=acc_id, **goal_data)
        
        try:
            db.session.add(goal)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message=f"Error whilst inserting goal into database")

        return goal
