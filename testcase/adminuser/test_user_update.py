#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query
from command.get_unique import rand_name
class UserUpdate(unittest.TestCase):
    '''更新用户'''
    sql = '''
        select id from user where is_delete=0 order by id desc;
    '''
    id_id = query(sql)[0]

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.data = {
            "id": UserUpdate.id_id,
            "name": rand_name(25),
            "password": "123456",
            "roleIds": [2],
        }

    def test_user_update171(self):
        '''更新用户:正常更新用户'''
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update172(self):
        '''更新用户:id不存在更新用户'''
        self.data['id'] = 9999999
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'更新用户id不存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update173(self):
        '''更新用户:角色id为非int数组更新用户'''
        self.data['roleIds'] = ['a']
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update174(self):
        '''更新用户:角色id不是数组更新用户'''
        self.data['roleIds'] = 'a'
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update175(self):
        '''更新用户:角色id为空数组更新用户'''
        self.data['roleIds'] = []
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update176(self):
        '''更新用户:用户昵称已被占用更新用户'''
        self.data['name'] = 'cdsihan'
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'该用户名或用户昵称已被注册', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update177(self):
        '''更新用户:未登录更新用户'''
        response = requests.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_update178(self):
        '''更新用户:无权限更新用户'''
        login_session = get_session(data_no_permission)
        response = login_session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_update179(self):
        '''更新用户:更新用户为锁定禁止登录'''
        account = {'username': '123456', 'password': '123456','rememberMe':False}
        self.data['locked'] = True
        self.session.post(user_update_api,headers=json_header,json=self.data)
        login_session = requests.post(user_login_api,data=account)
        login_data = login_session.json()
        login_msg = login_data['msg']
        login_success = login_data['success']
        login_result = login_data['result']
        self.assertEqual(u'超过了尝试登录的次数，您的账户已经被锁定。', login_msg)
        self.assertFalse(login_success)
        self.assertIsNone(login_result)
        self.assertEqual(login_session.status_code, 200)

    def test_user_update180(self):
        '''更新用户:昵称为空更新用户'''
        self.data['name'] = None
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update181(self):
        '''更新用户:密码为空更新用户'''
        self.data['password'] = None
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[password不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update182(self):
        '''更新用户:更新已删除用户'''
        delete_sql = '''
            select id from user where is_delete=1;
        '''
        delete_id = query(delete_sql)
        self.data['id'] = delete_id
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update183(self):
        '''更新用户:角色id为空更新用户'''
        self.data['roleIds'] = None
        response = self.session.post(user_update_api,headers=json_header,json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[roleIds不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_update184(self):
        '''更新用户:角色id不存在更新用户'''
        self.data['roleIds'] = [9999999]
        response = self.session.post(user_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'角色Id不存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    unittest.main()