from bs4 import BeautifulSoup
from tools import *

def crawl_website(db , id , text):
    detail_soup = BeautifulSoup(text , 'lxml')

    #title
    #example : Rain Man (1988)
    title_and_year = detail_soup.find('div', {'id': 'title_heading'}).find('span').text
    if "(" in title_and_year:
        title = title_and_year[:title_and_year.rindex('(') - 1].strip()

        # year
        year = title_and_year[title_and_year.rindex('(') + 1: -1]
    else:
        title = title_and_year
        year = ""

    # no website
    if detail_soup.select('#a-page > div.a-row > div > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-right > div.a-section.a-spacing-none.a-spacing-top-small > div > div > p'):
        return 0
    #offical_website
    category = detail_soup.select('#a-page > div.a-row > div > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-right > div.a-section.a-spacing-none.a-spacing-top-small > span')[0].text.strip()
    if category == 'Official web sites':
        table = detail_soup.select('#a-page > div.a-row > div > div > div.a-fixed-left-grid > div > div.a-fixed-left-grid-col.a-col-right > div.a-section.a-spacing-none.a-spacing-top-small')
        links = table[0].find('div').find_all('span' , class_ = 'a-list-item')
        for link in links:
            try:
                url = link.find('a').attrs['href'].strip()
                type = link.find('a').text.strip()
            except:
                url =""
                type = ""

            record = {"imdb_id": id,
                      "imdb_movie_title": title,
                      "imdb_website_type": type,
                      "imdb_website_url": url,

                      }
            table_name = 'imdb_movie_website_full'
            db.insert_dict(record , table_name)
            print(record)


