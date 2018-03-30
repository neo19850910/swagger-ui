#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query

class RolePage(unittest.TestCase):
    '''分页获得角色信息'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_role_page212(self):
        '''分页获得角色信息:不输入参数分页获得角色信息'''
        sql = '''
            select count(*) from role where is_delete=0;
        '''
        count = query(sql)[0]
        response = self.session.get(role_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertEqual((result['totalCount']), count)
        self.assertTrue(success)
        self.assertEqual(response.status_code, 200)

    def test_role_page213(self):
        '''分页获得角色信息:无权限分页获得角色信息'''
        login_session = get_session(data_no_permission)
        response = login_session.get(role_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertIsNone(result)
        self.assertFalse(success)
        self.assertEqual(response.status_code, 401)

    def test_role_page214(self):
        '''分页获得角色信息:未登录分页获得角色信息'''
        response = requests.get(role_page_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertIsNone(result)
        self.assertFalse(success)
        self.assertEqual(response.status_code, 401)

    def test_role_page215(self):
        '''分页获得角色信息:输入参数分页获取角色信息'''
        page = {'pageNum':1,'pageSize':5}
        response = self.session.get(role_page_api, params=page)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertEqual(len(result['data']), page['pageSize'])
        self.assertTrue(success)
        self.assertEqual(response.status_code, 200)

    def test_role_page216(self):
        '''分页获得角色信息:pageNum为字母分页获得角色信息'''
        page = {'pageNum': 'a', 'pageSize': 5}
        response = self.session.get(role_page_api, params=page)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'Failed', msg)
        self.assertFalse(success)
        self.assertEqual(response.status_code, 200)

    def test_role_page217(self):
        '''分页获得角色信息:pageNum为中文分页获得角色信息'''
        page = {'pageNum': '你好', 'pageSize': 5}
        response = self.session.get(role_page_api, params=page)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'Failed', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_page218(self):
        '''分页获得角色信息:pageSize为字母分页获得角色信息'''
        page = {'pageNum': 1, 'pageSize': 'a'}
        response = self.session.get(role_page_api, params=page)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'Failed', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_role_page219(self):
        '''分页获得角色信息:pageSize为数组分页获得角色信息'''
        page = {'pageNum': 1, 'pageSize': [2,'a','b','c']}
        response = self.session.get(role_page_api, params=page)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertIn(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNotNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")


if __name__ == '__main__':
    unittest.main()