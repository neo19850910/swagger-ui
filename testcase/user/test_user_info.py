#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *

class UserInfo(unittest.TestCase):
    '''获取个人信息'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_user_info132(self):
        '''获取个人信息:正常获取个人信息'''
        response = self.session.get(user_info_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertEqual(result['username'], 'admin')
        self.assertEqual(response.status_code, 200)

    def test_user_info133(self):
        '''获取个人信息:未登录获取个人信息'''
        response = requests.get(user_info_api)
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