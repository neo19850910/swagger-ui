# -*- coding:utf8 -*-
#__author__ = "neo"

from config.config import getConfig
import pymysql

host = getConfig('mysql','host')
port = getConfig('mysql','port')
user = getConfig('mysql','username')
passwd = getConfig('mysql','password')
db = getConfig('mysql','db')

def query(sql,data=None):
    conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=db, charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql, data)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result
