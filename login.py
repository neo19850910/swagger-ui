#-*- coding:utf8 -*-

import requests
from config.config import getConfig
from command.optionexcel import *

headers = getConfig('header', 'headers')
data = {'username': 'admin', 'password': '123456','rememberMe':False}
login_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户个人管理').get_value(4,1)

def get_session(data=data):
    login_session = requests.Session()
    login_session.post(login_api,headers=eval(headers), data=data)
    return login_session