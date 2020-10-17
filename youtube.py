import requests
import json

class YoutubeVideoData:

    def __init__(self, api_key, query, max_results, order, published_after, published_before):
        self.api_key = api_key
        self.query = query
        self.max_results = max_results
        self.order = order
        self.video_ids = None
        self.published_after = published_after
        self.published_before = published_before

    
    def get_youtube_videos(self):
        url = "https://www.googleapis.com/youtube/v3/search?"
        params = {
            "part" : "snippet",
            "type" : "video",
            "q" : self.query,
            "key" : self.api_key,
            "maxResults" : self.max_results,
            "order" : self.order,
            "publishedBefore" : self.published_before,
            "publishedAfter" : self.published_after
        }

        request = requests.get(url, params=params)
        data = json.loads(request.text)
        video_ids = []
        for item in data["items"]:
            video_ids.append(item["id"]["videoId"])
        return video_ids

        # url = f'''https://www.googleapis.com/youtube/v3/search?
        #         part=snippet
        #         &type=video
        #         &q={self.query}
        #         &key={self.api_key}
        #         &maxResults={self.max_results}'''

        # print(url)
        # json_url = requests.get(url)
        # data = json.loads(json_url.text)
        # video_ids = []
        # for item in data["items"]:
        #     video_ids.append(item["id"]["videoId"])
        # return video_ids

    # def dump(self):
    #     if self.video_ids is None:
    #         return 
    #     else:
    #         video_ids = " " #TODO: get video id from data