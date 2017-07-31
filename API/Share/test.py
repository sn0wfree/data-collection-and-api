#-*- coding:utf-8 -*-

#-------------------
__version__ = "0.2"
__author__ = "sn0wfree"
'''
This tool is for download the shares
'''
#-------------------
#-------------------
#-------------------
#-------------------

import yqd
import gc
import os
import platform
import time,random,sys

import requests
import requests_cache
import sqlite3


def findoperation():
    OperationSystem = platform.system()
    if OperationSystem is 'Darwin':
        link = '/'
    elif OperationSystem is 'Windows':
        link = '\\'
    else:
        link = '/'
    return link


def load_quote(ticker, startdate, enddate):
    # startdate = '20040115'
    # enddate = '20170617'

    a = yqd.load_yahoo_quote(ticker, startdate, enddate)
    return a


def test():
    # Download quote for stocks
    load_quote('QCOM')
    load_quote('C')

    # Download quote for index
    load_quote('^DJI')


def create_table(conn, Symbol):
    try:
        create_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS %s
        (Date TEXT,
        Open REAL,
        High REAL,
        Low REAL,
        Close REAL,
        Adj_Close REAL,
        Volume REAL);
        ''' % Symbol
        # 主要就是上面的语句
        conn.execute(create_tb_cmd)
    except:
        print "Create table failed"


def insert_dt(conn, data, Symbol):

    conn.executemany('insert into %s values (?,?,?,?,?,?,?)' % Symbol, data)


def list2str(data):
    ty = ''
    for order in xrange(len(data)):
        # print order, len(data)
        if order < len(data) - 1:
            if isinstance(data[order], str):
                ty = ty + data[order] + ','
            else:
                ty = ty + str(data[order]) + ','
        else:
            if isinstance(data[order], str):
                ty = ty + data[order]
            else:
                ty = ty + str(data[order])

    # print ty
    return ty


def download_sharedata(Symbol, startdate, enddate):
    request_time = 0
    while 1:

        try:
            stocks = load_quote(Symbol, startdate, enddate)

        except Exception as e:
            print e
           

            request_time = request_time + 1
            time.sleep(5 + request_time * 5)
            if request_time > 60:
                raise 'Quota limit'

        else:

            break
    return stocks


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


def importkeywords(target=False):
    link = findoperation()

    locals_file_path = os.path.split(os.path.realpath(__file__))[0]
    if target == False:

        target = locals_file_path + link + '1.txt'
    else:
        pass
    keywords = ImportListInfobyFile(locals_file_path, target)
    return keywords


def collectedtablename(conn):
    cur = conn.cursor()
    cur.execute(
        "select name from sqlite_master where type='table' order by name")
    tablename = [table[0].encode("utf-8") for table in cur.fetchall()]
    return tablename

def dowloadandinsert(conn,Symbol,startdate, enddate):
    request_time = 0
    while 1:

        try:
            stocks = load_quote(Symbol, startdate, enddate)
            output = [tuple(stock.encode("utf-8").split(',')) for stock in stocks]
            if output[0][0] == 'Date':
                del output[0]
            if output[-1][0] == "":
                del output[-1]
            else:
                pass
            # print output

            # create table

            create_table(conn, Symbol)
            # insert data

            insert_dt(conn, output, Symbol)
            conn.commit()

        except Exception as e:
            #print e,e.errno,dir(e)
            if e.code == 404 :

                print 'wrong ticker'
                write_txt_change(Symbol, 'error.txt')
                break

            elif e.code ==401:
                print e
                time.sleep(60)
           
                
            request_time = request_time + 1
            time.sleep(5 + request_time * 5)
            if request_time > 60:
                raise 'Quota limit'

        else:

            break
    
    
    time.sleep(random.randint(5, 20))

def write_txt_change(ticker, targetpath):
    Errorkeywords=[]
    fi=[]

    if isinstance(ticker,str):
        fi .append(ticker)
    elif isinstance(ticker,list):
        fi =ticker
    else:
        pass

    with open(targetpath, 'r') as f:
        ticker =f.readlines()
        for line in ticker:
                Errorkeywords.append(line.strip())
    errorticker =list(set(Errorkeywords) | set(fi))

    with open(targetpath, 'w') as f:
        for ff in errorticker:
            f.write(ff + '\n')
def write_txt(fi, targetpath):
    with open(targetpath, 'w') as f:
        for ff in fi:
            f.write(ff + '\n')
def write_txt_a(fi, targetpath):
    with open(targetpath, 'a') as f:
        for ff in fi:
            f.write(ff + '\n')
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
    requests_cache.install_cache(
        cache_name="shareprice_request_cache", backend="sqlite", expire_date=300)
    gc.enable()

    startdate = '20040115'
    enddate = '20170630'
    Symbol = 'SRCE'

    # import keywords
    keywords = importkeywords()

    # create database
    momeory = 0
    if momeory == 1:
        conn = sqlite3.connect(":memory:")
    else:
        conn = sqlite3.connect("1.db")

    ticker_colelcted = collectedtablename(conn)
    wrongticker = importkeywords('error.txt')


    Symbols = list(set(keywords) ^ set(ticker_colelcted) ^ set(wrongticker))
    counts=0
    lenn =len(Symbols)
    for Symbol in Symbols:
        f=time.time()


        dowloadandinsert(conn,Symbol,startdate, enddate)
        counts =counts +1
        speed =time.time()-f
        progress_test(counts, lenn, speed)

        if counts%10 == 0:
            time.sleep(60)
        else:
            pass



    conn.close()
