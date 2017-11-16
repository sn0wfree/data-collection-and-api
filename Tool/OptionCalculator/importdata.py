# -*- coding: utf-8 -*-

import datetime
import sqlite3
import time

import pandas as pd


def InitalSqliteConnection(target):

    if target != 0:
        conn = sqlite3.connect(target)
    else:
        conn = sqlite3.connect(":memory:")

    return conn


def changedatetimeform(endofperiod):
    if '/' in endofperiod:
        year = endofperiod.split('/')[-1]
        mon = endofperiod.split('/')[1]
        day = endofperiod.split('/')[0]
        return datetime.datetime.strptime(year + '-' + mon + '-' + day, '%Y-%m-%d')

    else:
        raise 'unexpected datatime'
if __name__ == '__main__':

    """
    上海5800**深圳030***是认购权证
    上海5809**深圳038***是认沽权证
    期权；权证；牛熊证
    option；warrant；callable bull and bear contract
    """
    csvfile = '0700认购权证20170918.csv'
    op = pd.read_csv(csvfile)[['代码', '名称', '正股代码', '正股简称', '到期日',
                               '权证最新价', '行权价', '兑换比率(倍)', '行权比率', '换股成本', '正股价格']]
    op.dropna(inplace=True)
    op.columns = ['WarrantCode', 'WarrantName', 'StockCode', 'StockName', 'ExpirationDate', 'CurrentWarrantPrice',
                  'ExercisePrice', 'WarrantExchangeRatio', 'WarrantExchangeRate', 'ExchangeCost', 'CurrentStockPrice']
    #----------------------

    op['Type'] = [1] * op.shape[0]  # call=1;put=-1

    ed = list(op['ExpirationDate'])
    op['ExpirationDate'] = [changedatetimeform(
        endofperiod) for endofperiod in ed]
    #-------------
    # print op['Expiration Date']
    #

    op['Time'] = [datetime.datetime.strptime(
        '2017-09-18', '%Y-%m-%d')] * op.shape[0]


def tosql(target=)
    conn = InitalSqliteConnection(target)
    conn.text_factory = str

    columns = ['WarrantCode', 'WarrantName', 'StockCode', 'StockName', 'ExpirationDate', 'CurrentWarrantPrice',
               'ExercisePrice', 'WarrantExchangeRatio', 'WarrantExchangeRate', 'ExchangeCost', 'Type', 'Time']

    op[columns].to_sql('Warrant', conn, if_exists='append')

    c = conn.cursor()
    c.execute('''SELECT DISTINCT %s FROM Warrant''' % (', '.join(columns)))
