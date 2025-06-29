"""Social feed management for handling posts, comments, and interactions

Contains business logic for social feed operations including post creation,
comment management, and like/unlike functionality.
"""

import os
from flask import g, current_app
from werkzeug.utils import secure_filename

from data_source.social_feed_queries import (
    add_comment, add_post, get_all_posts, increment_like, 
    decrement_like, get_featured_posts, get_post_by_id, update_post, delete_post as ds_delete_post
)
from domain.entity.social_post import Post, Comment


def allowed_file(filename):
    """Check if the uploaded file has an allowed image extension

    Args:
        filename (str): The name of the file

    Returns:
        bool: True if the file is allowed, False otherwise
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }


def create_entity_from_row(result):
    """Convert database rows to Post entities using actual DB field names

    Args:
        result (list): List of database row dictionaries

    Returns:
        list: List of Post entities
    """
    post_list = []
    
    for row in result:
        # Convert comments to Comment entities
        comments = []
        for comment_data in row.get('comments', []):
            comment = Comment(
                id=comment_data['id'],
                post_id=row['id'],
                user=comment_data.get('user', ''),
                content=comment_data.get('content', ''),
                created_at=""  # No created_at in current schema
            )
            comments.append(comment)
        
        # Create Post entity using only DB field names
        post = Post(
            id=row['id'],
            user=row.get('user_name', ''),
            content=row.get('caption', ''),
            image_url=row.get('image_path', ''),
            created_at="",  # No created_at in current schema
            likes=row.get('like_count', 0) or 0,
            comments=comments
        )
        post_list.append(post)
    
    g.post_list = post_list
    return post_list


def get_all_posts_control():
    """Get all posts for display in the social feed

    Returns:
        list: List of Post entities
    """
    result = get_all_posts()
    if not result:
        return []
    
    post_list = create_entity_from_row(result)
    return post_list


def get_featured_posts_control():
    """Get featured posts (top 5 by likes) for display

    Returns:
        list: List of Post entities for featured section
    """
    result = get_featured_posts()
    if not result:
        return []
    
    # Convert raw DB data to Post entities
    featured_list = []
    for row in result:
        # Create Post entity using only DB field names
        post = Post(
            id=row['id'],
            user=row.get('user_name', ''),
            content=row.get('caption', ''),
            image_url=row.get('image_path', ''),
            created_at="",  # No created_at in current schema
            likes=row.get('like_count', 0) or 0,
            comments=[]  # Featured posts don't need comments
        )
        featured_list.append(post)
    
    return featured_list


def create_post_control(user_id, content, image_file=None):
    """Handle creation of a new post with optional image upload

    Args:
        user_id (int): ID of the user creating the post
        content (str): Text content of the post
        image_file: Optional uploaded image file

    Returns:
        bool: True if post was created successfully, False otherwise
    """
    image_url = None
    
    if image_file and image_file.filename:
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            upload_folder = current_app.config.get(
                "UPLOAD_FOLDER", "presentation/static/images/social"
            )
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            image_file.save(filepath)
            image_url = f"/static/images/social/{filename}"
    
    return add_post(user_id, content, image_url)


def create_comment_control(post_id, user_id, content):
    """Handle creation of a new comment on a post

    Args:
        post_id (int): ID of the post to comment on
        user_id (int): ID of the user making the comment
        content (str): Text content of the comment

    Returns:
        bool: True if comment was created successfully, False otherwise
    """
    return add_comment(post_id, user_id, content)


def like_post_control(post_id):
    """Handle liking a post (increment like count)

    Args:
        post_id (int): ID of the post to like

    Returns:
        bool: True if like was successful, False otherwise
    """
    return increment_like(post_id)


def unlike_post_control(post_id):
    """Handle unliking a post (decrement like count)

    Args:
        post_id (int): ID of the post to unlike

    Returns:
        bool: True if unlike was successful, False otherwise
    """
    return decrement_like(post_id)


def get_posts_display_data():
    """Get formatted display data for posts

    Returns:
        list: List of post dictionaries formatted for template display
    """
    post_list = g.get("post_list")
    if not post_list:
        return []

    display_data = []
    for post in post_list:
        display_data.append({
            "id": post.id,
            "user": post.user,
            "content": post.content,
            "image_url": post.image_url,
            "likes": post.likes,
            "comments": [
                {
                    "id": comment.id,
                    "user": comment.user,
                    "content": comment.content
                } for comment in post.comments
            ]
        })

    return display_data


def editPost(userId: int, postId: int, updatedContent: str, removeImage: bool = False, newImage: str = None) -> bool:
    post = get_post_by_id(postId)
    if not post or int(post['user_id']) != userId:
        return False

    image_filename = post.get('image_path')
    # Remove image if requested
    if removeImage and image_filename:
        image_path = os.path.join('presentation', 'static', 'uploads', os.path.basename(image_filename))
        if os.path.exists(image_path):
            os.remove(image_path)
        image_filename = None

    # Replace image if new one uploaded
    if newImage:
        # Optionally remove old image
        if image_filename:
            old_image_path = os.path.join('presentation', 'static', 'uploads', os.path.basename(image_filename))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        image_filename = newImage

    # Update post in DB
    return update_post(postId, updatedContent, image_filename)


def deletePost(userId: int, postId: int) -> bool:
    post = get_post_by_id(postId)
    if not post or int(post['user_id']) != userId:
        return False
    image_filename = post.get('image_path')
    if image_filename:
        image_path = os.path.join('presentation', 'static', 'uploads', os.path.basename(image_filename))
        if os.path.exists(image_path):
            os.remove(image_path)
    return ds_delete_post(postId)
