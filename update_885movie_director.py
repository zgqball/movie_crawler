import time

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

    def get_imdb_id_list(self):
        #from all_city table
        query = ("select distinct imdb_id "
                 "from movie885 ")
        self.cur.execute(query)
        self.conn.commit()
        imdb_id_list= self.cur.fetchall()
        imdb_id_list = list(imdb_id_list)
        temp_list = []
        for item in imdb_id_list:
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

if __name__ == '__main__':
    table_name = 'movie885'
    db = Database(table_name)
    db.connect()

    imdb_id_list = db.get_imdb_id_list()
    base_url = "https://www.imdb.com/title/{}/fullcredits?ref_=tt_ov_dr#directors/"
    for id in imdb_id_list:
        url = base_url.format(id)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        directors = soup.select('#fullcredits_content > table')[0].find_all('tr')
        director = ""
        for item in directors:
            temp = item.find('a').text.strip()
            director = director + temp + ', '
        director = director[:-2]
        print(id + '~~~~~~~~~~' + director)
        db.update_director(director , id)
        # time.sleep(2)
    db.close()