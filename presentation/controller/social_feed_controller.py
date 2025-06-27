"""Controller for social feed routes and logic

Handles displaying the feed, creating posts, and adding comments
"""

import os

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from data_source.social_feed_queries import add_comment, add_post, get_all_posts, increment_like, decrement_like, get_featured_posts, search_posts

social_feed_bp = Blueprint("social_feed", __name__, url_prefix="/feed")


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


@social_feed_bp.route("/", methods=["GET"])
@login_required
def feed():
    """Render the main social feed page with all posts"""
    posts = get_all_posts()
    featured_posts = get_featured_posts()
    return render_template("socialfeed/social_feed.html", posts=posts, featured_posts=featured_posts)


@social_feed_bp.route("/create", methods=["POST"])
@login_required
def create_post():
    """Handle creation of a new post, including optional image upload"""
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))
    
    user_id = int(current_user.get_id())
    content = request.form["content"]
    image_url = None

    if "image" in request.files:
        file = request.files["image"]
        filename = file.filename
        if file and filename and allowed_file(filename):
            filename = secure_filename(filename)
            upload_folder = current_app.config.get(
                "UPLOAD_FOLDER", "presentation/static/images/social"
            )
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            image_url = f"/static/images/social/{filename}"

    add_post(user_id, content, image_url)
    return redirect(url_for("social_feed.feed"))


@social_feed_bp.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    """Handle creation of a new comment for a specific post

    Args:
        post_id (int): The ID of the post to comment on
    """
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))
    
    user_id = int(current_user.get_id())
    content = request.form["comment"]
    add_comment(post_id, user_id, content)
    return redirect(url_for("social_feed.feed"))


@social_feed_bp.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    success = increment_like(post_id)
    return {"success": success}


@social_feed_bp.route("/unlike/<int:post_id>", methods=["POST"])
@login_required
def unlike_post(post_id):
    success = decrement_like(post_id)
    return {"success": success}
