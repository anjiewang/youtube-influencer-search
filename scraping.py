# import requests
# import json
# import re
# from bs4 import BeautifulSoup


# def create_yahoo_url(channel_list):
#     urls = []
    
#     for channel in channel_list:
#         channel_name = channel["title"].split(" ")
#         url = "https://search.yahoo.com/search?p=" + ("+").join(channel_name) + "&fr2=sb-top&fp=1&nojs=1"
#         urls.append(url)

#     print(urls)

# def scrape_yahoo(urls, channel_list):
#     api_url = "http://api.scraperapi.com"

#     for url in urls:
#         params = {"api_key": "512c1171369bae18a23e30a62390a36c",
#                   "url": url}
    
#         response = requests.get(api_url, params=params)
#         result = BeautifulSoup(response.content, "html.parser")
#         print(result.prettify())
#         webpages = result.select('h3')
#         print(webpages)
#         instagram = re.findall("www.instagram.com", str(webpages))
#         print(instagram)
#         instagram_followers = webpages.find_all(class_="fz-ms lh-1_43x")
#         print(instagram_followers)
#         followers = re.findall("Followers", str(instagram_followers))
#         print(instagram_followers)
#         print(followers)
#         print(instagram)



# #urls: ['https://search.yahoo.com/search?p=hyram&fr2=sb-top&fp=1&nojs=1']
# #channel_list: [{"title":"hyram"}]

import requests
import json
import re
import os
from bs4 import BeautifulSoup


def create_yahoo_url(channel_list):
    urls = []

    for channel in channel_list:
        url = "https://search.yahoo.com/search?p=" + channel["title"].replace(" ", "+") + "&fr2=sb-top&fp=1&nojs=1"
        urls.append(url)

    return urls

def scrape_yahoo(channel_list, retries=3):

    urls = create_yahoo_url(channel_list)

    api_url = "http://api.scraperapi.com"

    count = 0
    for url in urls:
        print(url)
        params = {"api_key": os.environ['SCRAPING_KEY'],
                  "url": url}

        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            result = BeautifulSoup(response.content, "html.parser")
            instagram_search = result.select('p.fz-ms.lh-1_43x')
        else:
            while retries > 0:
                retries -= 1
                response = requests.get(api_url, params=params)
                if response.status_code == 200:
                    result = BeautifulSoup(response.content, "html.parser")


        for item in instagram_search:
            str_item = str(item)
            if re.search("See Instagram photos", str_item):
                followers = re.findall("(?<=\>)(.*?)(?=\ F)",str_item)
                followers = "".join(followers)
                print(followers)
                username = re.findall("(?<=@)(.+?)(?=\))", str_item)
                username = "".join(username).strip('<b>/')
                print(username)
                channel_list[count]["ig_username"] = username
                channel_list[count]["ig_followers"] = followers
            else:
                channel_list[count].setdefault("ig_username",)
                channel_list[count].setdefault("ig_followers",)
        count += 1


        
    return channel_list
                

