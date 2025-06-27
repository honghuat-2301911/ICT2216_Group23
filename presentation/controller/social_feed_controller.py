"""Controller for social feed routes and logic

Handles displaying the feed, creating posts, and adding comments
"""

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, current_user

from domain.control.social_feed_management import (
    get_all_posts_control, get_featured_posts_control, create_post_control,
    create_comment_control, like_post_control, unlike_post_control
)

social_feed_bp = Blueprint("social_feed", __name__, url_prefix="/feed")


@social_feed_bp.route("/", methods=["GET"])
@login_required
def feed():
    """Render the main social feed page with all posts"""
    posts = get_all_posts_control()
    featured_posts = get_featured_posts_control()
    return render_template("socialfeed/social_feed.html", posts=posts, featured_posts=featured_posts)


@social_feed_bp.route("/create", methods=["POST"])
@login_required
def create_post():
    """Handle creation of a new post, including optional image upload"""
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))
    
    user_id = int(current_user.get_id())
    content = request.form["content"]
    image_file = request.files.get("image") if "image" in request.files else None

    create_post_control(user_id, content, image_file)
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
    create_comment_control(post_id, user_id, content)
    return redirect(url_for("social_feed.feed"))


@social_feed_bp.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    success = like_post_control(post_id)
    return {"success": success}


@social_feed_bp.route("/unlike/<int:post_id>", methods=["POST"])
@login_required
def unlike_post(post_id):
    success = unlike_post_control(post_id)
    return {"success": success}
