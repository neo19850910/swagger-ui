#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query
from command.get_unique import rand_name

cbb = {'username': 'cbbtest', 'password': '123456','rememberMe':False}

class RoleDelete(unittest.TestCase):
    '''删除角色信息'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_role_delete201(self):
        '''删除角色信息:正常删除角色'''
        roleIds = [3]
        response = self.session.post(role_delete_api, headers=json_header, json=roleIds)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        sql = '''
            update role_permission set is_delete=0 where id=3;
        '''
        sql1 = '''
            update role set is_delete=0 where id=3;
        '''
        sql2= '''
            update user_role set is_delete=0 where id=3;
        '''
        query(sql)
        query(sql1)
        query(sql2)
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_delete202(self):
        '''删除角色信息:未登录删除角色'''
        roleIds = []
        response = requests.post(role_delete_api, headers=json_header, json=roleIds)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_delete203(self):
        '''删除角色信息:没有权限删除角色'''
        roleIds = []
        login_session = get_session(data_no_permission)
        response = login_session.post(role_delete_api, headers=json_header, json=roleIds)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_delete204(self):
        '''删除角色信息:删除角色用户再请求之前有权限接口'''
        role_sql = '''select max(role_id) from user_role where user_id = 3 and is_delete = 0 '''
        role_id = query(role_sql)[0]
        roleIds = [role_id]
        self.session.post(role_delete_api, headers=json_header, json=roleIds)  #删除角色（关联用户是cbbtest）
        add_data = {
                  "available": True,
                  "identify": rand_name(30),
                  "name": rand_name(20),
                  "permissionIds": [2,3,4]
        }
        self.session.post(role_add_api, headers=json_header, json=add_data)   #添加新的角色,且拥有之前的3,4(查看日志)权限
        sql = '''
                    select max(id) from role; 
                '''
        role_id = query(sql)[0]               #获取最新生成的role_id
        update_data = {
            "id": 3,
            "name": 'cbbtest',
            "password": "123456",
            "roleIds": [role_id],
        }
        self.session.post(user_update_api, headers=json_header, json=update_data)    #修改用户的role为最新的role_id
        login_session = get_session(cbb)
        response = login_session.get(dicts_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNotNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_delete205(self):
        '''删除角色信息:roleIds为空删除角色'''
        roleIds = None
        response = self.session.post(role_delete_api, headers=json_header, json=roleIds)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_delete206(self):
        '''删除角色信息:roleIds为非int数组删除角色'''
        roleIds = ['a']
        response = self.session.post(role_delete_api, headers=json_header, json=roleIds)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_delete207(self):
        '''删除角色信息:roleIds为空数组删除角色'''
        roleIds = []
        response = self.session.post(role_delete_api, headers=json_header, json=roleIds)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_delete208(self):
        '''删除角色信息:roleIds为非数组实参删除角色'''
        roleIds = 'a'
        response = self.session.post(role_delete_api, headers=json_header, json=roleIds)
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
    # suite.addTest(RoleDelete('test_role_delete204'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)