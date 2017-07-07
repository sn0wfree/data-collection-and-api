import os
os.chdir("path")

import re
import csv
import time
import pandas as pd
from random import randint
from GT_Automation_Code import pyGTrends

# set gmail credentials and path to extract data
google_username = "snowpythontest@gmail.com"
google_password = "19920815"

Daily_Data = []

# define daily pull code


def GT_Daily_Run(keys):

    path = 'path'

    # connect to Google
    connector = pyGTrends(google_username, google_password)
    # make request
    connector.request_report(keys, date="today 90-d", geo="")
    # wait a random amount of time between requests to avoid bot detection
    time.sleep(randint(5, 10))
    # download file
    connector.save_csv(path, '_' + "GT_Daily" + '_' + keys.replace(' ', '_'))

    name = path + '_' + "GT_Daily" + '_' + keys.replace(' ', '_')

    with open(name + '.csv', 'rt') as csvfile:
        csvReader = csv.reader(csvfile)
        data = []

        for row in csvReader:
            if any('2015' in s for s in row):
                data.append(row)

        day_df = pd.DataFrame(data)
        cols = ["Day", keys]
        day_df.columns = [cols]
        Daily_Data.append(day_df)

keywords = ['soccer', 'football', 'baseball']

map(lambda x: GT_Daily_Run(x), keywords)

rge = [Daily_Data[0], Daily_Data[1], Daily_Data[2]]

df_final_daily = reduce(
    lambda left, right: pd.merge(left, right, on='Day'), rge)
df_final_daily = df_final_daily.loc[:, (df_final_daily != "0").any(axis=0)]
df_final_daily.to_csv("Daily_Trends_Data.csv", index=False)

Weekly_Data = []

# define weekly pull code


def GT_Weekly_Run(keys):

    path = 'path'

    # connect to Google
    connector = pyGTrends(google_username, google_password)
    # make request
    connector.request_report(keys, geo="US")
    # wait a random amount of time between requests to avoid bot detection
    time.sleep(randint(5, 10))
    # download file
    connector.save_csv(path, '_' + "GT_Weekly" + '_' + keys.replace(' ', '_'))

    name = path + '_' + "GT_Weekly" + '_' + keys.replace(' ', '_')

    with open(name + '.csv', 'rt') as csvfile:
        csvReader = csv.reader(csvfile)
        data = []
        datex = re.compile(
            '(19|20)dd-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])')

        for row in csvReader:
            if datex.search(str(row)):
                data.append(row)

        week_df = pd.DataFrame(data)
        cols = ["Week", keys]
        week_df.columns = [cols]
        Weekly_Data.append(week_df)

map(lambda x: GT_Weekly_Run(x), keywords)

rge = [Weekly_Data[0], Weekly_Data[1], Weekly_Data[2]]

df_final_weekly = reduce(
    lambda left, right: pd.merge(left, right, on='Week'), rge)
df_final_weekly = df_final_weekly.loc[:, (df_final_weekly != "0").any(axis=0)]
df_final_weekly.to_csv("Weekly_Trends_Data.csv", index=False)
