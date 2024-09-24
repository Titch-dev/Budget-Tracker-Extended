import enum
from marshmallow import Schema, fields

class revenue_enum(str, enum.Enum):
    income = "income"
    expenditure = "expenditure"

class frequency_enum(str, enum.Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annualy = "annually"

class AccountSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    created = fields.Date(dump_only=True)
    last_login = fields.Date(dump_only=True)
    intro_done = fields.Bool(dump_only=True)

class AccountUpdateSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()

class RevenueSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    type = fields.Enum(revenue_enum, required=True)
    amount = fields.Float(required=True)
    created = fields.Date(dump_only=True)
    account_id = fields.Str(required=True)
    category_id = fields.Str(required=True)

class RevenueUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Enum(revenue_enum)
    amount = fields.Float()
    category_id = fields.Str()

class CategorySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    budget = fields.Float()
    created = fields.Date(dump_only=True)
    account_id = fields.Str(required=True)

class CategoryUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    budget = fields.Float()

class GoalsSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    balance = fields.Float()
    goal_target = fields.Float()
    end_date = fields.Date()
    created = fields.Date(dump_only=True)
    account_id = fields.Str(required=True)

class GoalUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    goal_target = fields.Float()
    end_date = fields.Date()

class RecurrentSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    type = fields.Enum(revenue_enum, required=True)
    amount = fields.Float(required=True)
    frequency = fields.Enum(frequency_enum, required=True)
    effect_date = fields.Date(required=True)
    end_date = fields.Date()
    created = fields.Date(dump_only=True)
    account_id = fields.Str(required=True)
    category_id = fields.Str(required=True)

class RecurrentUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Enum(revenue_enum)
    amount = fields.Float()
    frequency = fields.Enum(frequency_enum)
    effect_date = fields.Date()
    end_date = fields.Date()
    category = fields.Str()