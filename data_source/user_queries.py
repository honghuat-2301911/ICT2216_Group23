from data_source.db_connection import get_connection

def get_user_by_email(email: str):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_data

def insert_user(user_data):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO user (id, name, password, email, skill_lvl, sports_exp, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data['id'],
            user_data['name'],
            user_data['password'],
            user_data['email'],
            user_data['skill_lvl'],
            user_data['sports_exp'],
            user_data['role']
        ))
        connection.commit()
        return True
    except Exception as e:
        print("Insert failed:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

