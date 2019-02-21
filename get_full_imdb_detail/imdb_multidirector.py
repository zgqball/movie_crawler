from datetime import datetime

from bs4 import BeautifulSoup


def get_date(raw_date):
    try:
        temp = datetime.strptime(raw_date , "%b %d, %Y")
        audience_date = temp.strftime("%Y-%m-%d")
    except:
        temp = datetime.strptime(raw_date, "%b %Y")
        audience_date = temp.strftime("%Y-%m")
    return audience_date

def cut_string(string , sub , start_num , end_num):
    temp = string.split(sub)
    result = ''
    for i in range(start_num , end_num):
        result = result + temp[i]
    return result

def crawl_movie_multidirector(db , id , text):
    detail_soup = BeautifulSoup(text , 'lxml')

    #director
    try:
        director_soup = detail_soup.select('#const_page_summary_section > div > div')[1]
        if "Director" in director_soup.text:
            directors = director_soup.find_all('a')
        director = ""
        director_id = ""
        for item in directors:
            director = item.text.strip()

            temp_id = item.attrs['href']
            director_id = cut_string(temp_id , '/' , 4 , 5)
            if director_id[:2] == 'tt':
                continue
            else:
                record = {"imdb_id": id,
                          "imdb_director": director,
                          "imdb_director_id": director_id,
                          }
                table_name = 'imdb_movie_director_full'
                db.insert_dict(record, table_name)
                print(record)
        director = director[:-2]
        director_id = director_id[:-2]
    except:
        director = ""
        director_id = ""




