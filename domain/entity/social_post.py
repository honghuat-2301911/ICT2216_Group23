"""Defines domain entities for social media posts and comments"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Comment:
    """A comment on a social media post"""

    id_: int
    post_id: int
    user: str
    content: str
    created_at: str


@dataclass
class Post:
    """A social media post"""

    id_: int
    user: str
    content: str
    image_url: str
    created_at: str
    likes: int
    comments: List[Comment] = field(default_factory=list)
