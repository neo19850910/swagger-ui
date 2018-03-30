#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *


class UserLogin(unittest.TestCase):
    '''用户登录'''

    def setUp(self):
        self.verificationErrors = []

    def test_user_login85(self):
        '''用户登录:数据库存在用户登录'''
        response = requests.post(user_login_api, data=login_admin)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_login86(self):
        '''用户登录:数据库不存在用户登录'''
        data = {'username':'notexist', 'password':'123456', 'rememberMe':False}
        response = requests.post(user_login_api, data=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        self.assertEqual(u'用户名或密码错误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_login87(self):
        '''用户登录:数据库停用用户登录'''
        pass

    def test_user_login88(self):
        '''用户登录:不输入密码登录'''
        data = {'username': 'admin', 'password': None, 'rememberMe': False}
        response = requests.post(user_login_api, data=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        self.assertEqual(u'[password不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_login89(self):
        '''用户登录:不选择rememberMe字段登录'''
        data = {'username': 'admin', 'password': '123456', 'rememberMe': None}
        response = requests.post(user_login_api, data=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        self.assertEqual(u'[rememberMe不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_login90(self):
        '''用户登录:不输入用户名登录'''
        data = {'username': None, 'password': '123456', 'rememberMe': False}
        response = requests.post(user_login_api, data=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        self.assertEqual(u'[username不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_login91(self):
        '''用户登录:输入错误密码登录'''
        data = {'username': 'admin', 'password': '1234567', 'rememberMe': False}
        response = requests.post(user_login_api, data=data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        self.assertEqual(u'用户名或密码错误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.assertEqual(self.verificationErrors, [], 'test has bug!')

if __name__ == '__main__':
    unittest.main()