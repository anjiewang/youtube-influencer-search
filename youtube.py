import requests
import json
from filters import filter_by_subs

class YoutubeVideoData:


    def __init__(self, api_key, query, order, published_after, published_before, min_subscriber_count, max_subscriber_count):
        self.api_key = api_key
        self.query = query
        self.order = order
        self.channel_ids = set()
        self.published_after = published_after
        self.published_before = published_before
        self.previous_page_token = None
        self.next_page_token = None  #TODO: how to persist the next_page_token
        self.min_subscriber_count = min_subscriber_count
        self.max_subscriber_count = max_subscriber_count

    
    def get_youtube_data(self):
        # for keyword in self.query.split(", "): #TODO: where to put this for loop to loop through the keywords
        
        search_url = "https://www.googleapis.com/youtube/v3/search"
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        
        search_params = {
            "part" : "snippet",
            "type" : "video",
            "q" : self.query,
            "key" : self.api_key,
            "order" : self.order,
            "publishedBefore" : self.published_before,
            "publishedAfter" : self.published_after,
            "maxResults" : 50,
            "relevanceLanguage" : "EN"
        }

        request = requests.get(search_url, params=search_params)
        data = json.loads(request.text)
        print(data)

        self.next_page_token = data['nextPageToken']
        print(self.next_page_token)

        self.channel_ids = set() #TODO: trying to figure out how to get only unique channel_ids to add to the table

        for item in data["items"]:
            self.channel_ids.add(item["snippet"]["channelId"])
        
        print(self.channel_ids)


        channel_params = {
            "part" : "snippet,statistics,contentOwnerDetails,topicDetails",
            "key" : self.api_key,
            "id" : ",".join(self.channel_ids),
            "maxResults" : 50
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
            "subscriber_count" : item.get("statistics",{}).get("subscriberCount",0), #TODO: how to handle if no subscribers are returned
            "video_count" : item["statistics"]["videoCount"],
            "published_date" : item["snippet"]["publishedAt"],
            "url" : "https://www.youtube.com/channel/" + item["id"]
            }
            channel_list.append(channel_dict)

        filtered_channels = filter_by_subs(channel_list, self.min_subscriber_count, self.max_subscriber_count)


        return filtered_channels
        

