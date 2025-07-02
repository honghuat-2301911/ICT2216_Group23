# presentation/controller/social_feed_controller.py
import functools

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from data_source.user_queries import get_user_by_id, search_users_by_name
from domain.control.social_feed_management import (
    create_comment_control,
    create_post_control,
    get_all_posts_control,
    get_featured_posts_control,
    get_post_by_id_control,
    get_posts_by_user_id_control,
    like_post_control,
    unlike_post_control,
)
from domain.entity.forms import CommentForm, PostForm

social_feed_bp = Blueprint("social_feed", __name__, url_prefix="/feed")


def user_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "user":
            return redirect(url_for("admin.bulletin_page"))
        return func(*args, **kwargs)

    return wrapper


@social_feed_bp.route("/", methods=["GET"])
@login_required
@user_required
def feed():
    posts = get_all_posts_control()
    featured_posts = get_featured_posts_control()
    post_form = PostForm()
    comment_form = CommentForm()
    return render_template(
        "socialfeed/social_feed.html",
        posts=posts,
        featured_posts=featured_posts,
        post_form=post_form,
        comment_form=comment_form,
    )


@social_feed_bp.route("/create", methods=["POST"])
@login_required
@user_required
def create_post():
    post_form = PostForm()
    if not post_form.validate_on_submit():
        flash("Cannot submit empty post.", "error")
        return redirect(url_for("social_feed.feed"))

    user_id = int(current_user.get_id())
    content = post_form.content.data
    image_file = post_form.image.data
    create_post_control(user_id, content, image_file)
    return redirect(url_for("social_feed.feed"))


@social_feed_bp.route("/comment/<int:post_id>", methods=["POST"])
@login_required
@user_required
def create_comment(post_id):
    comment_form = CommentForm()
    if not comment_form.validate_on_submit():
        flash("Cannot submit empty comment.", "error")
        return redirect(url_for("social_feed.feed"))

    user_id = int(current_user.get_id())
    content = comment_form.comment.data
    create_comment_control(post_id, user_id, content)
    return redirect(url_for("social_feed.feed"))


@social_feed_bp.route("/like/<int:post_id>", methods=["POST"])
@login_required
@user_required
def like_post(post_id):
    success = like_post_control(post_id)
    return {"success": success}


@social_feed_bp.route("/unlike/<int:post_id>", methods=["POST"])
@login_required
@user_required
def unlike_post(post_id):
    success = unlike_post_control(post_id)
    return {"success": success}


@social_feed_bp.route("/post/<int:post_id>", methods=["GET"])
@login_required
@user_required
def view_post(post_id):
    posts = get_all_posts_control()
    featured_posts = get_featured_posts_control()
    target = get_post_by_id_control(post_id)
    if not target:
        return redirect(url_for("social_feed.feed"))

    filtered = [p for p in posts if p.id == post_id]
    return render_template(
        "socialfeed/social_feed.html",
        posts=filtered,
        featured_posts=featured_posts,
        filtered_post_id=post_id,
        post_form=PostForm(),
        comment_form=CommentForm(),
    )


@social_feed_bp.route("/search-users", methods=["GET"])
@login_required
@user_required
def search_users():
    term = request.args.get("q", "")
    if len(term) < 2:
        return jsonify([])
    users = search_users_by_name(term, limit=10)
    return jsonify(
        [
            {
                "id": u["id"],
                "name": u["name"],
                "email": u["email"],
                "profile_picture": u.get("profile_picture", ""),
            }
            for u in users
        ]
    )


@social_feed_bp.route("/user/<int:user_id>", methods=["GET"])
@login_required
@user_required
def view_user_posts(user_id):
    posts = get_posts_by_user_id_control(user_id)
    featured = get_featured_posts_control()
    user_data = get_user_by_id(user_id) or {}
    return render_template(
        "socialfeed/social_feed.html",
        posts=posts,
        featured_posts=featured,
        filtered_user_id=user_id,
        filtered_user_name=user_data.get("name"),
        filtered_user_profile_picture=user_data.get("profile_picture"),
        post_form=PostForm(),
        comment_form=CommentForm(),
    )
