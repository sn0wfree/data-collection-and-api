#-*- coding:utf-8 -*-

#-------------------
__version__ = "0.2"
__author__ = "sn0wfree"
'''
This tool is for importing the newsheat
'''
#-------------------
#-------------------
#-------------------
#-------------------

import pandas as pd
import sqlite3,gc


def create_table(conn, Symbol):
    try:
        create_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS %s
        (Date TEXT,
        NEWS_HEAT_PUB_DNUMSTORIES REAL,
        NEWS_HEAT_PUB_DMAX REAL,
        NEWS_HEAT_READ_DAVG REAL,
        NEWS_HEAT_READ_DMAX REAL,
        NEWS_HEAT_PUB_DAVG REAL);
        ''' % Symbol
       
        conn.execute(create_tb_cmd)
    except:
        print "Create table failed"


def insert_dt(conn, data, Symbol):

    conn.executemany('insert into %s values (?,?,?,?,?,?)' % Symbol, data)

def DetectTableOrTickerName_Str(tablename):
    if 'Equity' in tablename:
        tablename =tablename.split(' ')[0]
    
    elif tablename.find(' ') <5:
            tablename =tablename[0:tablename.find(' ')]
    else:
        pass
    return tablename

if __name__ == '__main__':
    gc.enable()
    data = pd.read_csv('bloomberg.csv')
    row_number = data.shape[0]
    column_number = data.shape[1]
    adj_num = row_number/6
    conn= sqlite3.connect("bloombergnewsheat.db")
    for row_num in xrange(adj_num):
        
        list_name =data.iloc[0+row_num*6][0]
        #NEWS_HEAT_PUB_DNUMSTORIES=data.iloc[1]
        #NEWS_HEAT_PUB_DMAX =data.iloc[2]
        #NEWS_HEAT_READ_DAVG=data.iloc[3]
        #NEWS_HEAT_READ_DMAX=data.iloc[4]
        #NEWS_HEAT_PUB_DAVG =data.iloc[5]
        #date =data.columns.tolist()[0:-1]

        dataT=data.iloc[0+row_num*6+1:0+row_num*6+5].T
        #data.iloc[1:5].T.iloc[0].tolist()
        dataT.columns=dataT.iloc[0].tolist()
        df =dataT.drop(dataT.index[:1])
        df.index.name='Date'
        df =df.reset_index()
        for datenumber in xrange(len(df['Date'])):
            temp =df['Date'][datenumber].split('/')
            date_replace = temp[2]+temp[1]+temp[0]
            df.set_value(datenumber,'Date',date_replace)


        df.to_sql(DetectTableOrTickerName_Str(list_name), conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

