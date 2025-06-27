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

from data_source.social_feed_queries import add_comment, add_post, get_all_posts

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
    return render_template("socialfeed/social_feed.html", posts=posts)


@social_feed_bp.route("/create", methods=["POST"])
@login_required
def create_post():
    """Handle creation of a new post, including optional image upload"""
    user = current_user.get_name() if current_user.is_authenticated else "Anonymous"
    content = request.form["content"]
    image_url = None

    if "image" in request.files:
        file = request.files["image"]
        filename = file.filename
        if file and filename and allowed_file(filename):
            filename = secure_filename(filename)
            upload_folder = current_app.config.get(
                "UPLOAD_FOLDER", "presentation/static/img/uploads"
            )
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            image_url = f"/static/img/uploads/{filename}"

    add_post(user, content, image_url)
    return redirect(url_for("social_feed.feed"))


@social_feed_bp.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    """Handle creation of a new comment for a specific post

    Args:
        post_id (int): The ID of the post to comment on
    """
    user = current_user.get_name() if current_user.is_authenticated else "Anonymous"
    content = request.form["comment"]
    add_comment(post_id, user, content)
    return redirect(url_for("social_feed.feed"))
