#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.get_unique import rand_name
from command.con_mysql import query

class UserRegister(unittest.TestCase):
    '''用户注册'''
    def setUp(self):
        self.verificationErrors = []

    def test_user_register92(self):
        '''用户注册:正常注册（username长度25位）'''
        register_data = {
            'name': rand_name(10),
            'username':rand_name(25),
            'password':'123456',
            'sex':False
        }
        response = requests.post(user_register_api,data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register93(self):
        '''用户注册:注册数据库已存在的username用户'''
        register_data = {
            'name': rand_name(10),
            'username': 'huhuan',
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register94(self):
        '''用户注册:不输入username注册'''
        register_data = {
            'name': rand_name(10),
            'username': None,
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register95(self):
        '''用户注册:不输入name注册'''
        register_data = {
            'name': None,
            'username': rand_name(10),
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register96(self):
        '''用户注册:不输入密码注册'''
        register_data = {
            'name': rand_name(10),
            'username': rand_name(10),
            'password': None,
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[password不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register97(self):
        '''用户注册:正常注册（username长度低于5位）'''
        register_data = {
            'name': rand_name(10),
            'username': rand_name(4),
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username只能是5-25位的字符]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register98(self):
        '''用户注册:不选择性别注册'''
        register_data = {
            'name': rand_name(10),
            'username': rand_name(10),
            'password': '123456',
            'sex': None
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register99(self):
        '''用户注册:username长度超过25注册'''
        register_data = {
            'name': rand_name(6),
            'username': rand_name(26),
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username只能是5-25位的字符]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register100(self):
        '''用户注册:使用已注销的username注册'''
        sql = '''select username from user where is_delete=1 limit 1'''
        username = query(sql)[0]
        register_data = {
            'name': rand_name(6),
            'username': username,
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register101(self):
        '''用户注册:注册数据库已存在的name用户'''
        sql = '''
            select name from user where is_delete=0 limit 2,3;
        '''
        name_sql = query(sql)[0]
        register_data = {
            'name': name_sql,
            'username': rand_name(17),
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register102(self):
        '''用户注册:注册数据库已存在的name的注销用户'''
        register_data = {
            'name': '0327152906',
            'username': rand_name(17),
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register103(self):
        '''用户注册:注册（username长度6位，name5位）'''
        register_data = {
            'name': rand_name(6),
            'username': rand_name(5),
            'password': '123456',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register104(self):
        '''用户注册:注册（密码5位）'''
        register_data = {
            'name': rand_name(20),
            'username': rand_name(20),
            'password': '12345',
            'sex': False
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[password只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_register105(self):
        '''用户注册:注册（密码15位）'''
        register_data = {
            'name': rand_name(6),
            'username': rand_name(6),
            'password': '1234567890123456',
            'sex': True
        }
        response = requests.post(user_register_api, data=register_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[password只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.assertEqual(self.verificationErrors, [], 'test has bug!')

if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(UserRegister("test_user_register105"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)