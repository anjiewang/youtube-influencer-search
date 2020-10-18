import requests
import json

class YoutubeVideoData:

    def __init__(self, api_key, query, order, published_after, published_before):
        self.api_key = api_key
        self.query = query
        self.order = order
        self.video_ids = None
        self.published_after = published_after
        self.published_before = published_before

    
    def get_youtube_data(self):
        search_url = "https://www.googleapis.com/youtube/v3/search"
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        
        search_params = {
            "part" : "snippet",
            "type" : "video",
            "q" : self.query,
            "key" : self.api_key,
            "order" : self.order,
            "publishedBefore" : self.published_before,
            "publishedAfter" : self.published_after
        }

        request = requests.get(search_url, params=search_params)
        data = json.loads(request.text)
        channel_ids = []
        for item in data["items"]:
            channel_ids.append(item["snippet"]["channelId"])


        channel_params = {
            "part" : "snippet,statistics,contentOwnerDetails,topicDetails",
            "key" : self.api_key,
            "id" : ",".join(channel_ids)
        }

        request = requests.get(channel_url, params=channel_params)
        channel_data = json.loads(request.text)
    
        channel_list = []    
        for item in channel_data["items"]:
            channel_dict = {
            "id" : item["id"],
            "title" : item["snippet"]["title"],
            "description" : item["snippet"]["description"],
            "view_count" : item["statistics"]["viewCount"],
            "subscriber_count" : item["statistics"]["subscriberCount"],
            "video_count" : item["statistics"]["videoCount"],
            "published_date" : item["snippet"]["publishedAt"],
            "url" : "youtube.com/channel/" + item["id"]
            }
            channel_list.append(channel_dict)


        return channel_list

