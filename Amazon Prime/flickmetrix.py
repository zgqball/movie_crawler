import datetime
import multiprocessing
import urllib

import requests
from database import Database
import json
from tool import logger


class get_etf_data(object):
    def __init__(self):
        self.root_url = 'https://flickmetrix.com/api/values/getFilms?amazonRegion=us&cast=&comboScoreMax=100&comboScoreMin=0&countryCode=hk&deviceID=1&director=&genreAND=false&imdbRatingMax=10&imdbRatingMin=0&imdbVotesMax=1600000&imdbVotesMin=0&inCinemas=true&includeDismissed=false&includeSeen=false&includeWantToWatch=false&isCastSearch=false&isDirectorSearch=false&language=all&letterboxdScoreMax=100&letterboxdScoreMin=0&letterboxdVotesMax=1400000&letterboxdVotesMin=0&metacriticMax=100&metacriticMin=0&netflixRegion=hk&onAmazonPrime=true&onAmazonVideo=false&onDVD=false&onNetflix=false&pageSize=20&plot=&popularityMax=100&popularityMin=0&queryType=GetFilmsToSieve&rtCriticFreshMax=300&rtCriticFreshMin=0&rtCriticMeterMax=100&rtCriticMeterMin=0&rtCriticRatingMax=10&rtCriticRatingMin=0&rtCriticReviewsMax=400&rtCriticReviewsMin=0&rtCriticRottenMax=200&rtCriticRottenMin=0&rtUserMeterMax=100&rtUserMeterMin=0&rtUserRatingMax=5&rtUserRatingMin=0&rtUserReviewsMax=40000000&rtUserReviewsMin=0&searchTerm=&sortOrder=dateDesc&title=&token=&watchedRating=0&writer=&yearMax=2019&yearMin=1900&currentPage='
        self.header = {'Accept': 'application/json, text/plain, */*',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
                       'Connection': 'keep-alive',
                       'Content-Length': '41',
                       'Content-Type': 'application/json',
                       'Cookie': '_ga=GA1.2.1824641935.1550714574; _gid=GA1.2.90579370.1550714574',
                       'Host': 'flickmetrix.com',
                       'Origin': 'https://etfdb.com',
                       'Referer': 'https://flickmetrix.com/',
                       'Response': 'application/json',
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       # 'X-NewRelic-ID': 'VQMAUFRXGwIIVVJXAgU='
                       }

    def spilt_data_by_name_and_insert(self , data , database , table_name):
        for item in data:
            item['record_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            spilt_attribute_list = ['name', 'symbol', 'category_name', 'complete', 'issuer_display_name', 'advanced','commission_free',
                                    'chart', 'etf_holdings', 'fact_sheet',
                                    'head_to_head', 'home_page_url']
            for attr in spilt_attribute_list:
                if attr in item.keys():
                    temp_detail = item.pop(attr)
                    item[attr + '_text'] = temp_detail['text']
                    item[attr + '_type'] = temp_detail['type']
                    item[attr + '_url'] = temp_detail['url']
            database.insert_dict(item , table_name)

    def get_data(self):
        db = Database()
        db.connect()
        for tab in self.tab_list:
            #因为mysql的命名不能用「-」
            if '-' in tab:
                temp_tab = tab.replace('-', '_')
            else:
                temp_tab = tab
            table_name = 'etf_' + temp_tab
            url = self.root_url
            first_body = {
                    "tab": tab,
                    "only": ["meta","data"],
                }
            re = requests.post(url,headers = self.header , data = json.dumps(first_body)).json()
            #meta 表示返回的数据概要
            total_pages = re['meta']['total_pages']
            #把第一次返回的内容写进数据库
            logger.info("{} has total {} pages!!".format(tab , total_pages))
            logger.info("getting {} page {} data".format(tab, '1'))
            self.spilt_data_by_name_and_insert(re['data'] , db , table_name)

            for i in range(2 , total_pages + 1):
                logger.info("getting data of {}--page {} / {}".format(tab, str(i) , str(total_pages)))
                payload = {
                    "page":str(i),
                    "tab": tab,
                    "only": ["meta","data"],
                }
                re = requests.post(url, headers=self.header, data=json.dumps(payload)).json()
                self.spilt_data_by_name_and_insert(re['data'], db, table_name)
        db.close()

    def single_tab_work(self , tab):
        db = Database()
        db.connect()
        # 因为mysql的命名不能用「-」
        if '-' in tab:
            temp_tab = tab.replace('-', '_')
        else:
            temp_tab = tab
        table_name = 'etf_' + temp_tab
        url = self.root_url
        first_body = {
                "tab": tab,
                "only": ["meta","data"],
            }
        re = requests.post(url,headers = self.header , data = json.dumps(first_body)).json()
        #meta 表示返回的数据概要
        total_pages = re['meta']['total_pages']
        #把第一次返回的内容写进数据库
        logger.info("{} has total {} pages!!".format(tab , total_pages))
        logger.info("getting {} page {} data".format(tab, '1'))
        self.spilt_data_by_name_and_insert(re['data'] , db , table_name)

        for i in range(2 , total_pages + 1):
            logger.info("getting data of {}--page {} / {}".format(tab, str(i) , str(total_pages)))
            payload = {
                "page":str(i),
                "tab": tab,
                "only": ["meta","data"],
            }
            re = requests.post(url, headers=self.header, data=json.dumps(payload)).json()
            self.spilt_data_by_name_and_insert(re['data'], db, table_name)
        db.close()

    def multi_work_by_tabs(self):
        tab_num = len(self.tab_list)
        pool = multiprocessing.Pool(processes=tab_num)
        pool.map(self.single_tab_work, self.tab_list)
        pool.close()
        pool.join()

    def test_request(self):
        page = 1
        url = self.root_url + str(page)
        re = requests.get(url , headers = self.header)
        print(re.text)

if __name__ == '__main__':
    ETF = get_etf_data()
    #单进程
    # ETF.get_data()
    #多进程 基于多少个tab
    ETF.test_request()


