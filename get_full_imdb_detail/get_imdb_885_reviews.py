import time
from datetime import datetime

from database import Database
from bs4 import BeautifulSoup

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from tools import cut_string
import os

import requests

from database import Database
from crawl_detail import crawl_movie_detail

header = {"Accept": "text/html, */*; q=0.01",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
          "Connection": "keep-alive",
          "Cookie": "session-id=134-9623991-4001834; session-id-time=2169681939; ubid-main=134-8682807-7323811; session-token='pe2C2cqR+kIl0yXE7ilXdZ/19TNkRWNCBHS+lZXH6H+0Ah1XkmTtskLRNm4wxsrGuwc1wDxAtrrGnJ9KmeQ7V8ESQX7KgfS2qVJn72cr63IM7rS5hjbJ8ZvVE3kfdgo1rx2JRCwrE9v0cSep4jf8uP0mg9N3IPJ1JzaFz6QTHol3wsafq+Z7aEmBD4ue3ddvNUbMUO6z/oxhnoK6Sj/UiA=='; x-main='fhufemw31oaoi59eyd2D8fCx0JbsuAuO9L92gBwpT85IjAh3?8jeeHCfmRQL1PPE'; at-main=Atza|IwEBIGIVlB5KBAgVeCbIliHa78jpWQwi47yOSitZ8QeysCyutbaYfzfzAUrcGyvph7Xfkiria0N3iBGorPR5xTzxck4GiJgb3S2F2VugGuXXdapK5iU9YZ3n0igUvHIOT4iDM7ptgSnLW3FNvhQ45zezczQBPuWfuSAf48yIjls0P0AKViK1oUfHTeJLlSZEbj_0Rf-fQuCv6yzwozpoHZ1m6NwTmpwxsZMBtl5_FCP50O8CLV70JjCn63FVew1vjiyoU5JOAPa6JyRmFTYYERFh4sbg0UTbBuX-dyMOvsez-DFb1K-a3trPA2dzvZfzJLjb9eH4tRVxk0hXmRUCQUCo5QL-WIZTfzHzXd01mY--cOm6_dkm-OpvVRBnWl4mt1plskDsfZcsrxqYtdHqbchz072U; sess-at-main='B2yUVlv1hAPTmZ+cckk+EnSLEjtpNd05vrMKJG3kH5s='; id=BCYqn-8sbizufuEObPif3e8gObrA9av0XBsD3zwJg0ocdq8a8LoqoJnrj187PfE3hggHEyI2F8JU%0D%0AbVYa8K-snLF8svhpdSg_SZjJi5Faz8MLgQMMMt4mv4F3C43TA5YvLJZYHSCKpLu6BkUSZFIoS636%0D%0AzQ%0D%0A; uu=BCYl-X5aVhHcO6yDZM71uBuDWuq6cDkRSZSE3YKU6zr5bVfsIgko0aHjT2p31dM9yfCvaAXSItN-%0D%0A5mLpXBBf4jLtswgPlMgr0Wjlr3-XzUuLJY2YN7mFHcuikxhlu32TMqcXKHSqf8iSMP00wMjEegeB%0D%0AU44ekAiNukUhIzFMxmQ7t994oPrmz7dcIEx1eJ0utp1oV9-ctp1IgseWMFswwncE0SgWTmZMyf5c%0D%0AjvbrdRBzquC6WhenHmWCcl1Wd7rRNqR4k6G_HGfmda4_341DdC1kUw%0D%0A; sid=BCYhTRi_6HBDoCSnMCGip8Y4PzM-PcwnQ85HUBHsIC4B0ePDN3jrRrxoZBFMuWJ29ARXPEf6VHBu%0D%0AuJSBEU_HP78mLjui6XrAslBv8w5zWCJZ1hR5wZLHtPyZ2yny-U8e0X9RsGUTVQXQAxcVr1ZVppqq%0D%0ADw%0D%0A; csm-hit=tb:S7YDJY3ERA212P1FMYVF+s-6HPQZX1CQWFK7B0BFCT2|1539047882541&adb:adblk_no; pa=BCYnaFsPn5iLN00VjGUSDaAkYuba1mk2Vl2CGHrRA5f5KfrauxEp2gyIEMCzZdeO9Yghwk_ahNcQ%0D%0AHa_1-eT78vwecYuYaT8_ZPBE9A4kJkRzAGFJxXR3CC2YtC7xWP2Mury-%0D%0A",
          "Host": "pro.imdb.com",
          "Referer": "https://pro.imdb.com/title/tt0101318/details",
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest"}

def save_base_web(id , type ,text):
    new_dir = r'imdb_885_review/' + id
    # if not os.path.exists(new_dir):
    #     os.makedirs(new_dir)

    f_save = open(new_dir +"_"+type+ '.html' , 'w')
    f_save.write(text)
    f_save.close()

def change_date_format(temp_date):
    return datetime.strptime(temp_date , "%d %B %Y").strftime("%Y%m%d")

def insert_into_db(id , imdb_total_reviews_num , text):
    soup = BeautifulSoup(text , 'lxml')
    reviews_list = soup.find_all('div' , class_= 'imdb-user-review')

    for item in reviews_list:
        imdb_review_id = item.attrs['data-review-id']
        imdb_review_title = item.find('a',class_= 'title').text.strip()
        score = item.find('span' , class_= 'rating-other-user-rating')
        if score:
            imdb_have_score = 1
            imdb_score = int(score.find('span').text.strip())
        else:
            imdb_have_score = 0
            imdb_score = None
        warning = item.find('span', class_='spoiler-warning')
        if warning:
            imdb_spoiler_warning = 1
        else:
            imdb_spoiler_warning = 0
        temp_id = item.find('span',class_='display-name-link').find('a').attrs['href']
        imdb_review_user_id = cut_string(temp_id, '/' , 2 , 3)
        imdb_review_user_name = item.find('span',class_='display-name-link').find('a').text.strip()
        temp_date = item.find('span',class_= 'review-date').text.strip()
        imdb_review_date = change_date_format(temp_date)
        imdb_review_article = item.find('div',class_='content').text.strip()
        helpful_content = item.find('div' , class_= 'text-muted').text.strip()

        imdb_review_helpful_num = int(helpful_content[:helpful_content.find(' out of')].replace(',',''))
        imdb_review_all_num = int(helpful_content[helpful_content.find('out of') + 7 : helpful_content.find(' found this')].replace(',',''))
        temp_record = {'imdb_id':id,
                       'imdb_total_reviews_num': imdb_total_reviews_num,
                       'imdb_review_id': imdb_review_id,
                       'imdb_review_title': imdb_review_title,
                       'imdb_have_score': imdb_have_score,
                       'imdb_score': imdb_score,
                       'imdb_review_user_id': imdb_review_user_id,
                       'imdb_review_user_name': imdb_review_user_name,
                       'imdb_review_date': imdb_review_date,
                       'imdb_review_article': imdb_review_article,
                       'imdb_review_helpful_num': imdb_review_helpful_num,
                       'imdb_review_all_num': imdb_review_all_num,
                       'imdb_spoiler_warning': imdb_spoiler_warning,
                       }
        db.insert_dict(temp_record , 'imdb_885_review')
if __name__ == '__main__':
    db = Database()
    db.connect()
    imdb_id_list = db.get_imdb_885_id_list()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
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
    url = 'https://www.imdb.com/title/tt0099785/reviews'
    driver.get(url)
    cookie = [{'name': 'session-id', 'value': '147-5459322-5064541'},
              {'name': 'session-id-time', 'value': '2169945378'},
              {'name': 'ubid-main', 'value': '133-4085646-8424928'},
              {'name': 'session-token',
               'value': '1zzjEjQko3LXqAPuVIi4TDh3L0tOFvzTyH2mw3vgAk50zd/5cV2PyuoDpkax4PKPJZvcJJlc2JQLOXSqg0Z85LQGcRuexMCSZ1dkY28S++0sOFuaeJDzDSxzpYCF6jmemGc1q/DbsTv0IAvzjKYNKtwqDkpzpKJk+8W4QAS+iRdxJSskSe/OAVEToSzyhTH/2Z1AQCG4iZDqT5tUvrewVg=='},
              {'name': 'x-main', 'value': 'zA6uX9o5FkQufBoFdkajnZBacnL1E1XtC3v5BvUqJ9hv5SVTULG85cgTUVJLuLUr'},
              {'name': 'at-main',
               'value': 'Atza|IwEBILTopdmBPdErGAOQORsOqjZ-njYxCQzbPGo7Woww1hSk6HdKTygVyOCz7WZ9IJJDGY2UbJfuf9JsW7MczjKqqZoObfiYi2hw3pI0B0ifdLMCDc_3_QwNWK4UXwn8H-ynzeJjLoyWkLhbbanyEqlVVPstsbCui4Lsp6V6683y5Vo42D5yyovM1StPZtjCaAZQ7GSb5yXQ1MjwIWa223AwKFYiljFG3qiNLLU5ynuNHs2UoQM1QLfYe0Q1pogzSRjGvkyhWgXYPqPmrS0uvtCd8LghBz0PsLZxwW5sboonQF_jcZCIa3nf7QbS38AeQvkF22AMuMHqXagMZaMmK_TrOlhBuxJ7gVcqvvorecxfN78YpsyrMAzHJtCUhGdIerFF66ti6etpJ__FwEUu3lT_29_V'},
              {'name': 'sess-at-main', 'value': 'WzgDDX1d5b3b/VMpzOp2SC0GyKTKeTsYFeDZFRohgmo='},
              {'name': 'id',
               'value': 'BCYmj1Hpi-NT-W9qD13XNba4hWe8iPfYA2jW_olpspnZemkpIVoicpGT5T18MYpY0q4q8r6Y2D9F%0D%0At0fXLt8dIF3VACFCPESP4YffkoEKmpQwNn42oMo_1n8vWLgxGtyc36CoOLmL-gC1FJZ5hiU-tKHt%0D%0AMQ%0D%0A'},
              {'name': 'uu',
               'value': 'BCYsWrKUZaZMat5xS2jC5mQ6jHisbMYKizKXXpzztjHnUtzTzwqXrvg8Qag6oyqXCcVji_dLU6US%0D%0A0CN4wCV0b_r9HmAkiNzB5AhlnIrkvZ7RJRyieS6jXMO4ROyl2nTKyGCpwU-xtwoEHvN4piSzHZ4O%0D%0Az0-hlyxzPvVoREvOG3XCQw35_Dtp7A-Dz07jzzxapA8cd2y8i2sCNPz_YYvmXbq90jRe9rNwrDeI%0D%0AHW4xrfxG3OfsBT_mEHnorEu3rgZVv19qzQaFuDnokpTJwu097z3RsQ%0D%0A'},
              {'name': 'sid',
               'value': 'BCYkttSEyEUWGx1tbspY72pUTxhgP7Ze986ZxVxe4HNcEXk1LFfeo33NR7ZvG7UJWeNxlzNO2jD6%0D%0Ag8OpZVVKrV9peZnZFkwryYXs4WSxAmWV79G3YLMsrBPl2OIECtx5IqhPVW6SeoCMPd-AMbaYLTb9%0D%0AwA%0D%0A'},
              {'name': 'pa',
               'value': 'BCYrm4iOethLVcHPgKgOfRzU12I43f3_3iKY0dcfTiGDfTOI6u6gL6hiErqexfTSVNEwmCc-4DKL%0D%0A0YTX_LyfZAt11olk89zhkvyxEyk5NdJKipxn4TP0EeLBO8v4wfxvEV-4%0D%0A'},
              {'name': 'csm-hit',
               'value': 'tb:JVR7MH0XMBBYE90MHK1W+s-JVR7MH0XMBBYE90MHK1W|1539225491633&adb:adblk_no'},
              ]
    for item in cookie:
        driver.add_cookie(item)
    already_have_list = []
    for item in os.listdir('imdb_885_review/'):
        if '_' in item:
            already_have_list.append(item.split('_')[0])
    for id in imdb_id_list:
        if id not in already_have_list:
            #review
            type = 'reviews'
            url = 'https://www.imdb.com/title/' + id + '/' + type

            print("fighting_______" + id)
            driver.get(url)
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('load-more-data'))
            all_review_num = int(driver.find_element_by_xpath('//*[@id="main"]/section/div[2]/div[1]/div/span').text.split(' ')[0].replace(',', ''))
            print("there are " + str(all_review_num) + "results!!!!!")
            realtime_review_num = len(driver.find_elements_by_class_name('imdb-user-review'))
            print(realtime_review_num)
            load_more_flag = driver.find_element_by_class_name('load-more-data').get_attribute('data-key')
            while (load_more_flag):
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                load_more_element = driver.find_element_by_class_name('ipl-load-more__button')
                ActionChains(driver).click(load_more_element).perform()
                # WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('ipl-load-more__button'))
                realtime_review_num = len(driver.find_elements_by_class_name('imdb-user-review'))
                print('temp:' + str(realtime_review_num))
                print(all_review_num)
                load_more_flag = driver.find_element_by_class_name('load-more-data').get_attribute('data-key')
            save_base_web(id , type , driver.page_source)
            insert_into_db(id, all_review_num , driver.page_source)
            time.sleep(1)
            # driver.close()

    db.close()