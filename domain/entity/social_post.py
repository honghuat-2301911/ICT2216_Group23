class Post:
    def __init__(self, id, user, content, image_url, created_at, likes, comments=None):
        self.id = id
        self.user = user
        self.content = content
        self.image_url = image_url
        self.created_at = created_at
        self.likes = likes
        self.comments = comments or []

class Comment:
    def __init__(self, id, post_id, user, content, created_at):
        self.id = id
        self.post_id = post_id
        self.user = user
        self.content = content
        self.created_at = created_at 