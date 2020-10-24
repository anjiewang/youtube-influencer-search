from flask import Flask, render_template, request, jsonify
import requests
import json
from youtube import YoutubeVideoData
from datetime import date
import sys


app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

