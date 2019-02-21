from database_for_steaming import Database
import csv
from datetime import datetime
db = Database()
db.connect()

f_read = open('leaving_Netflix_url.csv' , 'r')
# f_read = open('raw_url.csv' , 'r')
month_url_dict = {}
csv_reader = csv.reader(f_read)
for item in csv_reader:
    # month = datetime.strptime(item[1] , '%m月-%y').strftime("%Y%m")
    month = item[1]
    month_url_dict[month] = item[2]
# f_read_manual = open('manual_copy.csv' , 'r')
f_read_manual = open('manual_copy_leaving.csv' , 'r')
csv_reader = csv.reader(f_read_manual)
for item in csv_reader:
    month = item[1][:6]
    url = month_url_dict[month]
    if item[2] == '1':
        show_type = 'movie'
    elif item[2] == '2':
        show_type = 'tv show'
    else:
        show_type = ''
    record = {'streaming_website_source_name': 'vulture',
              'streaming_website_url': url,
              'streaming_show_from': 'Netflix',
              'streaming_show_name': item[0],
              'streaming_show_date': item[1],
              'streaming_show_type': show_type,
              }
    # db.insert_dict(record, 'streaming_coming')
    db.insert_dict(record, 'streaming_leaving')
    print(record)


db.close()