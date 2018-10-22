import copy
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from rt.RT_moive_crawler import Database

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

def is_superreviewer(item):
    if item.find('div' , {'class':'superreviewer'}).text == "":
        return 1
    else:
        return 0

def crawler_one_page(url , record):
    r = requests.get(url)
    soup = BeautifulSoup(r.text , 'lxml')
    record_list = []
    # if no result
    if soup.find('p' , {'class' : 'center'}):
        print('end of this movie')
        return 0
    else:
        reviews = soup.find_all('div' , {'class' : 'row'})
        for item in reviews[:-1]:
            tmp = copy.deepcopy(record)
            audience_name = item.find('span' , {'style':'word-wrap:break-word'}).text.strip()
            is_super = is_superreviewer(item)
            audience_score = count_star(item)
            audience_date = get_date(item)
            audience_comment = item.find('div' ,{'class':'user_review'}).text.strip()
            tmp.append(audience_name)
            tmp.append(is_super)
            tmp.append(audience_score)
            tmp.append(audience_date)
            tmp.append(audience_comment)
            record_list.append(tmp)
        return record_list

if __name__ == '__main__':
    #get valid movie list
    table_name = 'RT_reviews'
    db = Database(table_name)
    db.connect()
    db.create_review_table()
    already_have_url_list = db.get_already_have_url()
    valid_movie_list = db.get_valid_movie_list()
    count = 0
    for item in valid_movie_list:
        count += 1
        print("~~~~~~~~~~~~~" + str(count) + "~~~~~~~~~~~~~")
        movie_name = item[0]
        url = item[1]
        if url in already_have_url_list:
            continue
        else:
            record = []
            record.append(movie_name)
            record.append(url)
            for page in range(1 , 52):
                search_url = url + "/reviews/?type=user&page=" + str(page)
                crawler_result = crawler_one_page(search_url ,record)
                if crawler_result != 0:
                    for temp in crawler_result:
                        print(temp)
                        db.insert_RT_review(*temp)
                else:
                    break
    db.close()