# -*- coding:utf-8 -*-
# use config() to create a Tkinter toggle button
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
from datetime import datetime
import time
'''
def toggle():


    if t_btn.config('text')[-1] == 'True':
        t_btn.config(text='False')

    else:
        t_btn.config(text='True')
root = tk.Tk()
t_btn = tk.Button(text="True", width=12, command=toggle)
t_btn.pack(pady=5)
root.mainloop()
'''


def DateProduce(begindate):
    begindate = str(begindate)
    if len(begindate) == 4:
        beginyear = begindate
        return yearonly(beginyear)
    elif len(begindate) >= 6:
        beginyear = begindate[0:4]
        beginmonth = begindate[4:6]
        return yearandmonth(beginyear, beginmonth)


def ChangeInt2StrDay(date):
    if int(date) < 10:
        day = '0' + str(int(date))
    else:
        day = str(int(date))
    return day


def getDays(year, month):
    year = int(year)
    month = int(month)
    day = 31  # 定义每月最多的天数
    while day:
        # print day
        try:
            time.strptime('%d-%d-%d' % (year, month, day),
                          '%Y-%m-%d')  # 尝试将这个月最大的天数的字符串进行转化
            break

        except:
            day -= 1  # 否则将天数减1继续尝试转化, 直到成功为止
    return day  # 成功时返回得就是这个月的天数


def yearandmonth(beginyear, beginmonth):
    da = []
    if int(beginyear) < datetime.now().year:
        years = range(int(beginyear), datetime.now().year + 1, 1)
        da = yearonly(int(beginyear) + 1)
        if int(beginmonth) <= datetime.now().month:
            if int(beginmonth) <= 6:

                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-06-30'))
                da.append((str(beginyear) + '-07-01',
                           str(beginyear) + '-12-31'))
            else:

                da.append((str(beginyear) + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-12-31'))

        else:
            raise ValueError('Wrong month, you choose the future month')

    elif int(beginyear) == datetime.now().year:

        if int(beginmonth) <= datetime.now().month:
            if int(beginmonth) <= 6 and datetime.now().month <= 6:

                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-0' + ChangeInt2StrDay(datetime.now().month) + '-' + ChangeInt2StrDay(datetime.now().day)))

            elif int(beginmonth) <= 6 and datetime.now().month > 6:
                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) +
                           '-01', str(beginyear) + '-06-30'))

                da.append((str(beginyear) + '-07-01',
                           str(beginyear) + '-0' + ChangeInt2StrDay(datetime.now().month) + '-' + ChangeInt2StrDay(datetime.now().day)))
            elif int(beginmonth) > 6:
                da.append((str(beginyear) + '-' + ChangeInt2StrDay(beginmonth) + '-01',
                           str(beginyear) + '-0' + ChangeInt2StrDay(datetime.now().month) + '-' + ChangeInt2StrDay(datetime.now().day)))

        else:
            raise ValueError('Wrong month, you choose the future month')

    else:
        raise ValueError('Wrong year, you choose the future year')
    return da


def yearonly(beginyear):
    da = []
    # years = [int(beginyear) + i for i in range(14)]

    if int(beginyear) < datetime.now().year:
        years = range(int(beginyear), datetime.now().year + 1, 1)
    elif int(beginyear) == datetime.now().year:
        years = [datetime.now().year]
    else:
        raise ValueError('Wrong year, you choose the future year')

    for year in years:
        if year == datetime.now().year:
            if datetime.now().month <= 6:
                da.append((str(year) + '-01-01', str(year) +
                           '-%d-%d' % (datetime.now().month, datetime.now().day)))
            else:
                da.append((str(year) + '-01-01', str(year) + '-06-30'))

                da.append((str(year) + '-07-01', str(year) +
                           '-%d-%d' % (datetime.now().month, datetime.now().day)))

        elif year < datetime.now().year:
            da.append((str(year) + '-01-01', str(year) + '-06-30'))
            da.append((str(year) + '-07-01', str(year) + '-12-31'))
        else:
            raise ValueError('Unexpected year, you choose the future year')

    return da

begindate = input('begindate')
print DateProduce(begindate)
