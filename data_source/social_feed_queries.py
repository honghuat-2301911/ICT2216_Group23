"""Dummy in-memory data and query functions for the social feed feature"""


DUMMY_POSTS = [
    {
        "feed_id": 1,
        "id": 1,
        "user": "Alice",
        "content": "Excited for the basketball game this weekend!",
        "image_url": None,
        "likes": 3,
        "created_at": "2024-05-01 10:00",
        "comments": [
            {
                "id": 1,
                "user": "Bob",
                "content": "Me too!",
                "created_at": "2024-05-01 10:05",
            },
        ],
    },
    {
        "feed_id": 2,
        "id": 2,
        "user": "Charlie",
        "content": "Check out this cool shot from last night!",
        "image_url": "/static/img/sample.jpg",
        "likes": 5,
        "created_at": "2024-05-01 09:00",
        "comments": [],
    },
]


def _next_feed_id():
    """Get the next available feed_id for a new post"""
    return max((p["feed_id"] for p in DUMMY_POSTS), default=0) + 1


def _next_comment_id(post):
    """Get the next available comment id for a given post"""
    return max((c["id"] for c in post["comments"]), default=0) + 1


def get_all_posts():
    """
    Retrieve all posts in the dummy social feed

    Returns:
        list: List of all post dictionaries
    """
    return DUMMY_POSTS


def add_post(user, content, image_url=None):
    """
    Add a new post to the dummy social feed

    Args:
        user (str): Username of the poster
        content (str): Text content of the post
        image_url (str, optional): URL of the image to attach
    """
    new_post = {
        "feed_id": _next_feed_id(),
        "id": _next_feed_id(),
        "user": user,
        "content": content,
        "image_url": image_url,
        "likes": 0,
        "created_at": "Just now",
        "comments": [],
    }
    DUMMY_POSTS.insert(0, new_post)


def add_comment(feed_id, user, content):
    """
    Add a comment to a post in the dummy social feed

    Args:
        feed_id (int): The feed ID of the post to comment on
        user (str): Username of the commenter
        content (str): Text content of the comment
    """
    for post in DUMMY_POSTS:
        if post["feed_id"] == feed_id:
            new_comment = {
                "id": _next_comment_id(post),
                "user": user,
                "content": content,
                "created_at": "Just now",
            }
            post["comments"].append(new_comment)
            break
