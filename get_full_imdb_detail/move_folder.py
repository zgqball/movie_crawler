import os
import shutil
import sys

import pymysql


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
        query = ("select distinct imdb_id , imdb_year "
                 "from imdb_full_id ")
        self.cur.execute(query)
        self.conn.commit()
        imdb_id_list= self.cur.fetchall()
        imdb_id_list = list(imdb_id_list)
        temp_list = {}
        for item in imdb_id_list:
            temp_list[item[0]] = item[1]
        return temp_list

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
for year in range(2000 , 2019):
    new_dir = r'imdb_backup/' +str(year)+'/'
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
full_id_dict = db.get_imdb_id_list()
dir_path = 'imdb_backup/'
need_move_list = os.listdir(dir_path)
for id in need_move_list:
    if id[:2] == 'tt':
        try:
            shutil.move(dir_path + id +'/', dir_path + str(full_id_dict[id]) + '/'+ id +'/')
        except:
            continue