from datetime import datetime

from bs4 import BeautifulSoup
import bs4
from tools import *

def crawl_awards_detail(db , id , text):
    detail_soup = BeautifulSoup(text , 'lxml')
    #title
    #example : Rain Man (1988)
    title_and_year = detail_soup.find('div' , {'id':'title_heading'}).find('span').text

    if "(" in title_and_year:
        title = title_and_year[:title_and_year.rindex('(') - 1].strip()
    else:
        title = title_and_year


    awards_soup = detail_soup.find('div' , id = 'awards')
    if awards_soup:
        for award_event in awards_soup.find_all('div' , class_= 'event_awards'):
            event_year = award_event.find('div' , class_ = 'a-col-left').text.strip()
            event_name = award_event.find('div' , class_ = 'a-col-right').find('span').text.strip()
            #get each award
            for award_nomination in award_event.find('div' , class_ = 'a-col-right').find_all('div' , class_= 'award_nomination'):
                awarder_list = []

                if len(award_nomination.find_all('span')) == 3:
                    award_status = 'Won'

                else:
                    award_status = 'Nominated'
                award_title = award_nomination.find('div').find_all('span')[-1].text.strip()[2:]
                if award_nomination.find('a'):
                    is_to_movie = 0
                else:
                    is_to_movie = 1
                sub_title =''
                descrption = ''
                for i in range(0 , len(award_nomination.contents)):
                    if i == 2 and award_nomination.contents[i].name == 'div':
                        sub_title = award_nomination.contents[i].text.strip()
                    if award_nomination.contents[i].name == 'a':
                        actorname = award_nomination.contents[i].text.strip()
                        actorid = cut_string(award_nomination.contents[i].attrs['href'] , '/' , 4, 5)
                        awarder_list.append((actorname , actorid))
                    if i > 2 and award_nomination.contents[i].name == 'div':
                        descrption = award_nomination.contents[i].text.strip()

                #record data
                if is_to_movie == 1:
                    #award for movie
                    record = {"imdb_id": id,
                              "imdb_movie_title": title,
                              "imdb_award_year": event_year,
                              "imdb_award_event_name": event_name,
                              "imdb_award_status": award_status,
                              "imdb_award_title": award_title,
                              "imdb_award_subtitle": sub_title,
                              "imdb_award_is_tomovie": 1,
                              "imdb_award_owner": "",
                              "imdb_award_owner_id": "",
                              "imdb_award_description": descrption,
                              }
                    table_name = 'imdb_movie_awards'
                    db.insert_dict(record, table_name)
                    print(record)
                else:
                    for actor in awarder_list:
                        record = {"imdb_id": id,
                                  "imdb_movie_title": title,
                                  "imdb_award_year": event_year,
                                  "imdb_award_event_name": event_name,
                                  "imdb_award_status": award_status,
                                  "imdb_award_title": award_title,
                                  "imdb_award_subtitle": sub_title,
                                  "imdb_award_is_tomovie": 0,
                                  "imdb_award_owner": actor[0],
                                  "imdb_award_owner_id": actor[1],
                                  "imdb_award_description": descrption,
                                  }
                        table_name = 'imdb_movie_awards'
                        db.insert_dict(record, table_name)
                        print(record)
