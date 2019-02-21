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

def crawl_movie_detail(db , id , text):
    detail_soup = BeautifulSoup(text , 'lxml')

    #title
    #example : Rain Man (1988)
    title_and_year = detail_soup.find('div' , {'id':'title_heading'}).find('span').text

    if "(" in title_and_year:
        title = title_and_year[:title_and_year.rindex('(') - 1].strip()

        #year
        year = title_and_year[title_and_year.rindex('(') + 1 : -1]
    else:
        title = title_and_year
        year = ""

    #rating
    try:
        rating = detail_soup.find('span' , id = 'certificate').text.strip()
    except:
        rating =""

    #genre
    try:
        genre = detail_soup.find('span' , id = 'genres').text.strip()
    except:
        genre = ""

    #release_date and area
    try:
        release_date_and_area = detail_soup.find('div' , class_ = 'a-row a-spacing-base').text.replace('\n' ," ").strip()
        if "(" in release_date_and_area:
            release_date = release_date_and_area[:release_date_and_area.rindex('(') - 1].strip()
            release_date = get_date(release_date)
            release_area = release_date_and_area[release_date_and_area.rindex('(') + 1 : -1]
        else:
            release_date = release_date_and_area
            release_area = ""
    except:
        release_date = ""
        release_area = ""


    #director
    try:
        director_soup = detail_soup.select('#const_page_summary_section > div > div')[1]
        if "Director" in director_soup.text:
            directors = director_soup.find_all('a')
        director = ""
        director_id = ""
        for item in directors:
            temp = item.text.strip()

            temp_id = item.attrs['href']
            director_id = director_id + cut_string(temp_id , '/' , 4 , 5) + ', '
            director = director + temp + ', '
        director = director[:-2]
        director_id = director_id[:-2]
    except:
        director = ""
        director_id = ""

    #country_of_origin and language
    release_detail =detail_soup.find_all('tr' , class_ = 'release_details_item')
    country_of_origin = release_detail[0].find('td').text.strip()
    language = release_detail[1].find('td').text.strip()

    #runtime
    try:
        runtime = detail_soup.find('span' , id = 'running_time').text.strip()
    except:
        runtime = ""

    #budget
    try:
        budget = detail_soup.find('div' ,{'class':"budget_summary"}).text.replace('\n'," ")[9:].strip()
    except:
        budget = ""

    #opening_weekend
    try:
        opening_weekend = detail_soup.find('div' ,{'class':"opening_wknd_summary"}).text.replace('\n'," ")[15:].strip()
    except:
        opening_weekend =""

    #us_gross
    try:
        us_gross = detail_soup.find('div' ,{'class':"gross_usa_summary"}).text.replace('\n'," ")[13:].strip()
    except:
        us_gross = ""

    # world_gross
    try:
        world_gross = detail_soup.find('div', {'class': "gross_world_summary"}).text.replace('\n', " ")[15:].strip()
    except:
        world_gross = ""

    # plot_summary
    try:
        plot_summary = detail_soup.find('div', {'id': "plot_summaries"}).text.replace('\n', " ")[15:].strip()
    except:
        plot_summary =""

    # synopsis
    try:
        synopsis = detail_soup.find('div', {'id': "synopsis"}).text.replace('\n', " ")[11:].strip()
    except:
        synopsis = ""

    # production_company and Distributor
    try:
        production_company_and_Distributor = detail_soup.select('#contacts > div > div.a-section.a-spacing-top-mini > ul > li > span > div > span > span > span > a')
        production_company = production_company_and_Distributor[0].text.strip()
        production_company_id = cut_string(production_company_and_Distributor[0].attrs['href'] , '/' , 4 , 5)
    except:
        production_company = ""
        production_company_id = ""
    try:
        distributor = production_company_and_Distributor[1].text.strip()
        distributor_id = cut_string(production_company_and_Distributor[1].attrs['href'], '/', 4, 5)
    except:
        distributor = ""
        distributor_id = ""

    record = {"imdb_id": id,
              "imdb_movie_title": title,
              "imdb_year": year,
              "imdb_rating": rating,
              "imdb_genres": genre,
              "imdb_release_date": release_date,
              "imdb_release_area": release_area,
              "imdb_director": director,
              "imdb_director_id": director_id,
              "imdb_country_of_origin": country_of_origin,
              "imdb_language": language,
              "imdb_runtime": runtime,
              "imdb_budget": budget,
              "imdb_us_opening_weekend_gross": opening_weekend,
              "imdb_us_overall_gross": us_gross,
              "imdb_worldwide_overall_gross": world_gross,
              "imdb_plot_summary": plot_summary,
              "imdb_synopsis": synopsis,
              "imdb_production_company": production_company,
              "imdb_production_company_id": production_company_id,
              "imdb_distributor": distributor,
              "imdb_distributor_id": distributor_id,
              }
    table_name = 'imdb_movie_detail_full'
    db.insert_dict(record , table_name)
    print(record)


