# -*- coding:utf-8 -*-

# 2017-01-01%202017-06-30
# 2016-07-01%202016-12-31

# https://trends.google.com/trends/explore?date=2016-07-01%202016-12-31&q=OFL,XOH,IOM,EOM,ERO
#
#

import os
import time


def month2day(month, year):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month == 2:
        return runyear2day(year)
    else:
        return 30


def runyear2day(year):
    if (year % 4 == 0) and (year % 100 != 0):
        return 29
    elif (year % 100 == 0) and (year % 400 == 0):
        return 29
    else:
        return 28


def strmonth(month):
    if month < 10:
        return '0' + str(month)
    else:
        return str(month)


def mon(beginyear):

    link = '%20'

    da = []

    years = [beginyear + i for i in range(14)]
    for year in years:

        if year == 2017:

            command1 = '2017-05-01' + link + '2017-06-30'
            da.append(command1)

        elif year != 2017:
            stryear = str(year)
            if year % 2 == 1:
                command1 = stryear + '-05-01' + link + stryear + '-12-31'

                da.append(command1)

            elif year % 2 == 0:
                command1 = stryear + '-01-01' + link + stryear + '-08-31'

                command2 = stryear + '-09-01' + link + str(year + 1) + '-04-30'
                da.append(command1)
                da.append(command2)
    return da


def mon_backup(beginyear):
    begin1 = '-01-01%20'
    end1 = '-06-30'
    begin2 = '-07-01%20'
    end2 = '-12-31'
    da = []

    years = [beginyear + i for i in range(14)]
    for year in years:
        if year != 2017:
            year = str(year)
            command1 = year + begin1 + year + end1
            command2 = year + begin2 + year + end2
            da.append(command1)
            da.append(command2)
        else:
            year = str(year)
            command1 = year + begin1 + year + end1
            da.append(command1)
    return da


def command(datef, target):

    common1 = 'https://trends.google.com/trends/explore?date='
    common2 = '&q='
    url = common1 + datef + common2 + target
    return url


def chunks(arr, n):
    return [arr[i:i + n] for i in range(0, len(arr), n)]


def target_function(tic, n):
    te = chunks(tic, n)

    newlist = []
    for t in te:

        temp = ''

        for s in xrange(len(t)):
            if s + 1 < len(t):

                temp = temp + t[s] + ','
            else:
                temp = temp + t[s]
        newlist.append(temp)
    return newlist


def read_ticker(tickerfile):
    tic = []
    with open(tickerfile, 'r') as ticker:
        ticker = ticker.readlines()
        for line in ticker:
            tic.append(line.strip())
    return tic


def write_txt(fi, targetpath):
    with open(targetpath, 'w') as f:
        for ff in fi:
            f.write(ff + '\n')



    


def makedirs(names, path):
    for name in names:
        directory = path + '/' + name
        if not os.path.exists(directory):
        os.makedirs(directory)
        # time.sleep(30)


if __name__ == '__main__':
    # print mon(2004)
    tickerfile = '/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/ticker.txt'
    ticker = read_ticker(tickerfile)
    targets = target_function(ticker, 5)
    date = mon(2004)
    targetpath = '/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/tickergroup.txt'
    #write_txt(targets, targetpath)

    commands = []

    for target in targets:
        for d in date:
            commands.append(command(d, target))
    # print commands
    commandpath = '/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/commands2.txt'

    write_txt(commands, commandpath)
    pa = '/Users/sn0wfree/Desktop/russell3000/data'
    # makedirs(targets,pa)
