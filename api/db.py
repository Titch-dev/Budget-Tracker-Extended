accounts = {
    "1" : {
        "id": 1,
        "name": "Titch",
        "password": "password",
        "email": "test@test.com",
        "created": "18/09/2024",
        "last_login": "18/09/2024"
    },
    "2" : {
        "id": 1,
        "name": "Titch",
        "password": "password",
        "email": "test@test.com",
        "created": "18/09/2024",
        "last_login": "18/09/2024"
    }
}

revenues = {
    "1" : {
        "id": 1,
        "name": "Rent",
        "description": "Outgoing rental",
        "type": "expenditure",
        "amount": 1500,
        "created": "18/09/2024",
        "account_id": 1,
        "category": 1
    },
    "2" : {
        "id": 2,
        "name": "salary",
        "description": "wage",
        "type": "income",
        "amount": 100,
        "created": "18/09/2024",
        "account_id": 1,
        "category": 1
    }
}

categories = {
    "1" : {
        "id": 1,
        "name": "work",
        "description": "monthly salary",
        "created": "18/09/2024",
        "account_id": 1
    },
    "2" : {
        "id": 2,
        "name": "work",
        "description": "monthly salary",
        "created": "18/09/2024",
        "account_id": 1
    }
}

goals = {
    "1" : {
        "id": 1,
        "name": "Holiday",
        "description": "Holiday Fund",
        "balance": 100,
        "goal_target": 500,
        "end_date": "25/09/2024",
        "created": "18/09/2024",
        "account_id": 1
    }
}

recurrents = {
    "1" : {
        "id": 1,
        "name": "work",
        "description": "monthly salary",
        "frequency": "m",
        "type": "income",
        "amount": 500,
        "effect_date": "18/10/2024",
        "end_date": None,
        "created": "18/09/2024",
        "account_id": 1,
        "category": 1
    }
}