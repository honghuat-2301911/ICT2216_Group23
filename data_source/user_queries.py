from data_source.db_connection import get_connection

def get_user_by_email(email: str):
    connection = get_connection()
    if connection is None:
        return None
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        return user_data
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_user(user_data):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO user (id, name, password, email, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data['id'],
            user_data['name'],
            user_data['password'],
            user_data['email'],
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

def update_user_profile(email, name, password=None):
    connection = get_connection()
    if connection is None:
        return False
    cursor = None
    try:
        cursor = connection.cursor()
        if password:
            cursor.execute(
                "UPDATE user SET name=%s, password=%s WHERE email=%s",
                (name, password, email)
            )
        else:
            cursor.execute(
                "UPDATE user SET name=%s WHERE email=%s",
                (name,  email)
            )
        try:
            connection.commit()
        except Exception as e:
            print("Commit failed:", e)
            return False
        return True
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_user_by_id(user_id: int):
    connection = get_connection()
    if connection is None:
        return None
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        return user_data
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def update_user_profile_by_id(user_id, name, password=None):
    connection = get_connection()
    if connection is None:
        print("No DB connection")
        return False
    cursor = None
    try:
        cursor = connection.cursor()
        if password:
            print("Running: UPDATE user SET name=%s, password=%s WHERE id=%s" % (name, password, user_id))
            cursor.execute(
                "UPDATE user SET name=%s, password=%s WHERE id=%s",
                (name, password, user_id)
            )
        else:
            print("Running: UPDATE user SET name=%s WHERE id=%s" % (name, user_id))
            cursor.execute(
                "UPDATE user SET name=%s WHERE id=%s",
                (name, user_id)
            )
        connection.commit()
        return True
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

