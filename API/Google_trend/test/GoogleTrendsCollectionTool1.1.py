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





def get_data(bucket_start_date, bucket_end_date, keywords):
    geo=''

    bucket_start_date_printed = datetime.strftime(bucket_start_date, '%Y-%m-%d')
    bucket_end_date_printed = datetime.strftime(bucket_end_date, '%Y-%m-%d')
    time_formatted = '+'.join([bucket_start_date_printed,bucket_end_date_printed])
    comparisonItem = [{'keyword': kw,'time': time_formatted, 'geo': geo} for kw in keywords]
    
    

    req = {"comparisonItem": comparisonItem,"category": 7, "property": ""}
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

    return keywords


def HandleGTs(start_date, end_date, keywords):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    resp_text = get_data(start_date_dt, end_date_dt, keywords)
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




def DateProduce(beginyear):
    current_year =datetime.now().year
    if current_year < beginyear:
        raise 'Wrong year, the begin year is less than current year'

    else:
        pass
    da = []
    years = xrange(beginyear,current_year+1)
    for year in years:

        if year == current_year:
            stryear =str(current_year)
            if year % 2 == 1:
                date1 = (stryear+'-05-01', datetime.now().date().strftime('%Y-%m-%d'))
                da.append(date1)


            elif year % 2 == 0:
                if datetime.datetime.now().mouth < 9:
                    date1 = (stryear + '-01-01', ddatetime.now().date().strftime('%Y-%m-%d'))
                    da.append(date1)
                else: 
                    date1 = (stryear + '-01-01', stryear + '-08-31')
                    date2 = (stryear + '-09-01', datetime.now().date().strftime('%Y-%m-%d'))
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


def scraGoogleTrends_2yearPeriod(date, keywords, time2sleep=0.5):
    df =[HandleGTs(dt[0], dt[1], keywords) for  dt in date]
    
    time.sleep(time2sleep)
    
    #return pd.concat([df_temp0, df_temp1, df_temp2])
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


def downlaod(dates, keywords, link, locals_file_path):

    df_list = [scraGoogleTrends_2yearPeriod(date, keywords) for date in dates]

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
    sys.stdout.write("""\r%d%%|%s|completed %d *5 projects|Speed : %.4f s/5 projects|ETA: %s min""" %
                     (process * 100, hashes + spaces, counts, speed, ETA))

    
    sys.stdout.flush()

if __name__ == '__main__':
    gc.enable()
    requests_cache.install_cache(
        cache_name="googletrends_request_cache", backend="sqlite", expire_date=300)

    link = findoperation()
    

    locals_file_path = os.path.split(os.path.realpath(__file__))[0]
    target = locals_file_path + link + '1.txt'
    keywords = ImportListInfobyFile(locals_file_path, target)
    makedirs('data', locals_file_path, link)

    dates = chunks(DateProduce(2004), 3)

    #keywords = ['FDEF', 'FFBC' ,'THFF' ,'FFIN' ,'FFNW']
    key = chunks(keywords, 5)
    uncompleted_keywords = keywords
    
    # print key
    l_orign = len(key)
    l = l_orign
    count = 0
    request_time = 1

    for keywords in key:
        f = time.time()
        abnorl = True

        # downlaod(dates,keywords,link,locals_file_path)

        while abnorl:

            try:
                downlaod(dates, keywords, link, locals_file_path)
            except Exception as e:
                print e
                request_time = request_time + 1
                time.sleep(60)
                if request_time > 60:
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

    print 'download finished'
