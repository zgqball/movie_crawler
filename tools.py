from datetime import datetime


def get_date(raw_date):
    try:
        temp = datetime.strptime(raw_date , "%b %d, %Y")
        new_date = temp.strftime("%Y-%m-%d")
    except:
        temp = datetime.strptime(raw_date, "%b %Y")
        new_date = temp.strftime("%Y-%m")
    return new_date


def cut_string(string , sub , start_num , end_num):
    temp = string.split(sub)
    result = ''
    for i in range(start_num , end_num):
        result = result + temp[i]
    return result