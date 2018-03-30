#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
from command.get_unique import rand_name
from command.con_mysql import query

class UserAdd(unittest.TestCase):
    '''添加用户'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.data = {
                  "name": rand_name(20),
                  "password": '123456',
                  "roleIds": [
                    2
                  ],
                  "sex": True,
                  "username": rand_name(20)
                }

    def test_user_add134(self):
        '''添加用户:正常添加用户'''
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add135(self):
        '''添加用户:username已被使用添加用户'''
        self.data['username'] = 'huhuan'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add136(self):
        '''添加用户:name已被使用添加用户'''
        self.data['name'] = 'cdsihan'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add137(self):
        '''添加用户:不授予权限添加用户'''
        self.data['roleIds'] = []
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add138(self):
        '''添加用户:username为空添加用户'''
        self.data['username'] = None
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add139(self):
        '''添加用户:name为空添加用户'''
        self.data['name'] = None
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add140(self):
        '''添加用户:密码为空添加用户'''
        self.data['password'] = None
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[password不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add141(self):
        '''添加用户:性别为空添加用户'''
        self.data['sex'] = None
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add142(self):
        '''添加用户:username长度超过25添加用户'''
        self.data['username'] = '1'*26
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username只能是5-25位的字符]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add143(self):
        '''添加用户:username长度低于5添加用户'''
        self.data['username'] = '1' * 4
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username只能是5-25位的字符]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add144(self):
        '''添加用户:name超过25添加用户'''
        self.data['name'] = '1' * 26
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name只能是6-25位且不能有空格]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add145(self):
        '''添加用户:name低于6添加用户'''
        self.data['name'] = '1' * 5
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name只能是6-25位且不能有空格]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add146(self):
        '''添加用户:password长度低于6添加用户'''
        self.data['password'] = '1' * 5
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[password只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add147(self):
        '''添加用户:password长度大于15添加用户'''
        self.data['password'] = '1' * 16
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[password只能是6-15位的字符或数字]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add148(self):
        '''添加用户:未登录添加用户'''
        add_data = json.dumps(self.data)
        response = requests.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_add149(self):
        '''添加用户:无权限用户添加用户'''
        login_session = get_session(data_no_permission)
        add_data = json.dumps(self.data)
        response = login_session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_add150(self):
        '''添加用户:name为中文添加用户'''
        sql = '''
                            delete from user where name = '我爱你伟大的祖国';
                        '''
        query(sql)
        self.data['name'] = '我爱你伟大的祖国'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)


    def test_user_add151(self):
        '''添加用户:name为特殊字符添加用户'''
        sql = '''
                                    delete from user where name = '!@#$%^&amp;'
                                '''
        query(sql)
        self.data['name'] = '!@#$%^&'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add152(self):
        '''添加用户:username为中文添加用户'''
        self.data['username'] = '我爱你伟大的祖国'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username只能是5-25位的字符]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add153(self):
        '''添加用户:username为特殊字符添加用户'''
        self.data['username'] = '!@#$%^&*'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username只能是5-25位的字符]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add154(self):
        '''添加用户:name包含空格添加用户'''
        self.data['name'] = '!@#$ %^&*'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name只能是6-25位且不能有空格]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add155(self):
        '''添加用户:username包含空格添加用户'''
        self.data['username'] = 'has  adfa'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[username只能是5-25位的字符]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add156(self):
        '''添加用户:roleids不是int数组添加用户'''
        self.data['roleIds'] = ['a']
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add157(self):
        '''添加用户:roleids不存在添加用户'''
        self.data['roleIds'] = [99999997]
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'角色Id不存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_add158(self):
        '''添加用户:roleid传入非数组参数'''
        self.data['roleIds'] = '1'
        add_data = json.dumps(self.data)
        response = self.session.post(user_add_api, headers=json_header, data=add_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(UserAdd("test_user_add157"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    unittest.main()