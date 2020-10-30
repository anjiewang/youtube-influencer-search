import requests
import json
from filters import filter_by_subs

class YoutubeVideoData:

    def __init__(self, api_key, query = None, order = None, min_subscriber_count = None, max_subscriber_count = None, next_page_token = None):
        self.api_key = api_key
        self.query = query
        self.order = order
        self.channel_ids = set()
        self.next_page_token = next_page_token
        self.min_subscriber_count = min_subscriber_count
        self.max_subscriber_count = max_subscriber_count

    
    def get_youtube_data(self, query, order, min_subscriber_count, max_subscriber_count):
        # for keyword in self.query.split(", "): #TODO: where to put this for loop to loop through the keywords
        
        self.query = query
        self.order = order
        self.min_subscriber_count = min_subscriber_count
        self.max_subscriber_count = max_subscriber_count

        search_url = "https://www.googleapis.com/youtube/v3/search"
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        
        search_params = {
            "part" : "snippet",
            "type" : "video",
            "q" : self.query,
            "key" : self.api_key,
            "order" : self.order,
            "maxResults" : 5,
            "relevanceLanguage" : "EN",
            "pageToken" : self.next_page_token
        }
        print(search_params)

        request = requests.get(search_url, params=search_params)
        data = json.loads(request.text)

        self.next_page_token = data['nextPageToken']
        print(self.next_page_token)
    
        second_set = set()
        for item in data["items"]:
            second_set.add(item["snippet"]["channelId"])

        print(second_set)

        channel_params = {
            "part" : "snippet,statistics,contentOwnerDetails,topicDetails",
            "key" : self.api_key,
            "id" : ",".join(second_set.difference(self.channel_ids)),
            "maxResults" : 50
        }

        print(channel_params)

        request = requests.get(channel_url, params=channel_params)
        channel_data = json.loads(request.text) 

        for item in second_set:
            self.channel_ids.add(item)
        print(self.channel_ids)
    
        channel_list = []
        
        for item in channel_data["items"]:
            channel_dict = {
            "id" : item["id"],
            "title" : item["snippet"]["title"],
            "description" : item["snippet"]["description"],
            "view_count" : item["statistics"]["viewCount"],
            "subscriber_count" : item.get("statistics",{}).get("subscriberCount",0),
            "video_count" : item["statistics"]["videoCount"],
            "published_date" : item["snippet"]["publishedAt"],
            "url" : "https://www.youtube.com/channel/" + item["id"],
            }
            channel_list.append(channel_dict)
        

        tokens = {"nextPageToken" : data["nextPageToken"]}

        filtered_channels = filter_by_subs(channel_list, self.min_subscriber_count, self.max_subscriber_count)

        #variable to count how close I am to 50
        #if variable < 50 call the API again


        return filtered_channels, tokens
        

