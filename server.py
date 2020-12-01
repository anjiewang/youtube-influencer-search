from flask import Flask, render_template, request, jsonify, redirect, flash
import requests
import json
from youtube import YoutubeVideoData
from datetime import date
import sys
import crud
import scraping
import re
from model import connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'

API_KEY = "AIzaSyB7gBd3yJ6to16PESYfMIcgbf4eP2l60OI"

kw_search = YoutubeVideoData(API_KEY)


@app.route('/search')
def search():

    if current_user.is_authenticated:
        lists = crud.get_list_by_user(current_user.user_id)
        return render_template('main.html', lists=lists)
    else:
        flash('Please log in or sign up.')
        return redirect('/login')

    return render_template('main.html')

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/profile')
def load():
    list_count = crud.count_total_lists(current_user.user_id)
    print(f'THE LIST COUNT IS {list_count}')
    inf_count = crud.count_total_influencers_saved(current_user.user_id)
    print(f'THE INFLUENCER COUNT IS {inf_count}')
    print(current_user.email)
    lists = crud.get_list_by_user(current_user.user_id)
    contacted = crud.count_total_influencers_contacted(current_user.user_id)
    first_name = crud.get_first_name(current_user.user_id)

    return render_template('profile.html', name=first_name, lists=lists, list_count=list_count, inf_count=inf_count, contacted=contacted)
    

@app.route('/api/load_lists', methods=["POST"])
def load_lists():
    list_title = request.form.get("list_title")
    influencers = crud.get_influencers_by_title(current_user.user_id, list_title)

    channel_list = []
    for influencer in influencers:
            channel_dict = {
            "id" : influencer.influencer_id,
            "title" : influencer.channel_title,
            "description" : influencer.channel_desc,
            "view_count" : influencer.view_count,
            "subscriber_count" : influencer.subscriber_count,
            "video_count" : influencer.video_count,
            "email" : influencer.email,
            "url" : influencer.URL,
            "contacted" : influencer.contacted
            }
            channel_list.append(channel_dict)
    

    return jsonify({"channels":channel_list})


@app.route('/api/search', methods=["POST"])

def youtube_video_search():

    query = request.form.get("keywords")
    if "youtube.com" in query:
        query_string = re.search('v=(.*)&', query)
        if query_string:
            query = query_string.group(1)

    min_subscriber_count = request.form.get("min_subscriber_count")
    if min_subscriber_count == "":
        min_subscriber_count = 0

    max_subscriber_count = request.form.get("max_subscriber_count")
    if max_subscriber_count == "":
        max_subscriber_count = sys.maxsize

    search_type = request.form.get("type")
    print(f'HELLO the search_type is {search_type}')
    # next_page_token = request.form.get("next_page_token")

    title_keywords = request.form.get("title_keywords").split("\n")
    if title_keywords == ['']:
        title_keywords = None
    print(title_keywords)

    desc_keywords = request.form.get('desc_keywords').split("\n")
    if desc_keywords == ['']:
        desc_keywords = None
    print(desc_keywords)


    # kw_search = YoutubeVideoData(API_KEY, query, order, min_subscriber_count, max_subscriber_count, next_page_token)
    channel_data, tokens = kw_search.get_youtube_data(query, min_subscriber_count, max_subscriber_count, search_type, title_keywords, desc_keywords)

    return jsonify({"channels":channel_data, "tokens": tokens})
    

@app.route('/api/add_list', methods=["POST"])
@login_required
def create_new_list():
    
    list_title = request.form.get("list_title")
    user_id = current_user.user_id 

    crud.create_list(user_id, list_title)

    return list_title

# @app.route('/api/add_influencer', methods=["POST"])
# def add_new_influencer():

#     # list_id = #need to get the list ID of the list that is selected in the dropdown
    
#     # add_influencer():

@app.route('/api/add_influencer', methods=["POST"])
def add_influencer():
    title = request.form.get("list_title")
    # row_data = request.form.getlist("row_data[]")
    
    channel_title = request.form.get("row_data[title]")
    channel_desc = request.form.get("row_data[description]")
    video_count = request.form.get("row_data[video_count]")
    view_count = request.form.get("row_data[view_count]")
    subscriber_count = request.form.get("row_data[sub_count]")
    email = request.form.get("row_data[email]")
    URL = request.form.get("row_data[link]")

    crud.add_influencer(current_user.user_id, title, channel_title, channel_desc, subscriber_count, video_count, view_count, email, URL)

    return jsonify(success=True)

@app.route('/api/remove_influencer', methods=["POST"])
def remove_influencer():
    list_title = request.form.get("list_title")
    channel_title = request.form.get("channel_title")

    crud.remove_influencer(current_user.user_id, list_title, channel_title)

    return jsonify(success=True)

@app.route('/api/contacted', methods=["POST"])
def mark_contacted():
    list_title = request.form.get("list_title")
    channel_title = request.form.get("channel_title")

    crud.mark_contacted(current_user.user_id, list_title, channel_title)

    return jsonify(success=True)

@app.route('/api/enrich', methods =["POST"])
def enrich_profiles():
    channel_titles = request.form.get("channel_titles")
    print(channel_titles)
    channel_obj = json.loads(channel_titles)
    print(channel_obj[0]["title"])
    print((channel_obj[0]["title"].replace(" ","+")))
    print(channel_obj)

    instagram_data = scraping.scrape_yahoo(channel_obj)
    print(instagram_data)

    # instagram_data = jsonify([{'title': 'Dr Dray', 'ig_username': 'drdrayzday', 'ig_followers': '228.8k'}, {'title': 'All Things Adrienne', 'ig_username': 'allthingsadriennehoughton', 'ig_followers': '294.1k'}, {'title': 'SACHEU', 'ig_username': 'sacheu', 'ig_followers': '287.8k'}])

    return jsonify(instagram_data)



@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/auth/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = crud.get_user_by_email(email)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect('/login') # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    return redirect('/profile')


@app.route('/signup')
def show_signup():
    return render_template('signup.html')

@app.route('/auth/signup', methods=['POST'])
def signup():

    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    user = crud.get_user_by_email(email)

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect('/signup')

    crud.create_user(email, generate_password_hash(password, method='sha256'), first_name, last_name)

    return render_template('profile.html', name=first_name)

@app.route('/profile')
@login_required
def profile():
    list_count = crud.count_total_lists(current_user.user_id)
    print(f'THE LIST COUNT IS {list_count}')
    inf_count = crud.count_total_influencers_saved(current_user.user_id)
    print(current_user.email)

    return render_template('profile.html', name=current_user.email, list_count=list_count, inf_count=inf_count)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)

    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.init_app(app)

    from model import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.run(debug=True, host='0.0.0.0')

