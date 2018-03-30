#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query
from command.get_unique import rand_name

class RoleUpdate(unittest.TestCase):
    '''修改角色信息'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.data = {
                  "available": True,
                  "id": 0,
                  "identify": "string",
                  "name": "string",
                  "permissionIds": [0]
                }

    def test_role_update220(self):
        '''修改角色信息:正常修改角色信息'''
        role_add_data = {
                  "available": True,
                  "identify": rand_name(20),
                  "name": rand_name(20),
                  "permissionIds": [2,3]
                    }
        self.session.post(role_add_api, headers=json_header, json=role_add_data)
        role_sql = '''
            select id,identify,name from role order by id desc;
        '''
        role_id = query(role_sql)[0]
        identify = query(role_sql)[1]
        name = query(role_sql)[2]
        user_add_data = self.data = {
                    "name": rand_name(20),
                    "password": '123456',
                    "roleIds": [role_id],
                    "sex": True,
                    "username": rand_name(20)
                }
        self.session.post(user_add_api, headers=json_header, json=user_add_data)
        role_update_data = {
                  "available": True,
                  "id": role_id,
                  "identify": identify,
                  "name": name,
                  "permissionIds": [2]
                 }
        self.session.post(role_update_api, headers=json_header, json=role_update_data)
        user_sql = '''
            select username from user order by id desc
        '''
        user_name = query(user_sql)[0]
        login_date = {'username': user_name, 'password': '123456','rememberMe':False}
        login_session = get_session(login_date)
        response = login_session.get(dicts_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_update221(self):
        '''修改角色信息:无权限修改角色信息'''
        login_session = get_session(data_no_permission)
        response = login_session.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_update222(self):
        '''修改角色信息:未登录修改角色信息'''
        response = requests.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_update223(self):
        '''修改角色信息:id不存在修改角色信息'''
        response = self.session.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'更新角色Id不存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_update224(self):
        '''修改角色信息:name重复修改角色信息'''
        self.data['id'] = 2
        self.data['name'] = 'admin'
        response = self.session.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'角色名称或者角色标识已存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_update225(self):
        '''修改角色信息:identify重复修改角色信息'''
        self.data['id'] = 2
        self.data['identify'] = 'admin'
        response = self.session.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'角色名称或者角色标识已存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_update226(self):
        '''修改角色信息:permissionIds不存在修改角色信息'''
        self.data['id'] = 2
        self.data['permissionIds'] = [9999999]
        self.data['identify'] = 'abcdefg'
        self.data['name'] = 'abcdefg'
        response = self.session.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'权限Id不存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_update227(self):
        '''修改角色信息:permissionIds为空修改角色信息'''
        self.data['id'] = 2
        self.data['permissionIds'] = None
        self.data['identify'] = 'abcdefg'
        self.data['name'] = 'abcdefg'
        response = self.session.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[permissionIds不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_update228(self):
        '''修改角色信息:permissionIds为空数组修改角色信息'''
        self.data['id'] = 2
        self.data['permissionIds'] = []
        self.data['identify'] = 'abcdefg'
        self.data['name'] = 'abcdefg'
        response = self.session.post(role_update_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_update229(self):
        '''修改角色信息:permissionIds为字符数组修改角色信息'''
        self.data['id'] = 2
        self.data['permissionIds'] = 'update(select max(id) from role)'
        self.data['identify'] = 'abcdefg'
        self.data['name'] = 'abcdefg'
        response = self.session.post(role_update_api, headers=json_header, json=self.data)
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
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(RoleUpdate("test_role_update220"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)