# from data_source.login_queries import fetch_user_by_email, insert_user
from domain.entity.user import User

def test_print_user(id: int, email: str, password: str, name: str) -> User | None:
    list = [id, email, password, name]
    return list


