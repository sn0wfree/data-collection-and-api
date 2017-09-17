# -*- coding:utf-8 -*-
import os
import platform

import time

import requests_cache


import pandas as pd
import re
import gc
import csv
import numpy as np
from pandas import DataFrame
import sys
import json
import urllib
from datetime import datetime
import requests


class Pointer():

    def __init__(self, obj):
        self.obj = obj

    def get(self):
        return self.obj

    def set(self, obj):
        self.obj = obj


__status__ = Pointer(0)


def statuscheck(__status__):

    if __status__.get() == 0:
        print 'Will Stop'
        __status__.set(0)

    else:
        pass
    return __status__.get()


def get_data(bucket_start_date, bucket_end_date, keywords, category=7):
    geo = ''

    bucket_start_date_printed = datetime.strftime(
        bucket_start_date, '%Y-%m-%d')
    bucket_end_date_printed = datetime.strftime(bucket_end_date, '%Y-%m-%d')
    time_formatted = '+'.join([bucket_start_date_printed,
                               bucket_end_date_printed])
    comparisonItem = [
        {'keyword': kw, 'time': time_formatted, 'geo': geo} for kw in keywords]

    req = {"comparisonItem": comparisonItem,
           "category": category, "property": ""}
    hl = "en-GB"
    tz = "-120"

    explore_URL = 'https://trends.google.com/trends/api/explore?hl={0}&tz={1}&req={2}'.format(
        hl, tz, json.dumps(req).replace(' ', '').replace('+', ' '))
    # print explore_URL
    return requests.get(explore_URL).text


def get_token(response_text):
    try:
        return response_text.split('token":"')[1].split('","')[0]
    except:
        raise 'invaild get token request'
        return None


def get_csv_request(response_text):
    try:
        return response_text.split('"widgets":')[1].split(',"lineAnno')[0].split('"request":')[1]
    except:
        raise 'invaild get csv request'
        return None


def get_csv(response_text):
    request = get_csv_request(response_text)

    # print request
    token = get_token(response_text)

    csv = requests.get(
        'https://www.google.com/trends/api/widgetdata/multiline/csv?req={0}&token={1}&tz=-120'.format(request, token))
    # print csv.text.encode('utf8')
    return csv.text.encode('utf8')


def parse_csv(csv_contents, keywords):
    lines = csv_contents.split('\n')
    datas = lines[3:-1]

    col = lines[2].split(',')
    for colnumber in xrange(len(col)):

        if ': (Worldwide)' in col[colnumber]:
            col[colnumber] = col[colnumber].split(': (Worldwide)')[0]
        else:
            pass
        locals()[col[colnumber]] = []

    df = pd.DataFrame(columns=col)

    # Delete top 3 lines
    for data in datas:
        for columnnumber in xrange(len(col)):
            locals()[col[columnnumber]].append(
                data.split(',')[columnnumber])
    for columnnumber in xrange(len(col)):
        df[col[columnnumber]] = locals()[col[columnnumber]]
    return df


def read_a_file(file):
    with open(file, 'r') as f:
        f_collected = f.readlines()
    return f_collected


def ImportListInfobyFile(locals_file_path, target=False, GUI=False):
    keywords = []
    scan_files = os.listdir(locals_file_path)
    if target != False:

        with open(target, 'r') as ticker:
            ticker = ticker.readlines()
            for line in ticker:
                keywords.append(line.strip())

    else:

        if 'keywords.txt' in scan_files:
            fi = read_a_file('keywords.txt')
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif 'keywords2.txt' in scan_files:
            fi = read_a_file('keywords2.txt')
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif 'keywords.csv' in scan_files:
            fi = pd.read_csv('keywords.csv')
            keywords = fi['tinker']
        else:
            keywords = 0
            raise ValueError('unexpected keywords')

    return keywords


def HandleGTs(start_date, end_date, keywords, category):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    resp_text = get_data(start_date_dt, end_date_dt, keywords, category)
    # print resp_text
    df = parse_csv(get_csv(resp_text), keywords)
    return df


def findoperation():
    OperationSystem = platform.system()
    if OperationSystem is 'Darwin':
        link = '/'
    elif OperationSystem is 'Windows':
        link = '\\'
    else:
        link = '/'
    return link


def DateProduce(begindate):
    begindate = str(begindate)
    if len(begindate) == 4:
        beginyear = begindate
        return yearonly(beginyear)
    elif len(begindate) >= 6:
        beginyear = begindate[0:4]
        beginmonth = begindate[4:6]
        return yearandmonth(beginyear, beginmonth)


def ChangeInt2StrDay(date):
    if int(date) < 10:
        day = '0' + str(int(date))
    else:
        day = str(int(date))
    return day


def getDays(year, month):
    year = int(year)
    month = int(month)
    day = 31  # 定义每月最多的天数
    while day:
        # print day
        try:
            time.strptime('%d-%d-%d' % (year, month, day),
                          '%Y-%m-%d')  # 尝试将这个月最大的天数的字符串进行转化
            break

        except:
            day -= 1  # 否则将天数减1继续尝试转化, 直到成功为止
    return day  # 成功时返回得就是这个月的天数


def yearandmonth(beginyear, beginmonth):
    da = []
    if int(beginyear) < datetime.now().year:
        years = range(int(beginyear), datetime.now().year + 1, 1)
        da = yearonly(int(beginyear) + 1)
        if int(beginmonth) <= datetime.now().month:
            if int(beginmonth) <= 6:

                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-06-30'))
                da.append((str(beginyear) + '-07-01',
                           str(beginyear) + '-12-31'))
            else:

                da.append((str(beginyear) + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-12-31'))

        else:
            raise ValueError('Wrong month, you choose the future month')

    elif int(beginyear) == datetime.now().year:

        if int(beginmonth) <= datetime.now().month:
            if int(beginmonth) <= 6 and datetime.now().month <= 6:

                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-0' + ChangeInt2StrDay(datetime.now().month) + '-' + ChangeInt2StrDay(datetime.now().day)))

            elif int(beginmonth) <= 6 and datetime.now().month > 6:
                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) +
                           '-01', str(beginyear) + '-06-30'))

                da.append((str(beginyear) + '-07-01',
                           str(beginyear) + '-0' + ChangeInt2StrDay(datetime.now().month) + '-' + ChangeInt2StrDay(datetime.now().day)))
            elif int(beginmonth) > 6:
                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-0' + ChangeInt2StrDay(datetime.now().month) + '-' + ChangeInt2StrDay(datetime.now().day)))

        else:
            raise ValueError('Wrong month, you choose the future month')

    else:
        raise ValueError('Wrong year, you choose the future year')
    return da


def yearonly(beginyear):
    da = []
    # years = [int(beginyear) + i for i in range(14)]

    if int(beginyear) < datetime.now().year:
        years = range(int(beginyear), datetime.now().year + 1, 1)
    elif int(beginyear) == datetime.now().year:
        years = [datetime.now().year]
    else:
        raise ValueError('Wrong year, you choose the future year')

    for year in years:
        if year == datetime.now().year:
            if datetime.now().month <= 6:
                da.append((str(year) + '-01-01', str(year) +
                           '-%d-%d' % (datetime.now().month, datetime.now().day)))
            else:
                da.append((str(year) + '-01-01', str(year) + '-06-30'))

                da.append((str(year) + '-07-01', str(year) +
                           '-%d-%d' % (datetime.now().month, datetime.now().day)))

        elif year < datetime.now().year:
            da.append((str(year) + '-01-01', str(year) + '-06-30'))
            da.append((str(year) + '-07-01', str(year) + '-12-31'))
        else:
            raise ValueError('Unexpected year, you choose the future year')

    return da


def DateProduce_back(beginyear):
    current_year = datetime.now().year
    if current_year < beginyear:
        raise 'Wrong year, the begin year is less than current year'

    else:
        pass
    da = []
    years = xrange(beginyear, current_year + 1)
    for year in years:

        if year == current_year:
            stryear = str(current_year)
            if year % 2 == 1:
                date1 = (stryear + '-05-01',
                         datetime.now().date().strftime('%Y-%m-%d'))
                da.append(date1)

            elif year % 2 == 0:
                if datetime.datetime.now().mouth < 9:
                    date1 = (stryear + '-01-01',
                             ddatetime.now().date().strftime('%Y-%m-%d'))
                    da.append(date1)
                else:
                    date1 = (stryear + '-01-01', stryear + '-08-31')
                    date2 = (stryear + '-09-01',
                             datetime.now().date().strftime('%Y-%m-%d'))
                    da.append(date1)
                    da.append(date2)

        elif year != current_year:
            stryear = str(year)
            if year % 2 == 1:
                date1 = (stryear + '-05-01', stryear + '-12-31')

                da.append(date1)

            elif year % 2 == 0:
                date1 = (stryear + '-01-01', stryear + '-08-31')
                date2 = (stryear + '-09-01', str(year + 1) + '-04-30')
                da.append(date1)
                da.append(date2)
    return da


def read_ticker(tickerfile):
    tic = []
    with open(tickerfile, 'r') as ticker:
        ticker = ticker.readlines()
        for line in ticker:
            tic.append(line.strip())
    return tic


def chunks(target, n):
    if isinstance(target, list):
        date1 = [target[i:i + n] for i in xrange(0, len(target), n)]
    else:
        date1 = []
        raise ValueError, "Wrong type,I need a list."
    return date1


def spe(keywords):
    keywords_sep_list = chunks(keywords, 1003)
    for l in xrange(len(keywords_sep_list)):
        locals()[str(l)] = da + '/%s.txt' % str(l + 1)
        write_txt(keywords_sep_list[l], locals()[str(l)])


def write_txt(fi, targetpath):
    with open(targetpath, 'w') as f:
        for ff in fi:
            f.write(ff + '\n')


def scraGoogleTrends_2yearPeriod(date, keywords,  category=7):
    if category == 7:
        df = [HandleGTs(dt[0], dt[1], keywords, 7) for dt in date]
    else:
        df = [HandleGTs(dt[0], dt[1], keywords, category) for dt in date]

    # return pd.concat([df_temp0, df_temp1, df_temp2])
    return pd.concat(df)


def makedirs(names, path, link):
    if isinstance(names, list):
        for name in names:
            directory = path + link + name
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                pass

    elif isinstance(names, str):
        directory = path + link + names
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            pass


def downlaod(dates, keywords, link, locals_file_path, category=7):
    if category == 7:
        df_list = [scraGoogleTrends_2yearPeriod(
            date, keywords, 7) for date in dates]
    else:
        df_list = [scraGoogleTrends_2yearPeriod(
            date, keywords, category) for date in dates]

    target_pd = pd.concat(df_list).T

    filename = ''.join(keywords)

    savepath = locals_file_path + link + 'data' + link + filename + '.csv'
    # print savepath
    target_pd.to_csv(savepath, header=False)


def progress_test(counts, lenfile, speed):
    bar_length = 20

    process = counts / float(lenfile)

    ETA = speed * (lenfile - counts) / float(60)
    hashes = '#' * int(process * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|completed %d * projects|Speed : %.4f s/ projects|ETA: %s min""" %
                     (process * 100, hashes + spaces, counts, speed, ETA))

    sys.stdout.flush()


def main(target, category, dates):
    gc.enable()
    requests_cache.install_cache(
        cache_name="googletrends_request_cache", backend="sqlite", expire_date=300)

    link = findoperation()

    locals_file_path = os.path.split(os.path.realpath(__file__))[0]
    target = locals_file_path + link + 'keywords.txt'
    keywords = ImportListInfobyFile(locals_file_path, target)
    makedirs('data', locals_file_path, link)
    if dates == False:
        dates = chunks(DateProduce(2004), 3)
    else:
        dates = chunks(DateProduce(2004), 3)
    if category != 7:
        category = category
    else:
        category = 7

    # keywords = ['FDEF', 'FFBC' ,'THFF' ,'FFIN' ,'FFNW']
    #key = chunks(keywords, 1)
    key = chunks(keywords, 1)
    uncompleted_keywords = keywords

    # print key
    l_orign = len(key)
    l = l_orign
    count = 0
    request_time = 1

    for keyword in key:
        f = time.time()
        abnorl = True
        if statuscheck(__status__) == 0:
            break
        else:
            pass

        # downlaod(dates,keywords,link,locals_file_path)

        while abnorl:

            try:

                downlaod(dates, keyword, link, locals_file_path, category)
            except Exception as e:
                print e
                request_time = request_time + 1
                time.sleep(30)
                if request_time > 10:
                    raise 'Quota limit'

            else:
                request_time = 1
                break

        time.sleep(1)
        count = count + 1
        workingtime = time.time() - f
        if workingtime <= 60:
            time.sleep(5)
        else:
            time.sleep(1)
        if count > 50:
            count = 0
            time.sleep(10)
        else:
            pass
        closingtime = time.time() - f
        l = l - 1
        speed = closingtime
        for keyword in keywords:
            uncompleted_keywords.remove(keyword)
            write_txt(uncompleted_keywords, target)
        gc.collect()

        progress_test(l_orign - l, l_orign, speed)
    if statuscheck(__status__) == 0:
        print 'Interrupted'
    else:
        print 'download finished'
        __status__.set(0)


if __name__ == '__main__':
    dates, keyword, link, locals_file_path, category = 2004, 'ORI', '/', '/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/Source', 7
    # main()
    downlaod(dates, keyword, link, locals_file_path, category)
