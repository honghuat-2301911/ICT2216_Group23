from data_source.db_connection import get_connection

def delete_sports_activity(activity_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sports_activity WHERE id = %s", (activity_id,))
    connection.commit()
    success = cursor.rowcount > 0
    cursor.close()
    connection.close()
    return success    