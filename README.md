# Youtube Influencer Search Engine

The Youtube Influencer Search Engine allows users to query the Youtube API for channels related to a particular topic or video which can then be saved, enriched, and exported in a personal dashboard. 

## Key Features

- Search for relevant channels by keyword or video URL
- Filter out irrelevant channel titles or descriptions 
- Filter by a minimum or maximum number of subscribers
- Export results to CSV
- Create an account and save lists of influencers to a personal dashboard 
- Scrape Instagram username and follower counts for Youtube channels
- Organize influencers in the dashboard by starring or marking as contacted

## Site

### **Landing Page**
![Landing Page](/demo/landing_page.gif)


### **Search**
![Search](/demo/search.gif)


### **Results**
![Results](/demo/results.png)


### **Create Lists & Save Influencers**
![Create](/demo/create_list.gif)


### **Export to CSV**
![CSV](/demo/csv.png)


### **User Dashboard**
![Dashboard](/demo/dashboard.gif)


### **Enrich Profiles**
![Enrich](/demo/enrich.gif)


<!-- ### **Star / Mark as Contacted**
![Contact](/demo/contact.gif) -->

## Enrich Profiles Scraping
The enrich profiles feature allows users to augment Youtube channel statistics with Instagram usernames and follower counts by scraping the HTML of the first page of a Yahoo Search for the channel name. The HTML is parsed using Python's BeautifulSoup library for the Instagram username and follower count. 
\
\
![Scrape](/demo/yahoo_search.png)


## Tech Stack

- [Youtube Data API](https://developers.google.com/youtube/v3/docs)
- [ScraperAPI](https://www.scraperapi.com/)
- [Python Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Bootstrap 4.0](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
- Flask / Jinja
- jQuery / Ajax
- Postgres DB / SqlAlchemy




