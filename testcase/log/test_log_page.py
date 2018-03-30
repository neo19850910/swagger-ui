#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
from command.con_mysql import query

class LogPage(unittest.TestCase):
    '''分页检索系统日志列表'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_log_page40(self):
        '''分页检索系统日志列表:不输入参数查询日志'''
        response = self.session.get(log_page_api)
        data =response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        sql_count = '''
                    select count(*) from log where is_delete!=1;
                '''
        count = query(sql_count)[0]
        self.assertEqual(count, result['totalCount'] + 1)
        self.assertTrue(success)
        self.assertEqual(msg, u'操作成功')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['pageNum'], 1)
        self.assertEqual(result['pageSize'], 10)
        self.assertEqual(len(result['data']), 10)

    def test_log_page41(self):
        '''分页检索系统日志列表:无权限查询日志'''
        log_session = get_session(data_no_permission)
        response = log_session.get(log_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_log_page42(self):
        '''分页检索系统日志列表:未登录查询日志'''
        response = requests.get(log_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_log_page43(self):
        '''分页检索系统日志列表:正常输入参数查询日志'''
        params_data = {'pageNum':1,
                'pageSize':2
                }
        response = self.session.get(log_page_api, params=params_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertTrue(success)
        self.assertEqual(msg, u'操作成功')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['pageNum'], 1)
        self.assertEqual(result['pageSize'], 2)
        self.assertEqual(len(result['data']), 2)

    def test_log_page44(self):
        '''分页检索系统日志列表:输入pageNum为字符串查询日志'''
        params_data = {'pageNum': 'a',
                       'pageSize': 1
                       }
        response = self.session.get(log_page_api, params=params_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertFalse(success)
        self.assertIn(u'pageNumFailed', msg)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(result)

    def test_log_page45(self):
        '''分页检索系统日志列表:输入pageSize为字符串查询日志'''
        params_data = {'pageNum': 1,
                       'pageSize': 'a'
                       }
        response = self.session.get(log_page_api, params=params_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertFalse(success)
        self.assertIn(u'pageSizeFailed', msg)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(result)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    unittest.main()