from bs4 import BeautifulSoup
from tools import *

def crawl_cast(db , id , text):
    detail_soup = BeautifulSoup(text , 'lxml')

    #title
    #example : Rain Man (1988)
    title_and_year = detail_soup.find('div' , {'id':'title_heading'}).find('span').text
    if "(" in title_and_year:
        title = title_and_year[:title_and_year.rindex('(') - 1].strip()
    else:
        title = title_and_year

    #cast_name and cast_id
    try:
        cast_list = detail_soup.find("table" , id = 'title_cast_sortable_table').find_all('tr')[1:]
    except:
        return 0
    sequence = 0
    for cast in cast_list:
        #name and id
        try:
            cast_name = cast.find_all('a')[1].text.strip()
        except:
            cast_name = ""
        try:
            cast_id = cut_string(cast.find_all('a')[1].attrs['href'] , '/' , 4 , 5)
        except:
            cast_id = ""

        # role
        try:
            role = cast.find('span' , class_= 'see_more_text_expanded').text[:-10].strip()
        except:
            role = ""

        sequence += 1

        # moviestarmeter
        try:
            starmeter = cast.find('td' , class_= 'a-text-right').text.strip()
        except:
            starmeter = ""

        # known_for
        title_and_year = cast.find('td' , class_= 'a-text-left').text.strip()
        if "(" in title_and_year:
            known_for = title_and_year[:title_and_year.rindex('(') - 1].strip()

            # year
            known_for_year = title_and_year[title_and_year.rindex('(') + 1: -1]
        else:
            known_for = title_and_year

            known_for_year = ""

        # known_for_id
        try:
            known_for_id = cast.find('td' , class_= 'a-text-left').find('a').attrs['href']
            known_for_id = cut_string(known_for_id , '/' , 4 , 5)
        except:
            known_for_id = ""

        record = {"imdb_id": id,
                  "imdb_movie_title": title,
                  "imdb_cast_name": cast_name,
                  "imdb_cast_id": cast_id,
                  "imdb_cast_role": role,
                  "imdb_cast_sequence": sequence,
                  "imdb_star_meter": starmeter,
                  "imdb_known_for": known_for,
                  "imdb_known_for_year": known_for_year,
                  "imdb_known_for_movie_id": known_for_id,
                  }
        table_name = 'imdb_movie_cast'
        db.insert_dict(record , table_name)
        print(record)


