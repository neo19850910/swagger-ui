#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query

class RoleList(unittest.TestCase):
    '''获得简单的角色信息(没有权限信息)'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_role_list209(self):
        '''获得简单的角色信息:正常获得简单的角色信息'''
        sql = '''
            select count(*) from role where is_delete=0;
            '''
        count = query(sql)[0]
        response = self.session.get(role_list_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertEqual(len(result), count)
        self.assertTrue(success)
        self.assertEqual(response.status_code, 200)

    def test_role_list210(self):
        '''获得简单的角色信息:没有登录获得简单的角色信息'''
        response = requests.get(role_list_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_role_list211(self):
        '''获得简单的角色信息:无权限获得简单的角色信息'''
        login_session = get_session(data_no_permission)
        response = login_session.get(role_list_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")


if __name__ == '__main__':
    unittest.main()