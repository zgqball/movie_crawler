import random
import time
import traceback

import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.common
from selenium.webdriver.support.wait import WebDriverWait


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

    def create_table(self):
        try:
            query = ("CREATE TABLE if not exists {} ("
                     "search_title VARCHAR(255), "
                     "result_title VARCHAR(255), "
                     "search_year VARCHAR(10), "
                     "url VARCHAR(255),"
                     "description text"
                     ");".format(self.table_name))
            self.cur.execute(query)
            self.conn.commit()
            print("Table {} is created!".format(self.table_name))

        except Exception as e:
            print("Tables exist / cannot be created!")


    def create_review_table(self):
        try:
            query = ("CREATE TABLE if not exists {} ("
                     "search_title VARCHAR(255), "
                     "url VARCHAR(255), "
                     "audience_name VARCHAR(255), "
                     "audience_score int, "
                     "review_date VARCHAR(255), "
                     "audience_comment text, "
                     "useful_count int, "
                     "unuseful_count int "
                     ");".format(self.table_name))
            self.cur.execute(query)
            self.conn.commit()
            print("Table {} is created!".format(self.table_name))

        except Exception as e:
            print("Tables exist / cannot be created!")

    def get_885movies_title(self):
        #from all_city table
        query = ("SELECT movie_title "
                 "FROM movie885")
        self.cur.execute(query)
        self.conn.commit()
        movie885_title_list= self.cur.fetchall()
        movie885_title_list = list(movie885_title_list)

        return movie885_title_list

    def get_mc_valid_movie_by_year(self):
        #from all_city table
        query = ("select distinct a.search_title , a.url "
                 "from mc_movie as a , movie885 as b "
                 "where  a.search_title  = b.movie_title and a.search_year = b.movie_year")
        self.cur.execute(query)
        self.conn.commit()
        valid_movie_list= self.cur.fetchall()
        valid_movie_list = list(valid_movie_list)

        return valid_movie_list

    def get_mc_valid_movie_by_director(self):
        #from all_city table
        query = ("select distinct a.search_title , a.url "
                 "from mc_movie as a , movie885 as b "
                 "where  a.search_title  = b.movie_title and a.director = b.director "
                 "and a.url not in (select distinct url from mc_reviews)")
        self.cur.execute(query)
        self.conn.commit()
        valid_movie_list= self.cur.fetchall()
        valid_movie_list = list(valid_movie_list)

        return valid_movie_list

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

    def insert_MC_review(self, *args):
        query = ("INSERT INTO {} "
                 "(search_title, url , audience_name  , audience_score , review_date , audience_comment , audience_comment , useful_count , unuseful_count) "
                 "VALUES {};".format(self.table_name , args))
        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    table_name = 'MC_movie'
    db = Database(table_name)
    db.connect()
    db.create_table()
    movie_list = db.get_885movies_title()
    already_have = db.get_already_have_title()
    having_list = []
    for item in already_have:
        having_list.append(item[0])
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
    )
    driver = webdriver.Chrome(desired_capabilities=dcap)
    driver.implicitly_wait(5)


    base_url = "https://www.metacritic.com/search/movie/"
    for movie in movie_list:
        movie_name = movie[0]
        if movie_name not in having_list:
            movie_name =movie_name.replace('/' , ' ')
            url = base_url + movie_name + "/results"
            driver.get(url)
            # driver.implicitly_wait(10)
            WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name("search_results"))
            soup = BeautifulSoup(driver.page_source , 'lxml')
            resultsoup = soup.find('ul' , {"class" : "search_results"})

            if resultsoup:
                items = resultsoup.find_all('li')
                for item in items:
                    record = []
                    record.append(movie_name)

                    search_title = item.find('h3').find('a').text.strip()
                    record.append(search_title)
                    try:
                        movie_year = item.find('p').text.strip().split(', ')[1]
                        record.append(movie_year)
                    # no year record
                    except:
                        record.append("")

                    movie_url = 'https://www.metacritic.com' + item.find('h3').find('a').attrs['href']
                    record.append(movie_url)
                    try:
                        movie_description = item.find('p' , {"class":'deck'}).text.strip()
                        record.append(movie_description)
                    except:
                        record.append("")

                    print(record)
                    db.insert_movie(*record)
            else:
                f = open('MC_no_result.txt' , 'a')
                f.write(movie_name +'\n')
                f.close()

            time.sleep(random.randint(0, 2))
        else:
            continue

    driver.close()
    db.close()