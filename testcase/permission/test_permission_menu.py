#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query

class PerssionMenu(unittest.TestCase):
    '''查询用户的所有权限的菜单权限'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_permission_menu65(self):
        '''查询用户的所有权限的菜单权限:直接查询菜单权限'''
        sql = '''
            select count(*) from permission where parent_id = 0 and resource_type = 'menu';
        '''
        count = query(sql)[0]
        response = self.session.get(permission_menu_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertEqual(count, len(result))
        self.assertEqual(response.status_code, 200)

    def test_permission_menu66(self):
        '''查询用户的所有权限的菜单权限:非admin用户查询菜单权限'''
        login_session = get_session(data_no_permission)
        response = login_session.get(permission_menu_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        # self.assertEqual(len(result), 1)
        self.assertEqual(response.status_code, 200)

    def test_permission_menu67(self):
        '''查询用户的所有权限的菜单权限:没登录查询菜单权限'''
        response = requests.get(permission_menu_api)
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
        self.assertEqual([], self.verificationErrors, "test has bug!")


if __name__ == '__main__':
    unittest.main()