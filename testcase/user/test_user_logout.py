#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *

class UserLogout(unittest.TestCase):
    '''用户退出'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_user_logout118(self):
        '''用户退出:正常退出'''
        response = self.session.get(user_logout_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_logout119(self):
        '''用户退出:未登录退出'''
        response = requests.get(user_logout_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual(self.verificationErrors, [], 'test has bug!')


if __name__ == '__main__':
    unittest.main()