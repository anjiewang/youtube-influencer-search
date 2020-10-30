from flask import Flask, render_template, request, jsonify, redirect, flash
import requests
import json
from youtube import YoutubeVideoData
from datetime import date
import sys
import crud
import re
from model import connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'

API_KEY = "AIzaSyB7gBd3yJ6to16PESYfMIcgbf4eP2l60OI"

kw_search = YoutubeVideoData(API_KEY)


@app.route('/')
def index():

    lists = crud.get_list_by_user(current_user.user_id)

    return render_template('main.html', lists=lists)


@app.route('/api/search', methods=["POST"])


def youtube_video_search():

    query = request.form.get("keywords") #TODO: create a list to split keywords and loop through; can also jsonify the string 

    # published_after = request.form.get("published_after") + "T00:00:00-08:00"
    # if published_after == "T00:00:00-08:00":
    #     published_after = "2000-01-01T00:00:00-08:00"

    # published_before = request.form.get("published_before") + "T00:00:00-08:00"
    # if published_before == "T00:00:00-08:00":
    #     published_before = str(date.today()) + "T00:00:00-08:00"
    # print(published_before)
    
    order = request.form.get("order")
    if order == "Relevancy":
        order = "relevance"
    elif order == "Most Recently Published":
        order = "date"
    elif order == "Rating (Highest to Lowest)":
        order = "rating"
    elif order == "View Count (Highest to Lowest)":
        order = "viewCount"
    
    # max_results = request.args.get("max_results")
    # if max_results == "":
    #     max_results = 25

    min_subscriber_count = request.form.get("min_subscriber_count")
    if min_subscriber_count == "":
        min_subscriber_count = 0

    max_subscriber_count = request.form.get("max_subscriber_count")
    if max_subscriber_count == "":
        max_subscriber_count = sys.maxsize

    # next_page_token = request.form.get("next_page_token")


    # kw_search = YoutubeVideoData(API_KEY, query, order, min_subscriber_count, max_subscriber_count, next_page_token)
    channel_data, tokens = kw_search.get_youtube_data(query, order, min_subscriber_count, max_subscriber_count)

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

    user = crud.get_user_by_email(email)

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect('/signup')

    crud.create_user(email, generate_password_hash(password, method='sha256'))

    return render_template('profile.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.email)

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

