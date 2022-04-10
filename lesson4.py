from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news']
lenta = db.lenta

url = 'https://lenta.ru/'
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/100.0.4896.75 Safari/537.36'}

response = requests.get(url, headers=header)

dom = html.fromstring(response.text)

news_list = dom.xpath("//div[@class='topnews']//a[contains(@class,'_topnews')]")

news = []
for new in news_list:
    topnews = {}

    name = new.xpath(".//../text()")[0]
    link = str(new.xpath(".//../@href")[0])

    response = requests.get(url + link, headers=header)
    dom = html.fromstring(response.text)
    date = dom.xpath("//time[contains(@class, 'topic-header__time')]/text()")

    topnews['source'] = url
    topnews['name'] = name
    topnews['link'] = url + link
    topnews['date'] = date

    news.append(topnews)

for new in news:
    if lenta.find_one({'link': new['link']}):
        print(f"Новость по ссылке {new['link']} уже существует в базе данных")
    else:
        lenta.insert_one(new)



