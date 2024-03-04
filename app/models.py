import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
from time import time
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db, login
from flask_login import UserMixin
from hashlib import md5

followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True)
)


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

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    
    followers:so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')


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
    
    def follow(self, user):
        """Allows a Unique User id to Follow another Unique User id"""
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        """Allows a Unique User id to Unfollow another Unique User id"""
        if self.is_following(user):
            self.following.remove(user)
    
    def is_following(self, user):
        """Checks whether a Unique User id is
        following another Unique User id"""
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None
    
    def followers_count(self):
        """Returns the number of User ids that follow a unique User id"""
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)
    
    def following_count(self):
        """Returns the number of User ids that are following a Unique User id"""
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    
    def following_posts(self):
        """Returns Posts written by Users the User id
        associated with a User Follows
        """
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return(
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(sa.or_(
                Follower.id == self.id,
                Author.id == self.id,
            ))
            .group_by(Post)
            .order_by(Post.timestamp.desc())
        )
    
    def get_reset_password_token(self, expires_in=600):
        """Returns a JWT token as a string"""
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KET'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        """Takes a JWT token and attempts to decode it."""
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)

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