#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.get_unique import rand_name
from command.con_mysql import query

class RoleAdd(unittest.TestCase):
    '''添加角色信息'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.data = {
                  "available": True,
                  "identify": rand_name(30),
                  "name": rand_name(20),
                  "permissionIds": [1]
        }

    def test_role_add185(self):
        '''添加角色信息:正常添加角色'''
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add186(self):
        '''添加角色信息:未登录添加角色'''
        response = requests.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_add187(self):
        '''添加角色信息:无权限添加角色'''
        login_session = get_session(data_no_permission)
        response = login_session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_add188(self):
        '''添加角色信息:权限为空数组添加角色'''
        self.data['permissionIds'] = None
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[permissionIds不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add189(self):
        '''添加角色信息:角色名称重复添加角色'''
        self.data['name'] = 'admin'
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'角色名称或者角色标识已存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add190(self):
        '''添加角色信息:identify重复添加角色'''
        self.data['identify'] = 'admin'
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'角色名称或者角色标识已存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add191(self):
        '''添加角色信息:available为False添加角色再相关角色用户请求相关接口'''
        self.data['available'] = False
        self.data['permissionIds'] = [2, 3]
        sql = '''
                    select max(id) from role; 
                '''
        role_id = query(sql)
        self.session.post(role_add_api, headers=json_header, json=self.data)
        update_data = {
                  "id": 3,
                  "name": "胡桓",
                  "password": "123456",
                  "roleIds": [role_id],
                }
        self.session.post(user_update_api, headers=json_header, json=update_data)
        login_date = {'username': 'cbbtest', 'password': '123456','rememberMe':False}
        login_session = get_session(login_date)
        response = login_session.get(user_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_add192(self):
        '''添加角色信息:permissionIds为非数组添加角色'''
        self.data['permissionIds'] = 'a'
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add193(self):
        '''添加角色信息:permissionIds为字符串数组添加角色'''
        self.data['permissionIds'] = ['a']
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add194(self):
        '''添加角色信息:权限id不存在添加角色'''
        self.data['permissionIds'] = [0]
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'权限Id不存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add195(self):
        '''添加角色信息:角色名称低于2位添加角色'''
        self.data['name'] = '我'
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name长度需要在2和20之间]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add196(self):
        '''添加角色信息:角色名称高于20位添加角色'''
        self.data['name'] = '我' * 21
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name长度需要在2和20之间]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add197(self):
        '''添加角色信息:identify低于3位添加角色'''
        self.data['identify'] = '1' * 2
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[identify长度需要在3和30之间]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add198(self):
        '''添加角色信息:identify高于30位添加角色'''
        self.data['identify'] = '1' * 31
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[identify长度需要在3和30之间]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add199(self):
        '''添加角色信息:角色名称为空添加角色'''
        self.data['name'] = None
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_add200(self):
        '''添加角色信息:identify为空添加角色'''
        self.data['identify'] = None
        response = self.session.post(role_add_api, headers=json_header, json=self.data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[identify不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(RoleAdd('test_role_add191'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)