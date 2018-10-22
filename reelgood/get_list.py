import json

import requests
from database import Database
# header =

db = Database()
db.connect()


def handle_json_list(dict_json_list):
    for item in dict_json_list:
        record ={}
        for (key , value) in item.items():
            if key == 'sources':
                if 'amazon_prime' in value:
                    record["reelgood_is_amazon"] = 1
                if 'hulu_plus' in value:
                    record["reelgood_is_hulu"] = 1
                if 'netflix' in value:
                    record["reelgood_is_netflix"] = 1
            else:
                record["reelgood_" + key] = value
        db.insert_dict(record , 'reelgood')
        print(record)

def request_api(sources , current_num):
    header = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
              "accept-encoding": "gzip, deflate, br",
              "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
              "cache-control": "max-age=0",
              "cookie": "__cfduid=ddf713f3086a15b99079279c9894053a41539659152; _ga=GA1.2.1326966066.1539659153; _gid=GA1.2.50556354.1539843566; mp_1215522eade2a5ccbab3b079ca9fb735_mixpanel=%7B%22distinct_id%22%3A%20%221668b7b842a265-040d9a1bc94514-346a7809-1aeaa0-1668b7b842b484%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D",
              "upgrade-insecure-requests": "1",
              "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    url = 'https://api.reelgood.com/v2/browse/source/' + sources + '?availability=onSources&skip=' + str(
        current_num) + '&take=250&content_kind=movie&free=false&hide_seen=false&hide_tracked=false&hide_watchlisted=false&imdb_end=10&imdb_start=0&override_user_sources=true&overriding_free=false&overriding_sources=hulu&rt_end=100&rt_start=0&sort=0&year_end=2018&year_start=1900'
    all_movie_url = 'https://api.reelgood.com/v2/browse/filtered?availability=onSources&content_kind=movie&free=false&hide_seen=false&hide_tracked=false&hide_watchlisted=false&imdb_end=10&imdb_start=0&rt_end=100&rt_start=0&skip=' + str(
        current_num) + '&sort=0&take=50&year_end=2018&year_start=1900'
    r = requests.get(url)
    json_text = r.content.decode()
    # 将json字符串转换成dic字典对象
    dict_json_list = json.loads(json_text)
    return dict_json_list

sources_list = ['hulu' , 'amazon' , 'netflix']
for sources in sources_list:
    print('now crawling .......{}'.format(sources))
    current_num = 0
    dict_json_list = request_api(sources , current_num)
    handle_json_list(dict_json_list)
    while(len(dict_json_list) > 0):
        current_num += 250
        dict_json_list = request_api(sources, current_num)
        handle_json_list(dict_json_list)

db.close()