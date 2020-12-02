from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy.sql import func
import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class InfluencerList(db.Model):
    """A list."""

    __tablename__ = "influencer_lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user = db.relationship('User', backref='lists')

    def __repr__(self):
        return f'<List list_id={self.list_id} Title={self.title}>'


class Influencer(db.Model):
    """Saved Influencers."""

    __tablename__ = "influencers"

    influencer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('influencer_lists.list_id'))
    channel_title = db.Column(db.String)
    channel_desc = db.Column(db.String)
    subscriber_count = db.Column(db.Integer)
    video_count = db.Column(db.Integer)
    view_count = db.Column(db.Integer)
    email = db.Column(db.String)
    URL = db.Column(db.String)
    contacted = db.Column(db.Boolean, default=False)

    user = db.relationship('InfluencerList', backref='influencers')

    def __repr__(self):
        return f'<Influencer list={self.list_id} Channel={self.channel_title}>'



def connect_to_db(flask_app, db_uri='postgresql:///youtubedata', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app



    connect_to_db(app)
