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
    annually = "annually"

class PlainAccountSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    balance = fields.Int(dump_only=True)
    created = fields.Date(dump_only=True)
    last_login = fields.Date(dump_only=True)
    intro_done = fields.Bool(dump_only=True)

class PlainRevenueSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    type = fields.Enum(revenue_enum, required=True)
    amount = fields.Float(required=True)
    created = fields.Date(dump_only=True)

class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    budget = fields.Float()
    created = fields.Date(dump_only=True)

class PlainGoalSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    balance = fields.Float()
    goal_target = fields.Float()
    end_date = fields.Date()
    created = fields.Date(dump_only=True)

class PlainRecurrentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    type = fields.Enum(revenue_enum, required=True)
    amount = fields.Float(required=True)
    frequency = fields.Enum(frequency_enum, required=True)
    effect_date = fields.Date(required=True)
    end_date = fields.Date()
    created = fields.Date(dump_only=True)

### Account ###
class AccountSchema(PlainAccountSchema):
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)
    goals = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)
    recurrents = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)
    revenues = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)

class AccountUpdateSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    balance = fields.Float()

### Revenue ###
class RevenueSchema(PlainRevenueSchema):
    account_id = fields.Int(required=True, load_only=True)
    category_id = fields.Int(required=True)
    recurrent_id = fields.Int(dump_only=True)
    account = fields.Nested(PlainAccountSchema(), dump_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)
    recurrent = fields.Nested(PlainRecurrentSchema(), dump_only=True)

class RevenueUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Enum(revenue_enum)
    amount = fields.Float()
    category_id = fields.Int()

### Category ###
class CategorySchema(PlainCategorySchema):
    account_id = fields.Int(load_only=True)
    account = fields.Nested(PlainAccountSchema(), dump_only=True)

class CategoryUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    budget = fields.Float()

### Goal ###
class GoalsSchema(PlainGoalSchema):
    account_id = fields.Int(dump_only=True)
    account = fields.Nested(PlainAccountSchema(), dump_only=True)
    recurrents = fields.List(fields.Nested(PlainRecurrentSchema(), 
                                          dump_only=True))

class GoalUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    goal_target = fields.Float()
    end_date = fields.Date()

### Recurrent ###
class RecurrentSchema(PlainRecurrentSchema):
    account_id = fields.Int(dump_only=True)
    category_id = fields.Int(required=True)
    goal_id = fields.Int()
    account = fields.Nested(PlainAccountSchema(), dump_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)
    goal = fields.Nested(PlainGoalSchema(), dump_only=True)
    revenues = fields.List(fields.Nested(PlainCategorySchema(),
                                        dump_only=True))

class RecurrentUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Enum(revenue_enum)
    amount = fields.Float()
    frequency = fields.Enum(frequency_enum)
    effect_date = fields.Date()
    end_date = fields.Date()
    category_id = fields.Int()
