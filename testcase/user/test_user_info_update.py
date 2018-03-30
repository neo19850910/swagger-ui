#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query
import json
from command.get_unique import rand_name

class UserInfoUpdate(unittest.TestCase):
    '''更新个人信息'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.sql = '''select name from user where is_delete=0 order by id desc limit 1;'''
        self.data = {
            "id": 1,
            "name": '超级管理员1',
            "sex": True,
        }

    def test_user_info_update106(self):
        '''更新个人信息:正常更新'''
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api,headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)

    def test_user_info_update107(self):
        '''更新个人信息:name为空更新'''
        self.data['name'] = None
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_user_info_update108(self):
        '''更新个人信息:sex为空更新'''
        self.data['sex'] = None
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)

    def test_user_info_update109(self):
        '''更新个人信息:name已存在更新'''
        self.data['name'] = 'cdsihan'
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_user_info_update110(self):
        '''更新个人信息:修改值为本身自己的name'''
        self.data['name'] = query(self.sql)[0]
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_user_info_update111(self):
        '''更新个人信息:修改name超过25位（26位）'''
        self.data['name'] = rand_name(26)
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name只能是6-25位且不能有空格]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_user_info_update112(self):
        '''更新个人信息:修改name低于6位（5位）'''
        self.data['name'] = rand_name(5)
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name只能是6-25位且不能有空格]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_user_info_update113(self):
        '''更新个人信息:name为特殊字符更新'''
        self.data['name'] = '!@#$%^&*'
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)

    def test_user_info_update114(self):
        '''更新个人信息:name包含空格更新'''
        self.data['name'] = '      451212'
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name只能是6-25位且不能有空格]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_user_info_update115(self):
        '''更新个人信息:name为中文更新'''
        self.data['name'] = '我爱你中国，亲爱的祖国'
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)

    def test_user_info_update116(self):
        '''更新个人信息:修改已注销的账号'''
        sql = '''
            select name from user where is_delete=1 order by id desc limit 1;
        '''
        name = query(sql)[0]
        self.data['name'] = name
        json_data = json.dumps(self.data)
        response = self.session.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_user_info_update117(self):
        '''更新个人信息:未登录修改个人信息'''
        json_data = json.dumps(self.data)
        response = requests.post(user_info_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def tearDown(self):
        sql = '''
            update user set name='超级管理员',username='admin' where id=1;
        '''
        query(sql)
        self.session.cookies.clear_session_cookies()
        self.assertEqual(self.verificationErrors, [], 'test has bug!')


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(UserInfoUpdate("test_user_info_update120"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)