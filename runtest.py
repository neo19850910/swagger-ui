#coding=utf-8

import HTMLTestRunner
from sendmai import *
import os,time
import unittest
import sys
reload(sys)
sys.setdefaultencoding('utf8')

listaa = os.getcwd() + '\\testcase\\'
def creatsuitel():
    testunit=unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(listaa,
                                                   pattern='test_*.py',
                                                   top_level_dir=None)
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)
    return testunit
alltestnames = creatsuitel()
now = time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
filename = os.getcwd() + '\\report\\' + now + 'result.html'
fp = file(filename, 'wb')
runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'swagger-ui接口测试测试报告',
        description=u'用例执行情况：')
#执行测试用例
runner.run(alltestnames)
fp.close()
sentmail(reportsort())

