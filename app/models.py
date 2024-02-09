from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    """Database Model Table to store Particular Users of the app.
    Implements the `user` table to have the following;
    id - Integer
    username - VARCHAR(64)
    email - VARCHAR(120)
    password_hash - VARCHAR(128)
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<user {}>'.format(self.username)
    
    def set_password(self, password: str):
        """Generates a password hash to be stored in the User
        table for a particular user"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        """Checks whether a password from user evaluates to the password_hash
        associated with their id"""
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        """Fetches an Avatar to display as a User Profile Page"""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Post(db.Model):
    """Database Model Table for Blog Posts.
    Implements a `post` table to have the following;
     id - Posts key as primary key for this table
     body - the Body of the Posts
     timestamp - datetime to record created time
     user_id - the foreign key from `user` table
     """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
@login.user_loader
def load_user(id):
    """Loads a User to be tracked by a Flask's
    User session"""
    return db.session.get(User, int(id))