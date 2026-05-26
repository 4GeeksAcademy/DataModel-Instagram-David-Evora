from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

db = SQLAlchemy()


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(60),
        unique=True,
        nullable=False
    )

    firstname: Mapped[str] = mapped_column(String(60))
    lastname: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")

class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    medias: Mapped[list["Media"]] = relationship(back_populates="post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(SQLEnum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255))

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    post: Mapped["Post"] = relationship(back_populates="medias")


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class Follower(db.Model):
    __tablename__ = "followers"

    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True)

    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

#    user_from: Mapped["User"] = relationship(foreign_keys=[user_from_id])
#    user_to: Mapped["User"] = relationship(foreign_keys=[user_to_id])
