from flask import Flask, render_template, request, jsonify
import requests
import json
from youtube import YoutubeVideoData
from datetime import date

app = Flask(__name__)

API_KEY = "AIzaSyB7gBd3yJ6to16PESYfMIcgbf4eP2l60OI"

@app.route('/')
def index():
    return render_template("main.html")


@app.route('/api/search')
def youtube_video_search():
    query = request.args.get("keywords")

    published_after = request.args.get("published_after") + "T00:00:00-08:00"
    if published_after == "T00:00:00-08:00":
        published_after = "2000-01-01T00:00:00-08:00"

    published_before = request.args.get("published_before") + "T00:00:00-08:00"
    if published_before == "T00:00:00-08:00":
        published_before = str(date.today()) + "T00:00:00-08:00"
    print(published_before)
    
    order = request.args.get("order")
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


    
    kw_search = YoutubeVideoData(API_KEY, query, order, published_after, published_before)
    channel_data = kw_search.get_youtube_data()
    
    return jsonify({"channels":channel_data})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

