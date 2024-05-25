from bs4 import BeautifulSoup
import requests
import pandas as pd

data=[]
count = 0

def read_links():
    a=[]
    f = open("Data/dev_telecom_urls.txt", "r")
    #print(f.readlines())
    for line in f:
        a.append(str(line.strip()))
    return(a)

def developingtelecoms_scrap(path):
  baseURL="https://developingtelecoms.com"
  URL=baseURL + path
  print("Fetching: ", URL)
  
  headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate',
    'Host': 'developingtelecoms.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
    #'Referer': 'https://developingtelecoms.com/regions/sub-saharan-africa-telecommunications.html',
    'Connection': 'keep-alive',
  }

  try:
    source = requests.get(URL, headers=headers)
    soup = BeautifulSoup(source.text,'html.parser')
    heading = soup.find_all('h2', class_="article-title")
    date = soup.find_all('dd', class_="published")
    content = soup.find_all('section', class_="article-intro clearfix") 

    i=0
    while i<50:
      item={}


      title=heading[i].text
      #title=title.strip().rsplit("\t\n")[1]
      item["Title"] = title.strip()

      abstract=content[i].text
      item["Abstract"] = abstract.strip()

      


      Date=date[i].text
      #Date=Date.strip().rsplit("Created on ")[1]
      item["Date"] = Date.strip() 

      li=heading[i].find(href=True)
      item["Links"]=baseURL+li['href']

      data.append(item)
      i+=1

  except Exception as e:
    print("Error ", e)


from time import sleep

links = read_links()

for link in links:
    developingtelecoms_scrap(link)
    sleep(5)

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'], format="mixed")


cur_data = pd.read_csv("Data/dev_news_date_1.csv")
last_updated = cur_data["Date"].max()
filtered_df = df[df["Date"]>last_updated]
count = len(filtered_df)



h=pd.concat([cur_data, filtered_df], ignore_index = True)
h.to_csv("Data/dev_news_date_1.csv", index=False) #for safer side, create another version of the file

print("Update Success!" + "\n" + str(count) + " news Added")

#End here