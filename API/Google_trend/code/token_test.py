# -*- coding:utf-8 -*-
import requests
import urllib
import json


def get_token(key):
    headers = {}
    headers['Host'] = 'trends.google.com'
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Referfer'] = 'https://trends.google.com/trends/explore?date=2017-04-01%202017-07-05&q=' + \
        urllib.quote(key)
    headers['x-client-data'] = 'CIu2yQEIpLbJAQjBtskBCPqcygEIqZ3KAQ=='
    req = {}
    req['category'] = 0
    req['property'] = ''
    req['comparisonItem'] = [{"geo": "", "keyword":  urllib.quote(
        key).replace(' ', '+'), "time": "2017-04-01%202017-07-05"}]
    value = {}
    value['hl'] = 'zh-CN'
    value['tz'] = '-480'
    value['req'] = str(req).replace(' ', '')
    url = 'https://trends.google.com/trends/api/explore?'
    for index in value:
        url = url + index + '=' + value[index] + '&'
    # 后面两个参数很重要
    results = requests.get(url, headers=headers,
                           verify=False, allow_redirects=False)
    page = results.content
    jsonData = page[5:]
    print jsonData
    data = json.loads(jsonData, encoding="utf-8")
    # print data
    token = data['widgets'][0]['token']
    # print token
    return token


def get_google_trend(key):
    headers = {}
    headers['Host'] = 'trends.google.com'
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Referfer'] = 'https://trends.google.com/trends/explore?date=today%201-m&q=' + \
        urllib.quote(key)
    req = {}
    req['time'] = '2017-04-01' + "+" + '2017-07-05'
    req['resolution'] = "DAY"
    req['locale'] = "zh-CN"
    req['comparisonItem'] = [{"geo": {}, "complexKeywordsRestriction": {
        "keyword": [{"type": "BROAD", "value": urllib.quote(key).replace(' ', '+')}]}}]
    req['requestOptions'] = {"property": "", "backend": "IZG", "category": 0}
    value = {}
    value['hl'] = 'zh-CN'
    value['tz'] = '-480'
    value['req'] = str(req).replace(' ', '')
    value['token'] = get_token(key)
    url = 'https://trends.google.com/trends/api/widgetdata/multiline'
    for index in value:
        url = url + index + '=' + value[index] + '&'
    results = requests.get(url, headers=headers, verify=False)
    page = results.content
    jsonData = page[5:]
    data = json.loads(jsonData, encoding="utf-8")
    items = data['default']['timelineData']
    result = []
    for item in items:
        timestamp = int(item['time'])
        time_temp = time.localtime(timestamp)
        date = time.strftime("%Y-%m-%d", time_temp)
        value = item['value'][0]
        temp = {'key': key, 'date': date, 'google_index': value}
        result.append(temp)
    return result


if __name__ == '__main__':
    #result = get_token('ONB')
    get_google_trend('ONB')
