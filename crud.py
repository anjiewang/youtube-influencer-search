"""CRUD operations."""

from model import db, User, InfluencerList, Influencer, connect_to_db
from datetime import datetime

def create_user(email, password, first_name, last_name):
    """Create and return a new user."""

    user = User(email=email, password=password, first_name=first_name, last_name=last_name)

    db.session.add(user)
    db.session.commit()

    return user

def create_list(user_id, title):
    """Create and return a new movie."""

    influencer_list = InfluencerList(
        user_id = user_id,
        title = title
        )

    db.session.add(influencer_list)
    db.session.commit()

    return influencer_list

def get_first_name(user_id):
    
    first_name = User.query.filter_by(user_id=user_id).first()

    return first_name.first_name
    
def count_total_influencers_saved(user_id):
    list_ids = InfluencerList.query.filter_by(user_id=user_id).all()

    number = 0
    
    for lid in list_ids:
        list_id = lid.list_id
        count = db.session.query(Influencer.influencer_id).filter(Influencer.list_id==list_id).count()
        number += count
    
    return number

def count_total_influencers_contacted(user_id):
    list_ids = InfluencerList.query.filter_by(user_id=user_id).all()

    number = 0
    
    for lid in list_ids:
        list_id = lid.list_id
        count = db.session.query(Influencer.influencer_id).filter(Influencer.list_id==list_id, Influencer.contacted==True).count()
        number += count
    
    return number

def count_total_lists(user_id):

    count = db.session.query(InfluencerList.list_id).filter(User.user_id==user_id).count()

    return count


def get_list_by_user(user_id):
    """Get influencer lists using User ID"""
    influencer_list = InfluencerList.query.filter_by(user_id=user_id).all()

    return influencer_list

def add_influencer(user_id, title, channel_title, channel_desc, subscriber_count, video_count, view_count, email, URL):
    """Create and return a rating"""

    list_id = get_list_id_by_user(user_id, title)

    influencer = Influencer(
        list_id = list_id,
        channel_title = channel_title, 
        channel_desc = channel_desc, 
        subscriber_count = subscriber_count,
        video_count = video_count,
        view_count = view_count,
        email = email,
        URL = URL
        )
        
    
    db.session.add(influencer)
    db.session.commit()

    return influencer

def remove_influencer(user_id, list_title, channel_title):
    """Remove an influencer from a list"""

    list_id = get_list_id_by_user(user_id, list_title)

    print(list_id, channel_title)


    Influencer.query.filter_by(list_id=list_id, channel_title=channel_title).delete()
    
        
    db.session.commit()

def mark_contacted(user_id, list_title, channel_title):
    """Remove an influencer from a list"""

    list_id = get_list_id_by_user(user_id, list_title)

    print(list_id, channel_title)

    influencer = Influencer.query.filter_by(list_id=list_id, channel_title=channel_title).first()
    influencer.contacted = True
    
    db.session.commit()


def get_list_id_by_user(user_id, title):
    """Create a list of all users."""

    influencer_list = InfluencerList.query.filter_by(user_id=user_id,title=title).first()
    list_id = influencer_list.list_id

    return list_id

def get_influencers_by_title(user_id, list_title):

    list_id = get_list_id_by_user(user_id, list_title)

    influencers = Influencer.query.filter_by(list_id=list_id).all()

    return influencers

def get_user_by_id(user_id):
    """Get user by id"""

    user = User.query.get(user_id)

    return user

def get_user_by_email(email):

    user = User.query.filter(User.email==email).first()

    return user

if __name__ == '__main__':
    from server import app
    connect_to_db(app)