# -*- coding:utf-8 -*-
import os
import platform
import webbrowser
import time

import shutil
import copy
import pandas as pd
import re
import csv
import numpy as np
from pandas import DataFrame
import sys
import json
import urllib
from datetime import datetime, timedelta
import requests


def get_buckets(start_date, end_date):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    bucket_limits = [start_date_dt]
    left_limit = start_date_dt
    while left_limit <= end_date_dt:
        new_limit = left_limit + timedelta(days=365)
        if new_limit < end_date_dt:
            bucket_limits.append(new_limit)
        left_limit = new_limit
    bucket_limits.append(end_date_dt)
    return bucket_limits


def get_data(bucket_start_date, bucket_end_date, keywords):
    bucket_start_date_printed = datetime.strftime(
        bucket_start_date, '%Y-%m-%d')
    bucket_end_date_printed = datetime.strftime(bucket_end_date, '%Y-%m-%d')
    time_formatted = bucket_start_date_printed + '+' + bucket_end_date_printed
    comparisonItem = []
    geo = ''
    for kw in keywords:
        keyword_payload = {'keyword': kw,
                           'time': time_formatted, 'geo': geo}
        comparisonItem.append(keyword_payload)

    req = {"comparisonItem": comparisonItem,
           "category": 7, "property": ""}
    hl = "en-GB"
    tz = "-120"

    explore_URL = 'https://trends.google.com/trends/api/explore?hl={0}&tz={1}&req={2}'.format(
        hl, tz, json.dumps(req).replace(' ', '').replace('+', ' '))
    return requests.get(explore_URL).text


def get_token(response_text):
    try:
        return response_text.split('token":"')[1].split('","')[0]
    except:
        return None


def get_csv_request(response_text):
    try:
        return response_text.split('"widgets":')[1].split(',"lineAnno')[0].split('"request":')[1]
    except:
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

    df = pd.DataFrame(columns=col)
    for columnnumber in xrange(len(col)):
        locals()[col[columnnumber]] = []
    # Delete top 3 lines
    for data in datas:
        for columnnumber in xrange(len(col)):
            locals()[col[columnnumber]].append(
                data.split(',')[columnnumber])
    for columnnumber in xrange(len(col)):
        df[col[columnnumber]] = locals()[col[columnnumber]]
    return df


def parse_csv_backup(csv_contents):
    lines = csv_contents.split('\n')
    df = pd.DataFrame(columns=['date', 'value'])
    dates = []
    values = []
    # Delete top 3 lines
    for line in lines[3:-1]:
        try:
            dates.append(line.split(',')[0].replace(' ', ''))
            values.append(line.split(',')[1].replace(' ', ''))
        except:
            pass
    df['date'] = dates
    df['value'] = values
    return df


def get_daily_frames(start_date, end_date, keyword):

    bucket_list = get_buckets(start_date, end_date)
    frames = []
    for i in range(0, len(bucket_list) - 1):
        resp_text = get_data(bucket_list[i], bucket_list[i + 1], keyword)
        frames.append(parse_csv(get_csv(resp_text)))

    return frames


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
    da = []
    years = [beginyear + i for i in range(14)]
    for year in years:

        if year == 2017:
            date1 = ('2017-05-01', '2017-06-30')
            da.append(date1)

        elif year != 2017:
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

def scraGoogleTrends_2yearPeriod(date,keywords,time2sleep=0.9):
        df_temp0 = HandleGTs(date[0][0], date[0][1], keywords)
        df_temp1 = HandleGTs(date[1][0], date[1][1], keywords)
        df_temp2 = HandleGTs(date[2][0], date[2][1], keywords)
        time.sleep(time2sleep)
        return pd.concat([df_temp0, df_temp1, df_temp2])

def makedirs(names, path,link):
    if isinstance(names,list):
        for name in names:
            directory = path + link+ name
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                pass
            
    elif isinstance(names,str):
        directory = path + link+ name
        if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                pass

    
def downlaod(dates,keywords,link,locals_file_path):
    
        df_list =[scraGoogleTrends_2yearPeriod(date,keywords) for date in dates]

        target_pd=pd.concat(df_list).T

        filename=''
        for keyword in keywords:
            #print keyword
            filename=filename+keyword
        savepath=locals_file_path+link+'data'+link+filename+'.csv'
        #print savepath
        target_pd.to_csv(savepath,header=False)


def progress_test(counts,lenfile,speed):
    bar_length=20
    eta=time.time()+speed*counts
    process =counts/float(lenfile)

    ETA=datetime.datetime.fromtimestamp(eta)
    hashes = '#' * int(precent * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|completed %d *5 projects|Speed : %.4f s/5 projects|ETA: %s """ % (process*100,hashes + spaces,counts,speed,ETA))

    #sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects" % (counts,f2-f1))

    #sys.stdout.write("\rPercent: [%s] %d%%,remaining time: %.4f mins"%(hashes + spaces,precent,w))
    sys.stdout.flush()

if __name__ == '__main__':
    
    link = findoperation()

    locals_file_path = os.path.split(os.path.realpath(__file__))[0]
    target = locals_file_path+link+'1.txt'
    makedirs('data', locals_file_path,link)

    #target = '/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/1.txt'
    keywords = ImportListInfobyFile(locals_file_path, target)
    # print len(keywords)
    # print locals_file_path + '{0}.csv'.format('good')
    # show operation system
    
    #da_temp = '/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/'
    dates = chunks(DateProduce(2004), 3)

    
    #keywords = ['AON', 'APA', 'AIV', 'APIC', 'APOG']
    key=chunks(keywords, 5)
    l_orign =len(key)
    l=l_orign
    count =0
    
    for keywords in key:
        f = time.time()
        downlaod(dates,keywords,link,locals_file_path)
        time.sleep(1)
        count=count+1
        workingtime=time.time()-f
        if  workingtime<=60:
            time.sleep(5)
        else:
            time.sleep(random.randrange(1, 2,0.1))
        if count>50:
            count=0
            time.sleep(10)
        else:
            pass
        closingtime = time.time()-f
        l=l-1
        speed=closingtime
        
        progress_test(l_orign-l,l_orign,speed)
        
    print 'download finished'



    
    

    
   