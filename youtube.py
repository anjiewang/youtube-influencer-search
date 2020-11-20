import requests
import json
import re
from filters import filter_by_subs

class YoutubeVideoData:

    def __init__(self, api_key, query = None, order = None, min_subscriber_count = None, max_subscriber_count = None, next_page_token = None, title_keywords = None, desc_keywords = None):
        self.api_key = api_key
        self.query = query
        self.order = order
        self.channel_ids = set()
        self.next_page_token = next_page_token
        self.min_subscriber_count = min_subscriber_count
        self.max_subscriber_count = max_subscriber_count
        self.title_keywords = title_keywords
        self.desc_keywords = desc_keywords
        #store channels 



    def filter_by_subs(self, channel):    
        if int(self.min_subscriber_count) < int(channel["subscriber_count"]) < int(self.max_subscriber_count):
            return True

    def check_title(self, channel):
        if self.title_keywords == None:
            return True

        for keyword in self.title_keywords:
            if keyword.lower() in channel["title"].lower():
                return False
        return True 

    def check_desc(self, channel):
        if self.desc_keywords == None:
            return True

        for keyword in self.desc_keywords:
            if keyword.lower() in channel["description"].lower():
                return False
        return True

    def check_channels(self, channel_list):
        filtered_channels = []

        for channel in channel_list:
            if self.filter_by_subs(channel) and self.check_title(channel) and self.check_desc(channel):
                filtered_channels.append(channel)

        return filtered_channels
        

    def get_emails(self, filtered_channels):
        for channel in filtered_channels:
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", channel["description"])
            channel["email"] = emails

        return filtered_channels

    
    def get_youtube_data(self, query, min_subscriber_count, max_subscriber_count, search_type, title_keywords, desc_keywords):
        self.query = query
        self.min_subscriber_count = min_subscriber_count
        self.max_subscriber_count = max_subscriber_count
        self.title_keywords = title_keywords
        self.desc_keywords = desc_keywords

        search_url = "https://www.googleapis.com/youtube/v3/search"
        channel_url = "https://www.googleapis.com/youtube/v3/channels"

        channel_list = []
        second_set = set()
        count = 0
        
        while count < 10:

            print(f'count is {count}')
            if search_type == "Video URL":
                search_params = {
                    "part" : "snippet",
                    "type" : "video",
                    "relatedToVideoId" : self.query,
                    "key" : self.api_key,
                    "maxResults" : 10,
                    "relevanceLanguage" : "EN",
                    "pageToken" : self.next_page_token
                }
            else:
                search_params = {
                    "part" : "snippet",
                    "type" : "video",
                    "q" : self.query,
                    "key" : self.api_key,
                    "order" :"relevance",
                    "maxResults" : 10,
                    "relevanceLanguage" : "EN",
                    "pageToken" : self.next_page_token
                }

            request = requests.get(search_url, params=search_params)
            data = json.loads(request.text)

            self.next_page_token = data['nextPageToken']
        
            for item in data["items"]:
                second_set.add(item["snippet"]["channelId"])

            channel_params = {
                "part" : "snippet,statistics,contentOwnerDetails,topicDetails",
                "key" : self.api_key,
                "id" : ",".join(second_set.difference(self.channel_ids)),
                "maxResults" : 50
            }

            request = requests.get(channel_url, params=channel_params)
            channel_data = json.loads(request.text)

            for item in second_set:
                self.channel_ids.add(item)
            
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

                # filtered_channels = filter_by_subs(channel_list, self.min_subscriber_count, self.max_subscriber_count)


            filtered_channels = self.check_channels(channel_list)
            print(filtered_channels)
                
            count = len(filtered_channels)
            print(f'now the count is {count}')

        # import pdb
        # pdb.set_trace()
        
        final_channels = self.get_emails(filtered_channels)

        #variable to count how close I am to 50
        #if variable < 50 call the API again

        return final_channels, tokens
        

