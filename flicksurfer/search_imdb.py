import csv
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from database import Database

def cut_string(string , sub , start_num , end_num):
    temp = string.split(sub)
    result = ''
    for i in range(start_num , end_num):
        result = result + temp[i]
    return result

def work(id , title):

    "https://www.imdb.com/title/tt8765496/?ref_=fn_al_tt_1"

    url = "https://www.imdb.com/title/tt8765496/?ref_=fn_al_tt_1"
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')
    options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('quicksearch_dropdown_wrapper'))

    element = driver.find_element_by_xpath('//*[@id="navbar-query"]')
    element.clear()
    element.send_keys(u'18298329937')

    element.clear()
    element.send_keys(u'ab')
    element.clear()
    element.send_keys(u'rew')
    element.clear()
    element.send_keys(u'bg')
    element.clear()
    element.send_keys(u'nj')
    element.clear()
    element.send_keys(u'ui')
    a = '//*[@id="navbar-suggestionsearch"]/div[1]/a'
    all_movie_num = int(driver.find_element_by_class_name('total_item_count').text.replace(',', ''))
    print("there are " + str(all_movie_num) + "results!!!!!")
    realtime_movie_num = len(driver.find_elements_by_xpath('//*[@id="results"]/ul/li'))
    print(realtime_movie_num)
    while (realtime_movie_num < all_movie_num):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        realtime_movie_num = len(driver.find_elements_by_xpath('//*[@id="results"]/ul/li'))
        print('temp:' + str(realtime_movie_num))
        print(all_movie_num)
    f_write = open(new_dir + "imdb_movie_" + year + "_" + stage + '.html' ,'w')
    f_write.write(driver.page_source)
    f_write.close()
    time.sleep(3)
    driver.close()

def get_id(year):
    db = Database()
    db.connect()
    year_dir = 'imdb_whole_year_movie_backup/'
    years = os.listdir(year_dir)
    search_website_path = year_dir + str(year) + '/'
    website_list = os.listdir(search_website_path)
    for website in website_list:
        f_open = open(search_website_path + website , 'r')
        text = f_open.read()
        soup = BeautifulSoup(text , 'lxml')
        results = soup.find('div', {'id': 'results'}).find_all('li', {'class': 'title'})
        for item in results:
            id = cut_string(item.find('a').attrs['href'] , '/' , 4 , 5)
            title_and_year = item.text.strip()
            title = title_and_year[:title_and_year.rindex('(') - 1].strip()
            year = title_and_year[title_and_year.rindex('(') + 1: -1]
            temp = {'imdb_id':id,
                    'imdb_title':title,
                    'imdb_year':year}
            db.insert_dict(temp , 'imdb_full_id')
    db.close()

if __name__ == '__main__':
    # year = 1999
    file = open('imdb_tpb.csv' , 'r')
    csv_reader = csv.reader(file)
    url = "https://www.imdb.com/title/tt8765496/?ref_=fn_al_tt_1"
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')
    options.add_argument(
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('quicksearch_dropdown_wrapper'))

    element = driver.find_element_by_xpath('//*[@id="navbar-query"]')

    for item in csv_reader:
        file = open('search_result_coming_change.txt', 'a')
        id = item[0]
        title = item[1]
        element.clear()
        element.send_keys(title)
        time.sleep(3)
        result_first = driver.find_element_by_xpath('//*[@id="navbar-suggestionsearch"]/div[1]/a')
        # detail = result_first.text
        url = result_first.get_attribute('href')
        search_title = result_first.find_element_by_class_name('title').text
        try:
            year = result_first.find_element_by_class_name('extra').text
        except:
            year = ""
        file.write(id +','+title+','+url+','+search_title+','+year+'\n')
        file.close()
    driver.close()
        # work(id , title)