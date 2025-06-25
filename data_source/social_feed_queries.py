from data_source.db_connection import get_connection
import os
from werkzeug.utils import secure_filename

DUMMY_POSTS = [
    {
        'feed_id': 1,
        'id': 1,
        'user': 'Jane Doe',
        'content': 'This is my first post on SIT Sports Buddy! Excited to join the community.',
        'image_url': None,
        'likes': 2,
        'created_at': '2024-06-25 10:00',
        'comments': [
            {'id': 1, 'user': 'Jane', 'content': 'Welcome Jane!', 'created_at': '2024-06-25 10:05'},
        ]
    },
    {
        'feed_id': 2,
        'id': 2,
        'user': 'Alice',
        'content': 'Excited for the basketball game this weekend!',
        'image_url': None,
        'likes': 3,
        'created_at': '2024-05-01 10:00',
        'comments': [
            {'id': 1, 'user': 'Bob', 'content': 'Me too!', 'created_at': '2024-05-01 10:05'},
        ]
    },
    {
        'feed_id': 3,
        'id': 3,
        'user': 'Charlie',
        'content': 'Check out this cool shot from last night!',
        'image_url': '/static/img/sample.jpg',
        'likes': 5,
        'created_at': '2024-05-01 09:00',
        'comments': []
    }
]

# Helper to get the next feed_id or comment id
def _next_feed_id():
    return max((p['feed_id'] for p in DUMMY_POSTS), default=0) + 1

def _next_comment_id(post):
    return max((c['id'] for c in post['comments']), default=0) + 1

def get_all_posts():
    return DUMMY_POSTS

def add_post(user, content, image_url=None):
    new_post = {
        'feed_id': _next_feed_id(),
        'id': _next_feed_id(),
        'user': user,
        'content': content,
        'image_url': image_url,
        'likes': 0,
        'created_at': 'Just now',
        'comments': []
    }
    DUMMY_POSTS.insert(0, new_post)

def add_comment(feed_id, user, content):
    for post in DUMMY_POSTS:
        if post['feed_id'] == feed_id:
            new_comment = {
                'id': _next_comment_id(post),
                'user': user,
                'content': content,
                'created_at': 'Just now'
            }
            post['comments'].append(new_comment)
            break

def get_posts_by_user(username):
    return [post for post in DUMMY_POSTS if post['user'] == username]

def add_post_to_db(user_id, content, image_file=None):
    connection = get_connection()
    if connection is None:
        print("[DB ERROR] Could not connect to database.")
        return
    cursor = connection.cursor()
    image_url = None

    # Handle image upload (save to static/images/social/)
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join('presentation', 'static', 'images', 'social', filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image_file.save(image_path)
        image_url = f'/static/images/social/{filename}'

    query = """
        INSERT INTO feed (user_id, caption, image, like_count)
        VALUES (%s, %s, %s, 0)
    """
    cursor.execute(query, (user_id, content, image_url))
    connection.commit()
    cursor.close()
    connection.close()
