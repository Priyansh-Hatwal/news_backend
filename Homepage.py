from requests_html import HTMLSession
import json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://tikuhatwal:FHHP2KnoMZRqQU6G@cluster0.sg0rs.mongodb.net') 
db = client['news_database']  
collection = db['news_collection'] 

session = HTMLSession()

url = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen'
r = session.get(url)

r.html.render(sleep=2, scrolldown=2) 

articles = r.html.find('article')

news_items = []
max_articles = 100  
count = 0 

for item in articles:
    if count >= max_articles:
        break  
    try:
        a_tags = item.find('a')
        div_tags = item.find('div')
        figure_tag = item.find('figure')
        figure = ""
        if figure_tag:
            figure = figure_tag[0].find('img', first=True).attrs.get('src')
            if not figure.startswith('http'):
                figure = f'https://news.google.com{figure}'
        if len(a_tags) > 1:  
            first_a_tag = a_tags[1]
            title = first_a_tag.text
            link = first_a_tag.attrs.get('href')
            if not link.startswith('http'):
                link = f'https://news.google.com{link}'
            img = ""
            channel = ""
            if len(div_tags) > 1:
                channel_divs = div_tags[1].find('div')
                if len(channel_divs) > 0:
                    img_tag = channel_divs[0].find('img', first=True)
                    if img_tag:
                        img = img_tag.attrs.get('src', '')

                if len(channel_divs) > 1:
                    channel = channel_divs[1].text
            news_item = {
                "title": title,
                "link": link,
                "channel": channel,
                "image": img,
                "figure": figure,
                "scraped_at": datetime.utcnow()  
            }
            existing_article = collection.find_one({"link": link})
            if not existing_article:
                news_items.append(news_item)
                count += 1 

    except IndexError:
        news_items.append({"error": "IndexError - Possibly missing elements"})
    except Exception as e:
        news_items.append({"error": str(e)})

if news_items:
    collection.insert_many(news_items)  
    print(f"{len(news_items)} new news items inserted into MongoDB.")
session.close()
client.close()
print("Data has been saved to MongoDB.")
