#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
from command.con_mysql import query

class UserDelete(unittest.TestCase):
    '''删除用户'''

    sql = '''
                select id from user where is_delete=0 order by id desc limit 1;
            '''
    user_id = query(sql)[0]

    @classmethod
    def recover(cls, user_id):
        update_sql = '''
                update user set is_delete=0 where id=%s;
            '''
        return query(update_sql, user_id)

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.user_id = UserDelete.user_id
        self.json_id = json.dumps([self.user_id])

    def test_user_delete159(self):
        '''删除用户:正常批量删除用户'''
        response = self.session.post(user_delete_api, headers=json_header,data=self.json_id)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        UserDelete.recover(self.user_id)
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_delete160(self):
        '''删除用户:无权限删除用户'''
        login_session = get_session(data_no_permission)
        response = login_session.post(user_delete_api, headers=json_header,data=self.json_id)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_delete161(self):
        '''删除用户:未登录删除用户'''
        response = requests.post(user_delete_api, headers=json_header, data=self.json_id)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_user_delete162(self):
        '''删除用户:userids非int数组删除用户'''
        user_id = ['a']
        json_id = json.dumps(user_id)
        response = self.session.post(user_delete_api, headers=json_header, data=json_id)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        # UserDelete.recover(self.id)
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_delete163(self):
        '''删除用户:userids非数组删除用户'''
        user_id = 'a'
        json_id = json.dumps(user_id)
        response = self.session.post(user_delete_api, headers=json_header, data=json_id)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        # UserDelete.recover(self.id)
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_user_delete164(self):
        '''删除用户:删除已被注销用户'''
        sql = '''
            select id from user where is_delete=1;
        '''
        id_id = query(sql)[0]
        json_id = json.dumps([id_id])
        response = self.session.post(user_delete_api, headers=json_header, data=json_id)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    unittest.main()