import re
import sys
import time
from datetime import datetime

import pymysql
import requests
from bs4 import BeautifulSoup

class Database():
    def __init__(self , table_name):
        self.conn = None
        self.cur = None
        self.table_name = table_name

    def connect(self):
        db_host = "144.214.55.104"
        db_user = "zgq"
        db_pass = 'Indeed2018'
        db_name = "streaming"
        db_char = "utf8mb4"

        try:
            self.conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name,
                                        charset=db_char)
            self.cur = self.conn.cursor()
            print("Database connection succeeded!")
        except Exception as e:
            print(e)

    def get_885movies_title(self):
        #from all_city table
        query = ("SELECT movie_title "
                 "FROM movie885")
        self.cur.execute(query)
        self.conn.commit()
        movie885_title_list= self.cur.fetchall()
        movie885_title_list = list(movie885_title_list)

        return movie885_title_list

    def get_rt_url_list(self):
        #from all_city table
        query = ("select distinct url "
                 "from rt_movie where director is null ")
        self.cur.execute(query)
        self.conn.commit()
        rt_url_list= self.cur.fetchall()
        rt_url_list = list(rt_url_list)
        temp_list = []
        for item in rt_url_list:
            temp_list.append(item[0])
        return temp_list

    def get_already_have_title(self):
        # from all_city table
        query = ("SELECT search_title "
                 "FROM {}".format(self.table_name))
        self.cur.execute(query)
        self.conn.commit()
        already_have_title_list = self.cur.fetchall()
        already_have_title_list = list(already_have_title_list)

        return already_have_title_list

    def insert_movie(self, *args):
        query = ("INSERT INTO {} "
                 "(search_title, result_title , search_year , url , description) "
                 "VALUES {};".format(self.table_name , args))
        self.cur.execute(query)
        self.conn.commit()

    def update_director(self, new_director , update_imdb_id):
        query = ("update {} set director = %s "
                 "where imdb_id  = %s;".format(self.table_name ))
        self.cur.execute(query , (new_director , update_imdb_id))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def update_rt_detail(self , my_dict , raw_url):
        query = ''
        for (key, value) in my_dict.items():
            value = value.replace("\"" ,"")
            query = query + key + '=\"' + value + '\",'
        query = query[:-1]
        sql = "update {} set {} where url = %s".format(self.table_name , query)
        try:
            self.cur.execute(sql ,(raw_url))
            self.conn.commit()
        except:
            print("SQL error:", sys.exc_info()[1])

def get_date(raw_datetime):
    #para:item soup of comment
    #return date format:yyyy-mm-dd
    temp = datetime.strptime(raw_datetime , "%b %d, %Y")
    audience_date = temp.strftime("%Y-%m-%d")
    return audience_date


change_word = {"Rating" : "rating",
               "Genre": "genre",
               "Directed By": "director",
               "Written By": "written_by",
               "In Theaters": "in_theaters",
               "On Disc/Streaming": "streaming",
               "Box Office": "box_office",
               "Runtime": "runtime",
               "Studio": "studio",
               }
if __name__ == '__main__':
    table_name = 'rt_movie'
    db = Database(table_name)
    db.connect()

    rt_url_list = db.get_rt_url_list()
    # base_url = 'https://www.imdb.com/title/'
    for url in rt_url_list:
        # url = base_url + id
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            content = soup.find('section', {'class': 'movie_info'})
            record = {"description": "",
                      "rating": "",
                      "genre": "",
                      "director": "",
                      "written_by": "",
                      "in_theaters": "",
                      "streaming": "",
                      "box_office": "",
                      "runtime": "",
                      "studio": "",
                      }
            #description
            try:
                description = content.find('div',{'class':'movie_synopsis'}).text.strip()
            except:
                description = ""
            record["description"] = description
            details = content.find_all('li')
            for item in details:
                key = item.text.strip().split(':')[0]
                if key in change_word:
                    key = change_word[key]
                else:
                    continue
                #date
                if key == 'streaming':
                    value = item.text.strip().split(':')[1].strip()
                    value = get_date(value)

                elif key == 'in_theaters':
                    value = item.text.strip().split(':')[1].strip()
                    pattern = re.compile(r'\n\xa0')
                    value = re.split(pattern,value)[0]
                    value = get_date(value)
                else:
                    value = item.text.strip().split(':')[1].strip().replace("\n" ,"").replace(",                         ",",")
                record[key] = value
            print(record)
            db.update_rt_detail(record , url)
        else:
            continue
        # time.sleep(2)
    db.close()