import datetime
import sys

import pymysql
import requests
import json


class Database():
    def __init__(self):
        self.conn = None
        self.cur = None

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
        query = ("update {} set director = '{}' "
                 "where imdb_id  = '{}';".format(self.table_name , new_director , update_imdb_id))
        self.cur.execute(query)
        self.conn.commit()

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

    def close(self):
        self.cur.close()
        self.conn.close()

db = Database()
db.connect()
base_url = 'http://flicksurfer.com/api/flicks?query=&netflix_regions=all&types=&genres=&year_min=1915&year_max=2016&awards=-1&range_score_imdb_min=0&range_score_imdb_max=101&range_score_rt_min=0&range_score_rt_max=101&range_score_netflix_min=0&range_score_netflix_max=101&range_score_average_min=0&range_score_average_max=101&range_votes_imdb_min=0&range_votes_imdb_max=101000&range_votes_rt_min=0&range_votes_rt_max=101&date_added_min=-100&date_added_max=1&genre_connector=or&sort=date_added&page='
header = {
"Accept" : "application/json, text/plain, */*",
"Accept-Encoding" : "gzip, deflate",
"Accept-Language" : "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
"Authorization" : "*/*",
"Connection" : "keep-alive",
"Cookie" : "_dc=DOUBLECLICK.1372607028dniweol1404033358; _fb=FB.jd832dj489dj4cm8934cj98jmc3489cj434c894jc; _twtr=TWTR.cilbjcvx89bjvcbpjvxb89vcjbcvx0bjcv8x0bjcvx89; _ga=GA1.2.1336703723.1542860602; _gid=GA1.2.1670287253.1542860602",
"Host" : "flicksurfer.com",
"Referer" : "http://flicksurfer.com/",
"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}
for i in range(1 , 333):
    print('writing page ' + str(i) )
    url = base_url + str(i)
    re = requests.get(url , headers = header)
    dict = json.loads(re.text)
    for item in dict['_embedded']['flicks']:
        record = {'rating' : item.get('rating',None),
                  'rt_score': item.get('rt_score',None),
                  'image': item.get('image',None),
                  'year': item.get('year',None),
                  'duration': item.get('duration',None),
                  'category': item.get('category',None),
                  'netflix_score': item.get('netflix_score',None),
                  'title': item.get('title',None),
                  'rt_votes': item.get('rt_votes',None),
                  'imdb_link': item.get('imdb_link',None),
                  'imdb_votes': item.get('imdb_votes',None),
                  'netflix_description': item.get('netflix_description',None),
                  'netflix_regions': "@@@".join(item.get('netflix_regions',[])),
                  'average_score': item.get('average_score',None),
                  'netflix_link': item.get('netflix_link',None),
                  'director': "@@@".join(item.get('director',[])),
                  'awards': item.get('awards',None),
                  'genre': "@@@".join(item.get('genre',[])),
                  'date_added': datetime.datetime.utcfromtimestamp(item.get('date_added',[])).strftime("%Y-%m-%d %H:%M:%S"),
                  'rt_user_votes': item.get('rt_user_votes',None),
                  'rt_user_score': item.get('rt_user_score',None),
                  'rt_link': item.get('rt_link',None),
                  'language': "@@@".join(item.get('language',[])),
                  'imdb_description': item.get('imdb_description',None),
                  'cast': "@@@".join(item.get('cast',[])),
                  'imdb_score': item.get('imdb_score',None),
                  'rt_consensus': item.get('rt_consensus',None),
                  }
        db.insert_dict(record , 'flicksurfer_link_netflix_to_imdb')
db.close()