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

def work(year , start_id):
    moviemeter_stage = []
    for i in range(start_id, 1200000, 50000):
        moviemeter_stage.append(str(i) + "-" + str(i + 50000))
    moviemeter_stage.append("1200000-")
    years = list(range(year, year+1))
    for year in years[::-1]:
        year = str(year)
        new_dir = r'imdb_whole_year_movie_backup/' + year + '/'
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        print("downloading________" + year)
        for stage in moviemeter_stage:
            print("fighting_______" + stage)
            url = "https://pro.imdb.com/inproduction/development?ref_=hm_nv_tt_rel#type=movie&status=RELEASED&movieMeter=" + stage + "&year=" + year + "-" + year
            print(url)
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
            options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
            driver = webdriver.Chrome(chrome_options=options)
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
                      {'name': 'csm-hit', 'value': 'tb:JVR7MH0XMBBYE90MHK1W+s-JVR7MH0XMBBYE90MHK1W|1539225491633&adb:adblk_no'},
            ]
            for item in cookie:
                driver.add_cookie(item)

            driver.get(url)
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('total_item_count'))
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
    for year in range(1916 , 1915 , -1):

        #1916 700000-750000
        start_id = 700000
        work(year , start_id)
        get_id(year)
