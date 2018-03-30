#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
import time
from command.con_mysql import query

class PerssionDelete(unittest.TestCase):
    '''删除权限'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_permission_delete57(self):
        '''删除权限:直接删除权限'''
        sql = '''
            select max(id) from permission where is_delete = 0 limit 1;       
        '''
        sql_id = [query(sql)[0]]
        json_data = json.dumps(sql_id)
        response = self.session.post(permission_delete_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'操作成功')
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_delete58(self):
        '''删除权限:有子权限的直接删除权限'''
        sql = '''
                    select max(a.id) from permission a inner join permission b where a.is_delete = 0 and a.id =b.parent_id;       
                '''
        sql_id = [query(sql)[0]]
        json_data = json.dumps(sql_id)
        response = self.session.post(permission_delete_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'不能删除有子权限的权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_delete59(self):
        '''删除权限:无权限删除权限'''
        login_session = get_session(data_no_permission)
        sql = '''
                    select max(id) from permission where is_delete = 0 limit 1;       
                '''
        sql_id = [query(sql)[0]]
        json_data = json.dumps(sql_id)
        response = login_session.post(permission_delete_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_delete60(self):
        '''删除权限:未登录删除权限'''
        sql = '''
                            select max(id) from permission where is_delete = 0 limit 1;       
                        '''
        sql_id = [query(sql)[0]]
        json_data = json.dumps(sql_id)
        response = requests.post(permission_delete_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_delete61(self):
        '''删除权限:数组里面参数为string删除权限'''
        string = ['a']
        json_data = json.dumps(string)
        response = self.session.post(permission_delete_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'传入数据有误')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")


if __name__ == '__main__':
    unittest.main()
