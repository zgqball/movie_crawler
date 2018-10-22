import copy
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from mc.MC_crawler import Database

def count_star(item):
    #para:item soup of comment
    #return star num
    score = 0
    comment_detail = item.find('div' , {"class" : "col-xs-16"})
    if comment_detail.contents[1].name == 'img':
        #no interested or want to see
        score = 0
    else:
        # half
        if comment_detail.find('span' ,{"class":"fl"}):
            if comment_detail.find('span' ,{"class":"fl"}).text.strip() == '½':
                score = 0.5
        stars = comment_detail.find_all('span', class_ ='glyphicon-star')
        score += len(stars)
    return score

def get_date(item):
    #para:item soup of comment
    #return date format:yyyy-mm-dd
    raw_date = item.find('span', {"class": 'fr'}).text
    temp = datetime.strptime(raw_date , "%B %d, %Y")
    audience_date = temp.strftime("%Y-%m-%d")
    return audience_date


def crawler_one_page(url , record):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
        "cache-control": "keep-alive",
        "cookie": "CBS_INTERNAL=0; ctk=NWJiNWM4ZGUzYWIxN2M0MmJhZTdiNzVmODAyNw%3D%3D; il_geo=%7B%22country%5Fcode%22%3A%22HK%22%2C+%22country%5Fname%22%3A%22Hong+Kong%22%2C+%22dma%5Fcode%22%3A%22ZZ%22%2C+%22postal%5Fcode%22%3A%22ZZ%22%7D; mc_s_s=a_4; __utmc=15671338; __utmz=15671338.1538640104.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.58085230.1538640104; LDCLGFbrowser=69ee613f-a7fe-48b3-9a9e-a9bb1d3151a1; XCLGFbrowser=R4rYx1u1yOjpcDxzQpM; AMCVS_10D31225525FF5790A490D4D%40AdobeOrg=1; __gads=ID=dd05fb38bcdadf35:T=1538640104:S=ALNI_Ma271SJZFjK18NaygLg-O_c2VG7vA; s_cc=true; aam_uuid=54632294702589067141111622257900194541; OX_plg=pm; OX_nd=; GED_PLAYLIST_ACTIVITY=W3sidSI6Ik1jTGsiLCJ0c2wiOjE1Mzg2NDAxMjksIm52IjoxLCJ1cHQiOjE1Mzg2NDAxMjMsImx0IjoxNTM4NjQwMTI2fV0.; tmpid=1538982114855043; __utma=15671338.58085230.1538640104.1538721854.1538982115.4; s_vnum=1541232104901%26vn%3D4; s_invisit=true; s_lv_undefined_s=Less%20than%207%20days; _tb_sess_r=; _gid=GA1.2.1608336114.1538982116; trc_cookie_storage=taboola%2520global%253Auser-id%3D670ae15a-66c1-4212-bfd5-b7d63a6dcd1e-tuct2b09f6a; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=-894706358%7CMCMID%7C54422490646064340821097414294592868245%7CMCAAMLH-1539244905%7C11%7CMCAAMB-1539586915%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1538989315s%7CNONE%7CMCAID%7C2DDAE474852A03B5-60000106C0000CF2%7CvVersion%7C2.3.0%7CMCCIDH%7C3162487; s_sq=%5B%5BB%5D%5D; DigiTrust.v1.identity=eyJwcml2YWN5Ijp7Im9wdG91dCI6ZmFsc2V9LCJpZCI6ImRmWCtYM1NpckQ2WUk4QlFlUmZBOTV5Y1FOa3RkdmlJYTc1WVdNM1dwc0dxT0FacUdxU2N2emV6TVVNV2ZWSE9qcnppMXJ4TVFnUzhiTVlNazg5SWlEZmlQS0dmSytOZjBnWG9Qb1lKUld6bzZwK2Fad0J4cWFOWXpPbm55eGdJei84TGZINHhMaDBTWHBwdDduMC9sOUNMdWdhUnZQdlJWdm1CMDR2RW0yT0x4OGMyNk93WUVKdDlNWmpKVVR1TnM5VlVlNk9aYldOYmUrb1Q0V2VCWlNQVStYNi9VMitJTUVxanlNMmIxR0FsZkNNSW92a2t3L09lZzgxckN6S09ybTROUUZpemVWWGFaYmw0QlRmTWlJdVlUSFJiL1ZTTkVUcWNwT3lyZklhaHpmTmNRKzNLQUNreXY4dVZwRFV3RGc3ZWorYmxwQWp4SGJEMnBiUTAxdz09IiwicHJvZHVjZXIiOiJ5ZUNVTEZJT2tmIiwidmVyc2lvbiI6Miwia2V5diI6NH0%3D; __qca=P0-521254617-1538982696778; prevPageType=product_overview; metapv=6; utag_main=v_id:01663e18ca95006e7f4f88adbfd003079003807100ac2$_sn:4$_ss:0$_st:1538985145356$_pn:6%3Bexp-session$ses_id:1538982115367%3Bexp-session; __utmt=1; __utmb=15671338.6.10.1538982115; s_getNewRepeat=1538983345515-Repeat; s_lv_undefined=1538983345515; _tb_t_ppg=https%3A//www.metacritic.com/movie/pinocchio%3Faccept%3Dtext%252Fhtml%252Capplication%252Fxhtml%252Bxml%252Capplication%252Fxml%253Bq%253D0.9%252Cimage%252Fwebp%252Cimage%252Fapng%252C%252A%252F%252A%253Bq%253D0.8%26accept-encoding%3Dgzip%252C+deflate%252C+br%26accept-language%3Den-US%252Cen%253Bq%253D0.9%252Czh-TW%253Bq%253D0.8%252Czh%253Bq%253D0.7%26cache-control%3Dkeep-alive%26cookie%3DCBS_INTERNAL%253D0%253B+ctk%253DNWJiNWM4ZGUzYWIxN2M0MmJhZTdiNzVmODAyNw%25253D%25253D%253B+il_geo%253D%25257B%252522country%25255Fcode%252522%25253A%252522HK%252522%25252C%252B%252522country%25255Fname%252522%25253A%252522Hong%252BKong%252522%25252C%252B%252522dma%25255Fcode%252522%25253A%252522ZZ%252522%25252C%252B%252522postal%25255Fcode%252522%25253A%252522ZZ%252522%25257D%253B+mc_s_s%253Da_4%253B+__utmc%253D15671338%253B+__utmz%253D15671338.1538640104.1.1.utmcsr%253D%2528direct%2529%257Cutmccn%253D%2528direct%2529%257Cutmcmd%253D%2528none%2529%253B+_ga%253DGA1.2.58085230.1538640104%253B+LDCLGFbrowser%253D69ee613f-a7fe-48b3-9a9e-a9bb1d3151a1%253B+XCLGFbrowser%253DR4rYx1u1yOjpcDxzQpM%253B+AMCVS_10D31225525FF5790A490D4D%252540AdobeOrg%253D1%253B+__gads%253DID%253Ddd05fb38bcdadf35%253AT%253D1538640104%253AS%253DALNI_Ma...; _gat__pm_ga=1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}

    r = requests.get(url , headers = header)
    soup = BeautifulSoup(r.text , 'lxml')
    record_list = []
    # if no result
    content = soup.find('div' , {'class' : 'next_to_side_col'})

    if content.find('div' , {'class' : 'pad_btm2'}):
        print('end of this movie')
        return 0
    else:
        reviews = content.find_all('div' , {'class' : 'review'})
        for item in reviews:
            tmp = copy.deepcopy(record)
            audience_name = item.find('span' , class_='author').text.strip()
            audience_score = item.find('div' , class_='metascore_w').text.strip()
            audience_date = item.find('span' , class_='date').text.strip()
            audience_comment = item.find('div' , class_='review_body').text.strip()
            useful_count = item.find('span' , class_='yes_count').text.strip()
            total_count = item.find('span' , class_='total_count').text.strip()
            unuseful_count = int(total_count) - int(total_count)
            tmp.append(audience_name)
            tmp.append(audience_score)
            tmp.append(audience_date)
            tmp.append(audience_comment)
            tmp.append(useful_count)
            tmp.append(unuseful_count)
            record_list.append(tmp)
        return record_list

if __name__ == '__main__':
    #get valid movie list
    table_name = 'MC_reviews'
    db = Database(table_name)
    db.connect()
    db.create_review_table()
    valid_movie_list = db.get_mc_valid_movie_list()
    count = 0
    for item in valid_movie_list:
        count += 1
        print("~~~~~~~~~~~~~" + str(count) + "~~~~~~~~~~~~~")
        movie_name = item[0]
        url = item[1]
        record = []
        record.append(movie_name)
        record.append(url)
        for page in range(1 , 52):
            #https://www.metacritic.com/movie/the-wolf-of-wall-street/user-reviews?page=0
            search_url = url + "/user-reviews?page=" + str(page)
            crawler_result = crawler_one_page(search_url ,record)
            if crawler_result != 0:
                for temp in crawler_result:
                    print(temp)
                    db.insert_MC_review(*temp)
            else:
                break
    db.close()
