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
        query = ("select distinct url ,search_title "
                 "from rt_movie ")
        self.cur.execute(query)
        self.conn.commit()
        rt_url_list= self.cur.fetchall()
        rt_url_list = list(rt_url_list)
        # temp_list = []
        # for item in rt_url_list:
        #     temp_list.append(item[0])
        return rt_url_list

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

    def insert_dict(self, my_dict, table_name):
        data_values = "(" + "%s," * (len(my_dict)) + ")"
        data_values = data_values.replace(',)', ')')

        dbField = my_dict.keys()
        dataTuple = tuple(my_dict.values())
        dbField = str(tuple(dbField)).replace("'", '')
        sql = """ insert into %s %s values %s """ % (table_name, dbField, data_values)
        params = dataTuple
        try:
            self.cur.execute(sql, params)
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
               "Directed By": "rt_director",
               "Written By": "written_by",
               "In Theaters": "in_theaters",
               "On Disc/Streaming": "streaming",
               "Box Office": "box_office",
               "Runtime": "runtime",
               "Studio": "studio",
               }
if __name__ == '__main__':
    table_name = 'rt_movie_director'
    db = Database(table_name)
    db.connect()

    rt_url_list = db.get_rt_url_list()
    # base_url = 'https://www.imdb.com/title/'
    for url , search_title in rt_url_list:
        # url = base_url + id
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            content = soup.find('section', {'class': 'movie_info'})
            record = {"rt_url": url,
                      "rt_search_title": search_title,
                      "rt_director": "",
                      }

            details = content.find_all('li')
            for item in details:
                key = item.text.strip().split(':')[0]
                if key in change_word:
                    key = change_word[key]
                else:
                    continue
                if key == "rt_director":
                    value = item.text.strip().split(':')[1].strip().replace("\n", "").replace(
                        ",                         ", ",")
                    if ", " in value:
                        directors = value.split(', ')
                        for director in directors:
                            record[key] = director
                            print(record)
                            db.insert_dict(record, table_name)
                    else:
                        record[key] = value
                        db.insert_dict(record, table_name)
                else:
                    continue

        else:
            continue
        # time.sleep(2)
    db.close()