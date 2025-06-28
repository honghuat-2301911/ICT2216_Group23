from flask import g
from domain.entity.sports_activity import SportsActivity
from data_source.bulletin_queries import *
from data_source.admin_queries import *
from flask_login import current_user


def remove_sports_activity(activity_id: int):
    """
    Deletes an activity from the bulletin board by its ID.
    Returns True if successful, False otherwise.
    """
    try:
        # Fetch the current activity to check if it exists
        activity = get_sports_activity_by_id(activity_id)
        if not activity:
            return False
        
        # Delete the activity
        return delete_sports_activity(activity_id)

    except Exception as e:
        print(f"Error deleting activity: {e}")
        return False