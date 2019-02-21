import tools
import csv
from database_for_steaming import Database
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def deal_with_date(year , date_text):
    if 'Sept' in date_text:
        date_text = date_text.replace('Sept' , 'Sep')
    # if 'August' in date_text:
    #     date_text = date_text.replace('August' , 'Aug.')
    if ':' in date_text:
        date_text = date_text.replace(':' , '')
    if '.' in date_text:
        temp = datetime.strptime(date_text , '%b. %d').strftime('%m%d')
    else:
        print(date_text)
        temp = datetime.strptime(date_text.strip(), '%B %d').strftime('%m%d')

    return year + temp


def crawl_one_page(url):
    year = month[:4]
    re = requests.get(url)
    soup = BeautifulSoup(re.text , 'lxml')
    website_title = soup.find('h1').text.strip()
    print(website_title)
    contents_of_month = soup.find('div' , class_= 'article-body-content')
    #different page type
    if contents_of_month.find('h3'):
        contents_of_month = contents_of_month.contents
        effect_table = ''
        begin_flag = 0
        for i in range(len(contents_of_month)):
            if contents_of_month[i].name == 'h3' and effect_table == '':
                #switch to coming
                effect_table = 'streaming_coming'
            elif contents_of_month[i].name == 'h3' and effect_table == 'streaming_coming':
                # switch to close
                effect_table = 'streaming_leaving'
            else:
                if effect_table != "":
                    if (contents_of_month[i].name == 'h2' or contents_of_month[i].name == 'h4') and (contents_of_month[i].find('strong') or contents_of_month[i].find('b') ):
                        # new_date
                        if contents_of_month[i].find('strong'):
                            if contents_of_month[i].find('strong').text != '' and 'Follow Peggy' not in contents_of_month[i].find('strong').text:
                                begin_flag = 1
                                temp_date = contents_of_month[i].text
                                new_date = deal_with_date(year, temp_date)
                        elif contents_of_month[i].find('b'):
                            if contents_of_month[i].find('b').text != '' and 'Follow Peggy' not in contents_of_month[i].find('b').text:
                                begin_flag = 1
                                temp_date = contents_of_month[i].text
                                new_date = deal_with_date(year, temp_date)
                    else:
                        if begin_flag == 1 and contents_of_month[i].name == 'p':
                            ems = contents_of_month[i].find_all('em')
                            if len(ems) > 1:
                                for j in range(len(contents_of_month[i].contents)):
                                    if contents_of_month[i].contents[j].name == 'em':
                                        is_origin = 0
                                        show_title = contents_of_month[i].contents[j].text.strip()
                                        if j < len(contents_of_month[i].contents) - 1:
                                            if '—' in contents_of_month[i].contents[j+1] and 'Original' in contents_of_month[i].contents[j+1]:
                                                # show_title = show_title.split('-')[0]
                                                is_origin = 1
                                        if show_title == '':
                                            continue
                                        else:
                                            record = {'streaming_website_source_name': stream_source,
                                                      'streaming_website_url': url,
                                                      'streaming_title': website_title,
                                                      'streaming_show_from': 'Netflix',
                                                      'streaming_show_name': show_title,
                                                      'streaming_show_is_original': is_origin,
                                                      'streaming_show_date': new_date,
                                                      }
                                            db.insert_dict(record, effect_table)
                                            print(record)
                            else:
                                is_origin = 0
                                show_title = contents_of_month[i].text.strip()
                                if '—' in show_title and 'Original' in show_title:
                                    show_title = show_title.split('-')[0]
                                    is_origin = 1
                                if show_title == '':
                                    continue
                                else:
                                    record = {'streaming_website_source_name' : stream_source,
                                              'streaming_website_url': url,
                                              'streaming_title': website_title,
                                              'streaming_show_from': 'Netflix',
                                              'streaming_show_name': show_title,
                                              'streaming_show_is_original': is_origin,
                                              'streaming_show_date': new_date,
                                            }
                                    db.insert_dict(record , effect_table)
                                    print(record)
    else:
        contents_of_month = contents_of_month.contents
        effect_table = ''
        begin_flag = 0
        for i in range(len(contents_of_month)):
            if contents_of_month[i].name == 'h4' and effect_table == '' and ('Netflix' in contents_of_month[i].text or 'NETFLIX' in contents_of_month[i].text):
                #switch to coming
                effect_table = 'streaming_coming'
            elif contents_of_month[i].name == 'h4' and effect_table == 'streaming_coming':
                # switch to close
                effect_table = 'streaming_leaving'
            else:
                if effect_table != "":
                    if contents_of_month[i].name == 'p' and (contents_of_month[i].find('strong') or contents_of_month[i].find('b') ):
                        # new_date
                        if contents_of_month[i].find('strong'):
                            if contents_of_month[i].find('strong').text != '' and 'Follow Peggy' not in \
                                    contents_of_month[i].find('strong').text:
                                begin_flag = 1
                                temp_date = contents_of_month[i].text
                                new_date = deal_with_date(year, temp_date)
                        elif contents_of_month[i].find('b'):
                            if contents_of_month[i].find('b').text != '' and 'Follow Peggy' not in contents_of_month[i].find('b').text:
                                begin_flag = 1
                                temp_date = contents_of_month[i].text
                                new_date = deal_with_date(year, temp_date)
                    else:

                        if begin_flag == 1 and contents_of_month[i].name == 'p':
                            ems = contents_of_month[i].find_all('em')
                            if len(ems) > 1:
                                for j in range(len(contents_of_month[i].contents)):
                                    if contents_of_month[i].contents[j].name == 'em':
                                        is_origin = 0
                                        show_title = contents_of_month[i].contents[j].text.strip()
                                        if j < len(contents_of_month[i].contents) - 1:
                                            if '—' in contents_of_month[i].contents[j+1] and 'Original' in contents_of_month[i].contents[j+1]:
                                                # show_title = show_title.split('-')[0]
                                                is_origin = 1
                                        if show_title == '':
                                            continue
                                        else:
                                            record = {'streaming_website_source_name': stream_source,
                                                      'streaming_website_url': url,
                                                      'streaming_title': website_title,
                                                      'streaming_show_from': 'Netflix',
                                                      'streaming_show_name': show_title,
                                                      'streaming_show_is_original': is_origin,
                                                      'streaming_show_date': new_date,
                                                      }
                                            db.insert_dict(record, effect_table)
                                            print(record)
                            else:
                                is_origin = 0
                                show_title = contents_of_month[i].text.strip()
                                if '—' in show_title and 'Original' in show_title:
                                    show_title = show_title.split('—')[0]
                                    is_origin = 1
                                if show_title == '':
                                    continue
                                else:
                                    record = {'streaming_website_source_name' : stream_source,
                                              'streaming_website_url': url,
                                              'streaming_title': website_title,
                                              'streaming_show_from': 'Netflix',
                                              'streaming_show_name': show_title,
                                              'streaming_show_is_original': is_origin,
                                              'streaming_show_date': new_date,
                                            }
                                    db.insert_dict(record , effect_table)
                                    print(record)

if __name__ == '__main__':
    db = Database()
    db.connect()
    f = open('cosmopolitan.csv' , 'r')
    csv_reader = csv.reader(f)
    stream_source = 'cosmopolitan'
    for item in csv_reader:
        month = item[0]
        url = item[1]
        # crawl_one_page(url)
        # except:
        #     print(url)
        try:
            crawl_one_page(url)
        except:
            print(url)

    db.close()