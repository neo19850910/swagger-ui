#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
f = file('E:\\data.txt', 'r')
print f.read().decode('gbk')