#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query

class UserPage(unittest.TestCase):
    '''分页查询用户'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_user_page165(self):
        '''分页查询用户:不输入参数查询用户'''
        sql = '''
            select count(*) from user where is_delete=0;
        '''
        count = query(sql)[0]
        response = self.session.get(user_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNotNone(result)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, result['totalCount'])

    def test_user_page166(self):
        '''分页查询用户:未登录查询用户'''
        response = requests.get(user_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_page167(self):
        '''分页查询用户:无权限查询用户'''
        login_session = get_session(data_no_permission)
        response = login_session.get(user_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_page168(self):
        '''分页查询用户:pageNum不是int查询用户'''
        data = {'pageNum':'a', 'pageSize':10}
        response = self.session.get(user_page_api,params=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'Failed', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_page169(self):
        '''分页查询用户:pageSize不是int查询用户'''
        data = {'pageNum': 1, 'pageSize': 'a'}
        response = self.session.get(user_page_api, params=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'Failed', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_page170(self):
        '''分页查询用户:输入pageNum和pageSize查询用户'''
        data = {'pageNum': 1, 'pageSize': 5}
        response = self.session.get(user_page_api, params=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNotNone(result)
        self.assertEqual(result['pageNum'],1)
        self.assertEqual(result['pageSize'], 5)
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    unittest.main()