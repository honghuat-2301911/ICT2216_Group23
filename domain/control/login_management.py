from flask import g
from domain.entity.user import User
from data_source.user_queries import get_user_by_email

def login_user(email: str, password: str):
    result = get_user_by_email(email)
    if not result:
        return None

    user = User(
        id=result["id"],
        name=result["name"],
        password=result["password"],
        email=result["email"],
        role=result.get("role", "user")
    )

    g.current_user = user  # Store in request scope
    return user

def get_user_display_data():
    user = g.get("current_user")
    if not user:
        return None

    return {
        # "id": user.get_id(), # Uncomment if you want to display user ID
        "name": user.get_name(),
        "email": user.get_email(),
        "role": user.get_role()
    }

    


