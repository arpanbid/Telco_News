#!/usr/bin/env python
# coding: utf-8

# # Update the CSV file with news till today date. 

# In[25]:


import datetime 
import requests
import json
import pandas as pd


# In[26]:

news_added = -1

df = pd.read_csv("News.csv") #read csv
df["date"] = df["date"].str[:10] #take out date from date column
df['date'] = pd.to_datetime(df['date']) #convert to date format
min_date = df['date'].min()
last_updated = df['date'].max()
count = len(df)
print("Total news available in the CSV file: " + str(count))


# In[27]:


# Get today's date
today = datetime.date.today()

# Format the dates as strings in "yyyy-mm-dd" format
today_str = today.strftime("%Y-%m-%d")+"T09:51:05.251Z"
last_updated = last_updated.strftime("%Y-%m-%d")+'T09:51:05.251Z'



# In[28]:

a = datetime.datetime.strptime(last_updated[:10], '%Y-%m-%d').date()
b=today-a
if b.days>1:  
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.telecompaper.com',
        'Referer': 'https://www.telecompaper.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'X-Request-Language': 'en',
        'X-VISITOR-ID': '141428',
        'accept': '*/*',
        'content-type': 'application/json',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'operationName': None,
        'variables': {
            'where': {
                'useTypesense': False,
                'text': '',
                'contentTypeGroupIds': [],
                'editionIds': [],
                'countryId': None,
                'tags': [],
                'perPage': 70000,
                'page': 1,
                'sortBy': 'date:desc',
                'languageId': 1,
                'queryBy': ['TITLE', 'FULLTEXT', 'COMPANY',],
                'articleId': None,
                'date': None,
                'direction': 'BACKWARD',
                'startAt': last_updated,
                'endAt': today_str,
            },
        },
        'query': 'query ($where: ArticleSearchWhereInput) {\n  searchArticles(where: $where) {\n    id\n    externalId\n    date\n    title\n    slug\n    redirectUrl\n    abstract\n    edition {\n      id\n      name\n      __typename\n    }\n    country {\n      id\n      name\n      __typename\n    }\n    region {\n      id\n      name\n      __typename\n    }\n    contentType {\n      id\n      name\n      colour\n      contentTypeGroup {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    response = requests.post('https://telecompaper-api-abduz5l4ya-ez.a.run.app/graphql', headers=headers, json=json_data)


    # In[29]:


    print(response)


    # In[30]:


    resp = str(response.content)
    #resp = resp.replace('b'{"data":{"searchArticles":', '')
    resp = resp[28:-3]
    #print(resp)
    json_data = json.loads(resp)

    trimmed_json_data = [{key: value for key, value in item.items() if key in ['date', 'title', 'abstract', 'slug', 'country']} for item in json_data]

    new_df = pd.json_normalize(trimmed_json_data)
    new_df.head()


    # In[31]:


    if len(df) == 70000:
        print("Error: Too many news.")
    else:
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv("News.csv")
        new_count = len(df)
        news_added = new_count - count
        print("Updated\n\nTotal news available in the CSV file: " + str(new_count))


