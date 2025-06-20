# from data_source.login_queries import fetch_user_by_email, insert_user
from domain.entity.user import User
from data_source.user_queries import *;
from domain.control.auth_management import *;

def login_user(email: str, password: str):
    result = get_user_by_email(email)
    if not result:
        return None  # User not found in DB
    else:
        result = User(**result)
        return result
    # if check_password(password, result["password"]):
    #     return User(**result)
    # else:
    #     return None

    

    


