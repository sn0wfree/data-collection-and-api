# -*- coding:utf-8 -*-
#
#
#
#from flask import Flask, request, make_response
import hashlib
import json
import sys
import time
import xml.etree.ElementTree as ET

import requests

reload(sys)  # 不加这部分处理中文还是会出问题
sys.setdefaultencoding('utf-8')
#from dispatcher import *


if __name__ == '__main__':
    APPID = 'wxbc93a242f41c0314'  # app ID
    APPSECRET = '9c5100a4110e741897474140b873f867'  # secret

    requesturl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        APPID, APPSECRET)
    rs = requests.session()
    print rs.get(requesturl)
