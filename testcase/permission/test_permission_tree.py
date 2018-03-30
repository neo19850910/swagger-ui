#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query

class PerssionTree(unittest.TestCase):
    '''获得所有权限（树状形式）'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_permission_menu68(self):
        '''获得所有权限（树状形式）:直接查询（树状形式）'''
        # sql = '''
        #        select count(*) from permission where parent_id = 0 and resource_type = 'menu';
        #    '''
        # count = query(sql)[0]
        response = self.session.get(permission_tree_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        # self.assertEqual(count, len(result))
        self.assertEqual(response.status_code, 200)

    def test_permission_menu69(self):
        '''获得所有权限（树状形式）:无权限查询（树状形式）'''
        login_session = get_session(data_no_permission)
        response = login_session.get(permission_tree_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_menu70(self):
        '''获得所有权限（树状形式）:没登录查询（树状形式）'''
        response = requests.get(permission_tree_api)
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