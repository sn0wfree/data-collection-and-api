
# coding: utf-8

# In[4]:

import pandas as pd

import os,gc,platform
import sqlite3


# In[2]:

def InitalSqliteConnection(target):

    if target != 0:
        conn = sqlite3.connect(target)
    else:
        conn = sqlite3.connect(":memory:")

    return conn


def CollectedTableName(conn):
    #collect the name of table
    cur = conn.cursor()
    cur.execute(
        "select name from sqlite_master where type='table' order by name")
    return [table[0].encode("utf-8") for table in cur.fetchall()]


def DetectFileName(filepath):
    link = FindOperation()
    if '.' in filepath:
        if link in filepath:
            filename = filepath.split(link)[-1].split('.')[0]

        else:
            filename = filepath.split('.')[0]
    else:
        raise 'Unknown File Name'

    return filename


def FindOperation():
    #show platform and return the connect link word
    OperationSystem = platform.system()
    if OperationSystem is 'Darwin':
        link = '/'
    elif OperationSystem is 'Windows':
        link = '\\'
    else:
        link = '/'
    return link

def list2dict(keys,values):
    
    return dict(zip(keys,values))




def DetectUnciode(string):
    if isinstance(string, unicode):
        data= string.encode("utf-8")
    elif isinstance(string, str):
        data = string
    elif isinstance(string,basestring):
        data = string
        
    else:
        data = string
    
    return data

def DetectTypeAndTransform(unknown_type):
    if isinstance(unknown_type,list) or isinstance(unknown_type,tuple) or isinstance(unknown_type,set):
        for l in unknown_type:
            return DetectTypeAndTransform(l)
    elif isinstance(unknown_type,dict):
        raise 'Connot parse the Dict_type data'
   
    elif isinstance(unknown_type, unicode):
        return DetectUnciode(unknown_type)
    elif isinstance(unknown_type, str):
        return unknown_type
    else:
        raise 'Connot parse the unknown_type data'
def ChangeDate(Date):
    if "-" in Date:
        return Date.replace("-","")
    else:
        return Date
    
        
def FetchOutbySqlCmd(conn_cmd,variablelist):
        fetchout =conn_cmd.fetchall()
        
        date = [ChangeDate(DetectUnciode(d[0])) for d in fetchout ]
        data = [d[1:] for d in fetchout]
        return dict(zip(date,data)).update({'Date':variablelist}) 

def InitialSelectData(databasefilepath):
    FileName= DetectFileName(databasefilepath)
    conn = InitalSqliteConnection(databasefilepath)
    tables = CollectedTableName(conn)
    return tables,conn
    
def SelectDatafromSqliteImportPandas(conn,table,variablelist,TestModel=False):
    commandCODE = ','.join(variablelist)
    
    if TestModel == False:
        if table in ["ALL","ON"]:
            print '%s in ALL,ON'%table
            data ='Error'
        else:
            error=0
            for s in table:
                
                if s not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    
                    error=1
                    break
                else:
                    error=0
            if error == 0:
                #print "select %s from %s"%(commandCODE,table)
                commd ="select %s from %s"%(commandCODE,table)
                data = pd.read_sql_query(commd,conn)
            else:
                print '%s not in ABCDEFGHIJKLMNOPQRSTUVWXYZ'%table
                data ='Error'
    else:
        commd ="select %s from %s"%(commandCODE,table)
        data = pd.read_sql_query(commd,conn)
        
    return data
    
    
    

def SelectDatabyCMDOnlyfromSqlite(databasefilepath,variablelist):
    FileName= DetectFileName(databasefilepath)
    conn = InitalSqliteConnection(databasefilepath)
    tables = CollectedTableName(conn)
    commandCODE = ','.join(variablelist)
    conn_outputs=[]
    table_output=[]
    for table in tables:
        if table in ["ALL","ON"]:
            pass
        else:
            error=0
            for s in table:
                if s not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    error=1
                    break
                else:
                    error=0
            if error == 0:
                #print "select %s from %s"%(commandCODE,table)
                r =conn.execute("select %s from %s"%(commandCODE,table))
                conn_outputs.append(FetchOutbySqlCmd(r,variablelist))
                table_output.append(table)  
            else:
                pass
    #conn_outputs =[(table,conn.execute("select %s from %s"%(commandCODE,table)))for table in tables if table != "ALL"]
    
    return dict(zip(table_output,conn_outputs))

    
    
    
def ImportPandasfromSqliteFigureOutDate(conn,table,variablelist):
    df = SelectDatafromSqliteImportPandas(conn,table,variablelist)
    if isinstance(df,str):
        print df
        raise 'Error'
    
    #print str(df['Date'][0])
    
    if '-' in str(df['Date'][0]):
        #print df.get_value(1,'Date')
        for i in xrange(df.shape[0]):
            #print df.get_value(i,'Date')
            #print df.get_value(i,'Date').replace('-','')
            df.set_value(i,'Date',df.get_value(i,'Date').replace('-',''))
            pass
    else:
        pass
    return df

def chunks(target, n):
    if isinstance(target, list):
        date1 = [target[i:i + n] for i in xrange(0, len(target), n)]
    else:
        date1 = []
        raise ValueError, "Wrong type,I need a list."
    return date1  
 
def ReturnMerge(pd1,pd2):
     return pd.merge(pd1,pd2,how='left',on='Date')
def IntersectionForList(list1,list2):
    return list(set(list1) & set(list2))



def CalculateMA(DataFrame,ma_list ='Default'):
    
    # 分别计算5日、20日、30/60/100/200日的移动平均线
    if ma_list == 'Default':
        ma_list = [5, 20,30, 60,100,200]
    elif isinstance(ma_list,list) or isinstance(ma_list,tuple) or isinstance(ma_list,set):
        ma_list =ma_list
    else:
        ma_list = [5, 20,30, 60,100,200]
    for ma in ma_list:
        DataFrame['MA_' + str(ma)] = pd.rolling_mean(DataFrame['PRC'], ma)
    return DataFrame
        
def CalculateEMA(DataFrame,ma_list ='Default'):
    
    # 分别计算指数平滑移动平均线EMA
    if ma_list == 'Default':
        ma_list = [5, 20,30, 60,100,200]
    elif isinstance(ma_list,list) or isinstance(ma_list,tuple) or isinstance(ma_list,set):
        ma_list =ma_list
    else:
        ma_list = [5, 20,30, 60,100,200]
    for ma in ma_list:
        DataFrame['EMA_' + str(ma)] = pd.ewma(DataFrame['PRC'], span=ma)    
    return DataFrame


def ReadSqlByPandas(table,conn):
    
    return pd.read_sql_query("select * from %s"%table,conn)

if __name__ == '__main__':
    taeget = 'combine.db'
    tables,conn=InitialSelectData(taeget)
    
    df = ReadSqlByPandas(tables[2],conn).sort(['Date']).set_index(["Date"])
    print set(df.PRC)
    


    #variablelist_share=('Date','PRC','VOL','SICCD','NEWS_HEAT_PUB_DMAX','NEWS_HEAT_READ_DAVG','GoogleSearch')
    #print ReadSqlByPandas("AA",conn)






    
    # 分别计算5日、20日、60日的移动平均线
    ma_list = [5, 20,30, 60,100,200]

    # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
    #for ma in ma_list:
    #    sharesWRDS['MA_' + str(ma)] = pd.rolling_mean(sharesWRDS['PRC'], ma)
    #CalculateMA(sharesWRDS,[5, 20,30, 60,100,200])
    #CalculateEMA(sharesWRDS,[5, 20,30, 60,100,200])



    
   






