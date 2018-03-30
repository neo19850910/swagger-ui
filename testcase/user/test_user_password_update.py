#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *

def update_password(oldpassword):
    data = {
        'oldPassword': oldpassword,
        'newPassword': '123456',
    }
    update_data = {'username': 'admin', 'password': oldpassword, 'rememberMe': False}
    login_new = get_session(update_data)
    response = login_new.post(user_password_update_api, data=data)
    response.cookies.clear_session_cookies()
    return 0

class UserPassword(unittest.TestCase):
    '''修改密码'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.data = {
            'oldPassword': '123456',
            'newPassword':'123456',
        }
    def test_user_password_update120(self):
        '''修改密码:正常修改，密码长度15位'''
        self.data['newPassword'] = '123456789012345'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.data['oldPassword'] = '123456789012345'
        update_password(self.data['oldPassword'])
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update121(self):
        '''修改密码:正常修改，密码长度6位'''
        self.data['newPassword'] = '000000'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.data['oldPassword'] = '000000'
        update_password(self.data['oldPassword'])
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update122(self):
        '''修改密码:再请求修改密码'''
        self.data['newPassword'] = '000000'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        else_response = self.session.get(user_logout_api)
        else_data = else_response.json()
        else_msg = else_data['msg']
        else_success = else_data['success']
        else_result = else_data['result']
        update_password(self.data['newPassword'])
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(u'没有登录',else_msg )
        self.assertFalse(else_success)
        self.assertIsNone(else_result)
        self.assertEqual(else_response.status_code, 401)

    def test_user_password_update123(self):
        '''修改密码:长度为16位'''
        self.data['newPassword'] = '1234567890123456'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[newPassword只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update124(self):
        '''修改密码:长度为5位'''
        self.data['newPassword'] = '12345'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[newPassword只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update125(self):
        '''修改密码:新密码为空'''
        self.data['newPassword'] = ''
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'newPassword不能为空', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update126(self):
        '''修改密码:旧密码为空'''
        self.data['oldPassword'] = ''
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'oldPassword不能为空', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update127(self):
        '''修改密码:新密码为特殊字符'''
        self.data['newPassword'] = '!@#$%^&*'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[newPassword只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update128(self):
        '''修改密码:新密码为中文'''
        self.data['newPassword'] = '我爱你我的祖国'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[newPassword只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update129(self):
        '''修改密码:新密码包含空格'''
        self.data['newPassword'] = 'asas sasas'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[newPassword只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update130(self):
        '''修改密码:旧密码不匹配'''
        self.data['oldPassword'] = 'asdfghjkl'
        response = self.session.post(user_password_update_api, data=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'原密码错误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_password_update131(self):
        '''修改密码:未登录修改密码'''
        response = requests.post(user_password_update_api, data=self.data)
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
    # suite = unittest.TestSuite()
    # suite.addTest(UserPassword("test_user_password_update126"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)