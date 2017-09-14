
# coding: utf-8

# In[1]:

import sqlite3
import pandas as pd


# In[25]:

fama3factors_file = 'FAMA3factor.csv'
tbill_file = 'TBillRate.csv'


# In[63]:

FF3 = pd.read_csv(fama3factors_file)

tbill = pd.read_csv(tbill_file)


# In[44]:

tbill.Year
tbill.Day
tbill.Month


# In[46]:

def date2str(date):
    if isinstance(date,int):
        if date<=9:
            return '0'+str(date)
        else:
            return str(date)
    elif isinstance(date,str):
        return date

tbill['Date'] = [date2str(a)+date2str(b[0])+date2str(b[1]) for a,b in zip(tbill.Year,zip(tbill.Month,tbill.Day) )]
    
        


# In[49]:

tbill


# In[69]:

ttt =tbill[['Date','TBill1Mo','TBill3Mo']]


# In[56]:

def SetIndexType(pd):
    pd[['Date']]=pd[['Date']].astype(int)
    return pd

def ReturnMerge(pd1,pd2):
    pd1 =SetIndexType(pd1)
    pd2 =SetIndexType(pd2)
    return pd.merge(pd1,pd2,how='left',on='Date')


# In[73]:

returns  =ReturnMerge(ttt,FF3).dropna()
#ttt.dtype


# In[75]:

returns[['Date','TBill1Mo','TBill3Mo','Mkt-RF','SMB','HML','RF']].to_csv('otherfactor.csv')


# In[ ]:



