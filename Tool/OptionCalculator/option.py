# -*- coding: utf-8 -*-


import datetime
import multiprocessing as mp
import sqlite3
import time
from enum import Enum

import numpy
import pandas as pd


def InitalSqliteConnection(target):

    if target != 0:
        conn = sqlite3.connect(target)
    else:
        conn = sqlite3.connect(":memory:")

    return conn


def locate(l, obj, location=[], init=-1):
    try:
        init = l.index(obj, init + 1,)

        location.append(init)

        return locate(l, obj, location, init)
    except Exception, e:

        return location


def locateandreplace(l, obj, replacestr):
    lo = locate(l, obj)
    for i in lo:
        l[i] = replacestr
    return l


class Stock():

    def __init__(self, stockprice, stockcode, stockname, ma='default'):

        self.stockcode = stockcode
        self.stockname = stockname
        self.stockprice = stockprice
        self.MACalculator()

    def MACalculator(self, ma='default'):
        if ma == 'default':
            ma = 20
        elif isinstance(ma, int):
            ma = ma
        else:
            raise 'Unknown Moving Average Period'

        self.ma = self.stockprice.rolling(window=ma, center=False).mean()
        self.ma_description = 'MA_%d' % ma


class OptionBasedContractType(Enum):
    put = -1
    call = 1


class Option():

    def __init__(self):
        Normal = {'HK': 'inf', 'SZ': 0.1, 'SH': 0.1}
        ST = {'SZ': 0.05, 'SH': 0.05, 'HK': 'inf'}
        self.market = (Normal, ST)

    def CalculateProfitinclass(self, op, increase=0, profitrate=False):

        op['CurrentOptionCost'] = op[
            'CurrentOptionPrice'] * (1 / op['ExchangeRatio'])
        Exercisable = op['CurrentStockPrice'] * (increase + 1) * op['OptionType'] > op[
            'ExercisePrice'] * op['OptionType']
        Profit = (op['CurrentStockPrice'] * (increase + 1) - op['ExercisePrice']
                  ) * op['Type'] * Exercisable - op['CurrentOptionCost']
        if profitrate:
            return Profit / op['CurrentOptionPrice']

        else:
            return Profit

    def Single_input(self, option, stockprice, increase=0, profitrate=False):
        optionname, optiontype, optioncode, stockname, stockcode, exerciseprice, optionfee, period = option
        Exercisable = stockprice * optiontype > exerciseprice * optiontype

        Profit = (stockprice * (increase + 1) - exerciseprice) * \
            optiontype * Exercisable - optionfee
        if profitrate:
            return Profit / optionfee
        else:
            return Profit

        #-------------------

    def Df_input(self, op, increase=0, profitrate=False):
        """
        input: dataframe(op);
                   expected stock change rate (increase);
                   calcualte return rate:profitrate bool value
        output: dataframe:include:1.Current Stock Price
                                                          2.Option Type
                                                          3.Exercise Price
                                                          4.Current Option Cost


        """
        if isinstance(increase, float) or isinstance(increase, int):
            if profitrate is False:
                op['Profit as stock increased %d%%' % increase *
                    100.0] = self.CalculateProfitinclass(op, increase=increase, profitrate=profitrate)
            elif profitrate is True:
                op['ReturnRate as stock increased %d%%' % increase *
                    100.0] = self.CalculateProfitinclass(op, increase=increase, profitrate=profitrate)
            elif profitrate == 'both':
                op['Profit as stock increased %d%%' % increase *
                    100.0] = self.CalculateProfitinclass(op, increase=increase, profitrate=False)
                op['ReturnRate as stock increased %d%%' % increase *
                    100.0] = self.CalculateProfitinclass(op, increase=increase, profitrate=True)
            else:
                raise 'Unknown parameter:profitrate==%s' % profitrate

            return op
        else:
            raise 'Unknonw Increase Number'

    def WhichMarketandLimit(self, code):

        return self.market[0][code.split('.')[-1].upper()]

    def Stringanddatetimetransform(self, date, transform='String2Datetime', TypeForm="%Y-%m-%d"):
        '''
        option: String To Datetime
                        Datetime To String
                        String To Timestamp
                        String To Timestamp
                        Timestamp To String
                        Datetime To Timestamp


        '''
        if transform == 'String2Datetime':
            return datetime.datetime.strptime(date, TypeForm)
        elif transform == 'Datetime2string':
            return datetime.date.strftime(TypeForm)
        elif transform == 'String2Timestamp':
            return datetime.time.mktime(datetime.datetime.strptime(date, TypeForm).timetuple())
        elif transform == 'Timestamp2String':
            return datetime.time.strftime(TypeForm, datetime.time.localtime(date))
        elif transform == 'Datetime2Timestamp':
            return datetime.time.mktime(datetime.date.timetuple())
        elif transform == 'Timestamp2Datetime':
            return datetime.datetime.strptime(datetime.time.strftime(TypeForm, datetime.time.localtime(date)), TypeForm)

        else:
            raise 'Unknow transform order:%s' % transform

    def Calincrease(self, op, profitrate=False, mode='Df_input'):
        # span=[ self.increasespan('0700.HK',date) for date in list(op['Expiration Date'])]
        # adjustedspan=[10 if sp=='inf' or sp>10 else sp for sp in span ]
        for increase in numpy.arange(-10, 10, 0.05):
            op = eval('self.%s(op,increase=increase,profitrate=False)' % mode)
        return op

    def detectdate(self, endofperiod, transform='String2Datetime'):
        if '-' in endofperiod:
            endofperiod = self.Stringanddatetimetransform(
                endofperiod, transform=transform)
        elif '/' in endofperiod:
            year = endofperiod.split('/')[-1]
            mon = endofperiod.split('/')[1]
            day = endofperiod.split('/')[0]

            endofperiod = self.Stringanddatetimetransform(
                (year + mon + day), transform=transform, TypeForm="%Y%m%d")
        elif isinstance(endofperiod, (int, float)):
            if len(str(endofperiod)) != 8:
                endofperiod = self.Stringanddatetimetransform(
                    endofperiod, transform=transform)
            else:
                endofperiod = self.Stringanddatetimetransform(
                    str(endofperiod), transform=transform, TypeForm="%Y%m%d")
        elif isinstance(endofperiod, datetime.datetime):
            pass

        else:
            raise 'Unknown Form of endofperiod'
        return endofperiod

    def increasespan(self, code, endofperiod):
        endofperiod = self.detectdate(endofperiod)

        timedelta = (endofperiod - datetime.datetime.now()).days
        if timedelta <= 0:
            raise 'Invalid Period:%s' % self.Stringanddatetimetransform(
                endofperiod, transform='Datetime2string')
        elif timedelta < 7:
            workingday = sum([(now + datetime.timedelta(days=day)).weekday()
                              not in [5, 6] for day in xrange(timedelta)])
        else:
            if timedelta % 7 >= 5:
                workingday = (timedelta // 7) * 5 + 5
            else:
                workingday = (timedelta // 7) * 5 + temp7

        increasespan = self.WhichMarketandLimit(code)
        if increasespan == 'inf':
            return 10
        else:
            return (1 + increasespan)**workingday


def CalculateProfit(op, increase, profitrate=False):
    op['CurrentWarrantCost'] = op[
        'CurrentWarrantPrice'] * (1 / op['ExchangeRatio'])
    Exercisable = op['CurrentStockPrice'] * (increase + 1) * op['WarrantType'] > op[
        'ExercisePrice'] * op['Warrant Type']
    Profit = (op['CurrentStockPrice'] * (increase + 1) - op['ExercisePrice']
              ) * op['WarrantType'] * Exercisable - op['CurrentWarrantCost']
    if profitrate:
        return Profit
    else:
        return Profit / op['WarrantPrice']


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

    test = Option()
    ed = list(op['ExpirationDate'])
    op['ExpirationDate'] = [test.detectdate(
        endofperiod) for endofperiod in ed]
    #-------------
    # print op['Expiration Date']
    op['Time'] = [datetime.datetime.strptime(
        '2017-09-18', '%Y-%m-%d')] * op.shape[0]
    conn = InitalSqliteConnection('option.db')
    conn.text_factory = str
    print op.columns
    print op.Time
    columns = ['WarrantCode', 'WarrantName', 'StockCode', 'StockName', 'ExpirationDate', 'CurrentWarrantPrice',
               'ExercisePrice', 'WarrantExchangeRatio', 'WarrantExchangeRate', 'ExchangeCost', 'Type', 'Time']

    op[columns].to_sql('Warrant', conn, if_exists='append')

    c = conn.cursor()
    c.execute('''SELECT DISTINCT %s FROM Warrant''' % (', '.join(columns)))

    # print op['ReturnRate as stock increased %s'%str(increase)]

    # if 正股价格 *期权类型（put or call）> 行权价 *期权类型（put or call）:行权
    # else 不行权
    # def exercise(exercise):

    # return 正股价格*期权类型（put or call）*exercise-行权价*期权类型（put or
    # call)*exercise-权证最新价*(1/兑换比率(倍))
