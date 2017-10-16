# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
"""
This code is for personal use.

"""
# Copyright by Lin Lu 2017
# version control


__author__ = 'sn0wfree'
__version__ = '0.02'


import pandas as pd
# -------------------------------------------------------------------------
import requests
import requests_cache
import xlrd,datetime



def RepalceYMD2Eng(pdseries,status='Store'):
    symbollist = ['年'.decode('utf-8'),'月'.decode('utf-8'),'日'.decode('utf-8')]
    for symbol in symbollist:
        pdseries=pdseries.str.replace(symbol,'-')
            #pdseries =[d[:-2] if str(d)[-1] == '-' else d for d in pdseries.tolist()]
    c=[]
    for d in pdseries.tolist():
        try:
            if d[-1] == '-':
                
                c.append(d[:-1])
            elif d =='Now':
                if status == 'Parse':
                    c.append(str(datetime.date.today()))
                else:
                    c.append(d)
            else:
                c.append(d)
        except  Exception:
            c.append(d)

    return c
    

    
    
   
    return pdseries
if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="Leader", backend="sqlite", expire_date=300)

    ministry_file = pd.ExcelFile("ministry.xlsx")
    ministry_list = []
    for sheetname in ministry_file.sheet_names:
        tempdf = ministry_file.parse(sheetname)[
            ['Name', 'Start', 'End', 'Jobtitle']]
        tempdf['Ministry Section'] = [sheetname] * tempdf.shape[0]
        ministry_list.append(tempdf)
    ministry = pd.concat(ministry_list)
    ministry = ministry.reindex()
    ministry['End'] =RepalceYMD2Eng(ministry['End'])
    ministry['Start'] =RepalceYMD2Eng(ministry['Start'])
    print ministry


    #print RepalceYMD2Eng(ministry['End'],status='Parse')



