import os

import requests
from bs4 import BeautifulSoup

from database import Database
from crawl_detail import crawl_movie_detail
from imdb_multidirector import crawl_movie_multidirector
from crawl_cast import  crawl_cast
from crawl_website import crawl_website

header = {"Accept": "text/html, */*; q=0.01",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
          "Connection": "keep-alive",
          "Cookie": "session-id=134-9623991-4001834; session-id-time=2169681939; ubid-main=134-8682807-7323811; session-token='pe2C2cqR+kIl0yXE7ilXdZ/19TNkRWNCBHS+lZXH6H+0Ah1XkmTtskLRNm4wxsrGuwc1wDxAtrrGnJ9KmeQ7V8ESQX7KgfS2qVJn72cr63IM7rS5hjbJ8ZvVE3kfdgo1rx2JRCwrE9v0cSep4jf8uP0mg9N3IPJ1JzaFz6QTHol3wsafq+Z7aEmBD4ue3ddvNUbMUO6z/oxhnoK6Sj/UiA=='; x-main='fhufemw31oaoi59eyd2D8fCx0JbsuAuO9L92gBwpT85IjAh3?8jeeHCfmRQL1PPE'; at-main=Atza|IwEBIGIVlB5KBAgVeCbIliHa78jpWQwi47yOSitZ8QeysCyutbaYfzfzAUrcGyvph7Xfkiria0N3iBGorPR5xTzxck4GiJgb3S2F2VugGuXXdapK5iU9YZ3n0igUvHIOT4iDM7ptgSnLW3FNvhQ45zezczQBPuWfuSAf48yIjls0P0AKViK1oUfHTeJLlSZEbj_0Rf-fQuCv6yzwozpoHZ1m6NwTmpwxsZMBtl5_FCP50O8CLV70JjCn63FVew1vjiyoU5JOAPa6JyRmFTYYERFh4sbg0UTbBuX-dyMOvsez-DFb1K-a3trPA2dzvZfzJLjb9eH4tRVxk0hXmRUCQUCo5QL-WIZTfzHzXd01mY--cOm6_dkm-OpvVRBnWl4mt1plskDsfZcsrxqYtdHqbchz072U; sess-at-main='B2yUVlv1hAPTmZ+cckk+EnSLEjtpNd05vrMKJG3kH5s='; id=BCYqn-8sbizufuEObPif3e8gObrA9av0XBsD3zwJg0ocdq8a8LoqoJnrj187PfE3hggHEyI2F8JU%0D%0AbVYa8K-snLF8svhpdSg_SZjJi5Faz8MLgQMMMt4mv4F3C43TA5YvLJZYHSCKpLu6BkUSZFIoS636%0D%0AzQ%0D%0A; uu=BCYl-X5aVhHcO6yDZM71uBuDWuq6cDkRSZSE3YKU6zr5bVfsIgko0aHjT2p31dM9yfCvaAXSItN-%0D%0A5mLpXBBf4jLtswgPlMgr0Wjlr3-XzUuLJY2YN7mFHcuikxhlu32TMqcXKHSqf8iSMP00wMjEegeB%0D%0AU44ekAiNukUhIzFMxmQ7t994oPrmz7dcIEx1eJ0utp1oV9-ctp1IgseWMFswwncE0SgWTmZMyf5c%0D%0AjvbrdRBzquC6WhenHmWCcl1Wd7rRNqR4k6G_HGfmda4_341DdC1kUw%0D%0A; sid=BCYhTRi_6HBDoCSnMCGip8Y4PzM-PcwnQ85HUBHsIC4B0ePDN3jrRrxoZBFMuWJ29ARXPEf6VHBu%0D%0AuJSBEU_HP78mLjui6XrAslBv8w5zWCJZ1hR5wZLHtPyZ2yny-U8e0X9RsGUTVQXQAxcVr1ZVppqq%0D%0ADw%0D%0A; csm-hit=tb:S7YDJY3ERA212P1FMYVF+s-6HPQZX1CQWFK7B0BFCT2|1539047882541&adb:adblk_no; pa=BCYnaFsPn5iLN00VjGUSDaAkYuba1mk2Vl2CGHrRA5f5KfrauxEp2gyIEMCzZdeO9Yghwk_ahNcQ%0D%0AHa_1-eT78vwecYuYaT8_ZPBE9A4kJkRzAGFJxXR3CC2YtC7xWP2Mury-%0D%0A",
          "Host": "pro.imdb.com",
          "Referer": "https://pro.imdb.com/title/tt0101318/details",
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest"}

def save_base_web(id , type , text):
    new_dir = r'imdb_backup/' + id + '/'
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    f_save = open(new_dir + type + '.html' , 'w')
    f_save.write(text)
    f_save.close()

def is_wrong_website(text , title):
    soup = BeautifulSoup(text , 'lxml')
    soup.find('title').text
    if soup.find('title').text =='500 - IMDbPro' or soup.find('div' , {"id":'upsell_widget'}):
        fw_wrong = open('wrong_website.txt' , 'a')
        fw_wrong.write(title + '\n')
        fw_wrong.close()
        return 0
    return 1

if __name__ == '__main__':
    db = Database()
    db.connect()
    # imdb_id_list = db.get_imdb_id_list()
    # read local file
    dir_path = 'imdb_backup/'
    dir_list = os.listdir(dir_path)

    # dir_list = ['tt0457513' , 'tt3630276']
    for id in dir_list:
        #details
        if id[0] == '.':
            continue
        else:
            # type = 'details'
            # file_name = dir_path + id + "/"  + type + '.html'
            # f_read = open(file_name , 'r')
            # # r = requests.get(url , headers = header)
            # html_content = f_read.read()
            # f_read.close()
            # if is_wrong_website(html_content , file_name):
            #     print(file_name)
            #     # save_base_web(id , type , html_content)
            #     crawl_movie_multidirector(db , id , html_content)

            # type = 'cast'
            # file_name = dir_path + id + "/" + type + '.html'
            # f_read = open(file_name, 'r')
            # # r = requests.get(url , headers = header)
            # html_content = f_read.read()
            # f_read.close()
            # if is_wrong_website(html_content, file_name):
            #     print(file_name)
            #     # save_base_web(id , type , html_content)
            #     crawl_cast(db, id, html_content)

            type = 'website'
            file_name = dir_path + id + "/" + type + '.html'
            f_read = open(file_name, 'r')
            # r = requests.get(url , headers = header)
            html_content = f_read.read()
            f_read.close()
            if is_wrong_website(html_content, file_name):
                print(file_name)
                # save_base_web(id , type , html_content)
                crawl_website(db, id, html_content)

        #
        # # cast
        # type = 'cast'
        # file_name = dir_path +  type + '.html'
        # f_read = open(file_name , 'r')
        # # r = requests.get(url , headers = header)
        # html_content = f_read.read()
        # f_read.close()
        #
        # # awards
        # type = 'awards'
        #
        #
        # # website
        # type = 'website'






    db.close()

