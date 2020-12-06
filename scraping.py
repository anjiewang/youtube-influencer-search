import requests
import json
import re
import os
from bs4 import BeautifulSoup

"""Scrape Yahoo search results for the Instagram username and Follower count"""

def create_yahoo_url(channel_list):
    """Create the yahoo search URL from the channel title"""

    urls = []

    for channel in channel_list:
        url = "https://search.yahoo.com/search?p=" + channel["title"].replace(" ", "+") + "&fr2=sb-top&fp=1&nojs=1"
        urls.append(url)

    return urls

def scrape_yahoo(channel_list, retries=3):
    "Scrape the first page of a Yahoo search and parse HTML"""

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
                username = re.findall("(?<=@)(.+?)(?=\))", str_item)
                username = "".join(username).strip('<b>/')
                channel_list[count]["ig_username"] = username
                channel_list[count]["ig_followers"] = followers
            else:
                channel_list[count].setdefault("ig_username",)
                channel_list[count].setdefault("ig_followers",)
        count += 1


        
    return channel_list
                

