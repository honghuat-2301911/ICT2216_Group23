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

from data_source.social_feed_queries import add_comment, add_post, get_all_posts

social_feed_bp = Blueprint("social_feed", __name__, url_prefix="/feed")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }


@social_feed_bp.route("/", methods=["GET"])
def feed():
    posts = get_all_posts()
    return render_template("socialfeed/social_feed.html", posts=posts)


@social_feed_bp.route("/create", methods=["POST"])
def create_post():
    user = session.get("username", "Anonymous")
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
def create_comment(post_id):
    user = session.get("username", "Anonymous")
    content = request.form["comment"]
    add_comment(post_id, user, content)
    return redirect(url_for("social_feed.feed"))
