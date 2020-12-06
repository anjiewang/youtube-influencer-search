# Youtube Influencer Search Engine

The Youtube Influencer Search Engine is a tool that allows users to query the Youtube API for channels related to a particular topic or video which can then be saved, enriched, and exported in a personal dashboard. 

## Key Features

- Search for relevant channels by Keyword or Video URL
- Filter out irrelevant Channel Titles or Descriptions 
- Filter by a minimum or maximum number of subscribers
- Export results to CSV
- Create an account and save lists of influencers to a personal dashboard 
- Enrich Youtube channel data with scraped Instagram username and follower counts
- Organize influencers in the dashboard by starring or marking as contacted

## Site

###### **Landing Page**
![Landing Page](/demo/landing_page.gif)
\
\
###### **Run a Search**
![Search](/demo/search.gif)
\
\
###### **Results**
![Results](/demo/results.gif)
\
\
###### **Create Lists & Save Influencers**
![Create](/demo/create_list.gif)
\
\
###### **Export to CSV**
![CSV](/demo/csv.png)
\
\
###### **User Dashboard**
![Dashboard](/demo/dashboard.gif)
\
\
###### **Enrich Profiles**
![Enrich](/demo/enrich.gif)
\
\
###### **Star / Mark as Contacted**
![Contact](/demo/contact.gif)

## Enrich Profiles Scraping
The enrich profiles feature allows users to augment Youtube channel information with Instagram usernames and follower counts by scraping the HTML of the first page of a Yahoo Search for the channel name. The HTML is parsed using Python's BeautifulSoup library for the Instagram username and follower count. 
\
![Scrape](/demo/yahoo_search.png)


## Tech Stack

- Flask / Jinja
- jQuery / Ajax
- Youtube Data API
- Scraper API
- Python BeautifulSoup
- Boostrap 
- Postgres DB / SqlAlchemy




