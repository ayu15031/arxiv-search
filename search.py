
import urllib.request
import feedparser
import json
from time import sleep
from datetime import datetime, timedelta

# Base api query url
base_url = 'http://export.arxiv.org/api/query?'

# Search parameters
search_query = 'cat:cs.LG'  # search for electron in all fields
start = 50000                     # retreive the first 5 results
max_results = 500

query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
                                                     start,
                                                     max_results)

response = urllib.request.urlopen(base_url+query).read()

date_string = "21-05-1999"


date_object = datetime.strptime(date_string, "%d-%m-%Y")
next_date = date_object + timedelta(days=1)


while True:
    # query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
    #                                                      start,
    #                                                      max_results)
    query = f"search_query={search_query}+AND+submittedDate:[{date_object.year}{date_object.strftime('%m')}{date_object.strftime('%d')}2000+TO+{next_date.year}{next_date.strftime('%m')}{next_date.strftime('%d')}2000]"

    response = urllib.request.urlopen(base_url+query).read()
    feed = feedparser.parse(response)
    if len(feed.entries) == 0:
        print(f'sleeping... for query {query}')
        sleep(10)
        date_object = next_date 
        next_date = date_object + timedelta(days=1)
        continue

    print(date_object)

    with open(f"filtered_papers/{date_object.year}/{date_object.strftime('%m')}/{date_object.strftime('%d')}.json", "w") as outfile:
        json.dump(feed, outfile)

    date_object = next_date 
    next_date = date_object + timedelta(days=1)

# print out feed information
