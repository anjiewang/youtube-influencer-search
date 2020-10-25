from flask import Flask, render_template, request, jsonify, redirect
import requests
import json
from youtube import YoutubeVideoData
from datetime import date
import sys
import crud
from model import connect_to_db
from werkzeug.security import generate_password_hash


app = Flask(__name__)

# app.config['SECRET_KEY'] = 'secret-key-goes-here'

API_KEY = "AIzaSyB7gBd3yJ6to16PESYfMIcgbf4eP2l60OI"

@app.route('/')
def index():
    return render_template("main.html")


@app.route('/api/search', methods=["POST"])
def youtube_video_search():
    query = request.form.get("keywords") #TODO: create a list to split keywords and loop through; can also jsonify the string 

    published_after = request.form.get("published_after") + "T00:00:00-08:00"
    if published_after == "T00:00:00-08:00":
        published_after = "2000-01-01T00:00:00-08:00"

    published_before = request.form.get("published_before") + "T00:00:00-08:00"
    if published_before == "T00:00:00-08:00":
        published_before = str(date.today()) + "T00:00:00-08:00"
    print(published_before)
    
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


    kw_search = YoutubeVideoData(API_KEY, query, order, published_after, published_before, min_subscriber_count, max_subscriber_count)
    channel_data = kw_search.get_youtube_data()

    return jsonify({"channels":channel_data})

@app.route('/api/add_list', methods=["POST"])
def create_new_list():
    
    list_title = request.form.get("list_title")
    user_id = request.form.get("user_id") #TODO: change this to email!

    new_list = crud.create_list(user_id, list_title)

    return new_list

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/show_signup')
def show_signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        return render_template('login.html')

    crud.create_user(email, generate_password_hash(password, method='sha256'))

    return render_template('profile.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')

