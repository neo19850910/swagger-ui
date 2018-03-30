#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
from command.con_mysql import query

class PerssionList(unittest.TestCase):
    '''获得所有权限（数组形式）'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_permission_list62(self):
        '''获得所有权限（数组形式):直接查询菜单权限'''
        sql = '''
            select count(*) from permission where is_delete=0;
        '''
        sql_count = query(sql)[0]
        response = self.session.get(permission_list_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'操作成功')
        self.assertTrue(success)
        self.assertEqual(sql_count, len(result))
        for i in result:
            self.assertIsNone(i['children'])


    def test_permission_list63(self):
        '''获得所有权限（数组形式):无权限查询菜单权限'''
        login_session = get_session(data_no_permission)
        response = login_session.get(permission_list_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_list64(self):
        '''获得所有权限（数组形式):没登录查询菜单权限'''
        response = requests.get(permission_list_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(PerssionList("test_permission_list62"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)