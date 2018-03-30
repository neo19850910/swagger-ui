#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
import time
from command.con_mysql import query

class PerssionAdd(unittest.TestCase):
    '''添加权限'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_permission_add46(self):
        '''添加权限:直接创建权限'''
        add_data = {
              "available": True,
              "icon": "string",
              "identify": str(time.time()),
              "name": str(time.time()),
              "parentId": 0,
              "resourceType": "button",
              "sort": 0,
              "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data )
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg,u'操作成功')
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add47(self):
        '''添加权限:name重复创建权限'''
        sql = '''
                select name from permission limit 1;        
            '''
        sql_name = query(sql)[0]
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": sql_name,
            "parentId": 0,
            "resourceType": "button",
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'权限名称或权限标识或Url已经存在')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add48(self):
        '''添加权限:标识符重复创建权限'''
        sql = '''
                        select name from permission limit 1;        
                    '''
        sql_name = query(sql)[0]
        add_data = {
            "available": True,
            "icon": "string",
            "identify": sql_name,
            "name": str(time.time()),
            "parentId": 0,
            "resourceType": "button",
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'权限名称或权限标识或Url已经存在')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add49(self):
        '''添加权限:没权限创建权限'''
        log_session = get_session(data_no_permission)
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": str(time.time()),
            "parentId": 0,
            "resourceType": "button",
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = log_session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_add50(self):
        '''添加权限:未登录创建权限'''
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": str(time.time()),
            "parentId": 0,
            "resourceType": "button",
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = requests.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_add51(self):
        '''添加权限:parent_id为空创建权限'''
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": str(time.time()),
            "parentId": None,
            "resourceType": "button",
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'[parentId不能为null]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add52(self):
        '''添加权限:name为空创建权限'''
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": None,
            "parentId": 0,
            "resourceType": "button",
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'[name不能为空]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add53(self):
        '''添加权限:resourceType为空创建权限'''
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": str(time.time()),
            "parentId": 0,
            "resourceType": None,
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'[resourceType不能为空]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add54(self):
        '''添加权限:identify为空创建权限'''
        add_data = {
            "available": True,
            "icon": "string",
            "identify": None,
            "name": str(time.time()),
            "parentId": 0,
            "resourceType":'button',
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'[identify不能为空]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add55(self):
        '''添加权限:name长度超过20创建权限'''
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": '1'*21,
            "parentId": 0,
            "resourceType": 'button',
            "sort": 0,
            "url": str(time.time())
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'[name长度需要在1和20之间]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_permission_add56(self):
        '''添加权限:url重复创建权限'''
        sql = '''
                        select url from permission where url is not Null limit 1;    
                    '''
        sql_name = query(sql)[0]
        add_data = {
            "available": True,
            "icon": "string",
            "identify": str(time.time()),
            "name": str(time.time()),
            "parentId": 0,
            "resourceType": "button",
            "sort": 0,
            "url": sql_name
        }
        json_data = json.dumps(add_data)
        response = self.session.post(permission_add_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(msg, u'权限名称或权限标识或Url已经存在')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    unittest.main()