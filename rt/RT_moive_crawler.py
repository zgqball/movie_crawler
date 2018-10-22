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
                     "url VARCHAR(255)"
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
                     "is_superreviewer tinyint, "
                     "audience_score float, "
                     "review_date VARCHAR(255), "
                     "audience_comment text "
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

    def get_valid_movie_list(self):
        #from all_city table
        query = ("select distinct a.search_title , url "
                 "from rt_movie as a , movie885 as b "
                 "where  a.search_title  = b.movie_title and a.search_year = b.movie_year")
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

    def get_already_have_url(self):
        # from all_city table
        query = ("SELECT distinct url "
                 "FROM {}".format(self.table_name))
        self.cur.execute(query)
        self.conn.commit()
        already_have_url = self.cur.fetchall()
        already_have_url = list(already_have_url)

        return already_have_url

    def insert_movie(self, *args):
        query = ("INSERT INTO {} "
                 "(search_title, result_title , search_year , url) "
                 "VALUES {};".format(self.table_name , args))
        self.cur.execute(query)
        self.conn.commit()

    def insert_RT_review(self, *args):
        query = ("INSERT INTO {} "
                 "(search_title, url , audience_name , is_superreviewer , audience_score , review_date , audience_comment) "
                 "VALUES {};".format(self.table_name , args))
        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()



class Chrome_driver(object):
    def __init__(self):
        try:
            self.driver = None
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
             )
            self.driver = webdriver.Chrome(desired_capabilities=dcap)
            self.driver.implicitly_wait(5)

            self.driver.get('https://www.tianyancha.com/login')
            time.sleep(2.0)

            element = self.driver.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]'
                                                        '/div[2]/div[2]/div[2]/input')
            element.clear()
            element.send_keys(u'18298329937')
            element = self.driver.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]'
                                                        '/div[2]/div[2]/div[3]/input')
            element.clear()
            element.send_keys(u'zz112233')

            element = self.driver.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]'
                                                        '/div[2]/div[2]/div[5]')
            element.click()
            time.sleep(5.0)
        except Exception:
            print(traceback.format_exc())
            print('异常退出')
            if self.driver:
                self.driver.close()


if __name__ == '__main__':
    table_name = 'RT_movie'
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


    base_url = 'https://www.rottentomatoes.com/search/?search='
    for movie in movie_list:
        if movie[0] not in having_list:
            url = base_url + movie[0]
            driver.get(url)
            # driver.implicitly_wait(10)
            try:
                driver.find_element_by_class_name("noresults")
                f = open('RT_no_result.txt' , 'a')
                f.write(movie[0] +'\n')
                f.close()

            except:
                WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("movieSection"))
                soup = BeautifulSoup(driver.page_source , 'lxml')
                movie_section = soup.find('section' , {'id' : 'movieSection'})
                movie_section = movie_section.find_all('li', {'class': 'bottom_divider'})
                for item in movie_section:
                    record = []
                    record.append(movie[0])

                    search_title = item.find('span',{'class':'bold'}).text
                    record.append(search_title)
                    try:
                        movie_year = item.find('span',{'class':'movie_year'}).text[2:][:-1]
                        record.append(movie_year)
                    # no year record
                    except:
                        record.append("")

                    movie_url = 'https://www.rottentomatoes.com' + item.find('span' , {'class':'bold'}).contents[0].attrs['href']
                    record.append(movie_url)
                    print(record)
                    db.insert_movie(*record)
            time.sleep(random.randint(0, 2))
        else:
            continue

    driver.close()
    db.close()