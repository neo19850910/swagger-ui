#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query

class DictPage(unittest.TestCase):
    '''检索字典'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []


    def test_dicts22(self):
        '''检索字典:无参数直接查询'''
        response = self.session.get(dicts_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        sql = '''
            select count(*) from dict where parent_id=0 and is_delete=0;
        '''
        sql_res = query(sql)[0]
        self.assertEqual(msg,u'操作成功')
        self.assertTrue(success)
        self.assertEqual(result['totalCount'],sql_res)
        self.assertEqual(response.status_code,200)

    def test_dicts23(self):
        '''检索字典:输入参数查询'''
        resquests_data = {'pageNum': 2, 'pageSize': 11}
        response = self.session.get(dicts_api, params=resquests_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        sql = '''
                   select count(*) from dict where parent_id=0 and is_delete=0;
               '''
        sql_res = query(sql)[0]
        self.assertEqual(msg, u'操作成功')
        self.assertTrue(success)
        self.assertEqual(result['totalCount'], sql_res)
        self.assertEqual(result['pageNum'], 2)
        self.assertEqual(result['pageSize'], 11)
        self.assertEqual(response.status_code, 200)


    def test_dicts24(self):
        '''检索字典:未登录查询'''
        response = requests.get(dicts_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg,u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_dicts25(self):
        '''检索字典:无权限用户查询字典'''
        response = get_session(data=data_no_permission)
        dicts_response = response.get(dicts_api)
        data = dicts_response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg,u'没有权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(dicts_response.status_code, 401)

    def test_dicts26(self):
        '''检索字典:参数非int查询字典'''
        resquests_data = {'pageNum': 'sa', 'pageSize': '1212'}
        response = self.session.get(dicts_api, params=resquests_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertIn(u'pageNumFailed', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual(self.verificationErrors, [], 'test has bug!')

if __name__ == '__main__':
    unittest.main()
