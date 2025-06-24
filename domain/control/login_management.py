from flask import g

from data_source.user_queries import get_user_by_email
from domain.entity.user import User


def login_user(email: str, password: str):
    result = get_user_by_email(email)
    if not result:
        return None

    user = User(
        id=result["id"],
        name=result["name"],
        password=result["password"],
        email=result["email"],
        skill_lvl=result.get("skill_lvl"),
        sports_exp=result.get("sports_exp"),
        role=result.get("role", "user"),
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
        "skill_lvl": user.get_skill_lvl(),
        "sports_exp": user.get_sports_exp(),
        "role": user.get_role(),
    }
