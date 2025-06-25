# data_source/bulletin_feed_queries.py

DUMMY_ACTIVITIES = [
    {
        'activity_name': 'Basketball Game',
        'activity_type': 'Basketball',
        'skills_req': 'Dribbling, Shooting',
        'date': '2024-07-01 18:00',
        'location': 'SIT Sports Hall',
        'max_pax': 10,
        'user_id_list_join': '2,3,4',
        'user_id': 2
    },
    {
        'activity_name': 'Badminton Session',
        'activity_type': 'Badminton',
        'skills_req': 'Beginner',
        'date': '2024-07-05 16:00',
        'location': 'SIT Badminton Court',
        'max_pax': 6,
        'user_id_list_join': '1,2',
        'user_id': 2
    },
    {
        'activity_name': 'Pickleball Game',
        'activity_type': 'Pickleball',
        'skills_req': 'Intermediate',
        'date': '2024-07-10 15:00',
        'location': 'SIT Badminton Court',
        'max_pax': 20,
        'user_id_list_join': '2,3,4,5',
        'user_id': 1
    }
]

def get_all_activities():
    return DUMMY_ACTIVITIES 