#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
import time
from command.con_mysql import query

class PerssionUpdate(unittest.TestCase):
    '''更新权限'''

    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_permission_update71(self):
        '''更新权限:正常修改权限'''
        name = str(time.time())
        time.sleep(0.01)
        identify = str(time.time())
        sql = '''
            select max(id) from permission where is_delete=0;
        '''
        id = query(sql)[0]
        sql_identify = '''
                    select identify from permission where id=%s;
                '''
        sql_name = '''
                select name from permission where id=%s
        '''
        updata_data = {
                "id": id,
                "identify": identify,
                "name": name,
                "resourceType": "button",
            }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        identify_update = query(sql_identify, id)[0]
        name_update = query(sql_name, id)[0]
        self.assertEqual(u'操作成功', msg)
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(identify_update, identify)
        self.assertEqual(name_update, name)

    def test_permission_update72(self):
        '''更新权限:无权限修改权限'''
        login_session = get_session(data_no_permission)
        name = str(time.time())
        time.sleep(0.01)
        identify = str(time.time())
        sql = '''
                    select max(id) from permission where is_delete=0;
                '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": name,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = login_session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有权限', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_update73(self):
        '''更新权限:未登录修改权限'''
        name = str(time.time())
        time.sleep(0.01)
        identify = str(time.time())
        sql = '''
                            select max(id) from permission where is_delete=0;
                        '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": name,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = requests.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'没有登录', msg)
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_permission_update74(self):
        '''更新权限:identify为空修改权限'''
        name = str(time.time())
        sql = '''
                    select max(id) from permission where is_delete=0;
                '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": None,
            "name": name,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[identify不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update75(self):
        '''更新权限:name为空修改权限'''
        identify = str(time.time())
        sql = '''
                            select max(id) from permission where is_delete=0;
                        '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": None,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[name不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update76(self):
        '''更新权限:id为空修改权限'''
        identify = str(time.time())
        name = str(time.time())
        updata_data = {
            "id": None,
            "identify": identify,
            "name": name,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[id不能为null]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update77(self):
        '''更新权限:resourceType为空修改权限'''
        identify = str(time.time())
        name = str(time.time())
        sql = '''
                                    select max(id) from permission where is_delete=0;
                                '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": name,
            "resourceType": None,
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'[resourceType不能为空]', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update78(self):
        '''更新权限:name重复修改权限'''
        identify = str(time.time())
        sql = '''
                    select max(id) from permission where is_delete=0;
                '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": u'首页',
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'权限名称或权限标识或Url已经存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)


    def test_permission_update79(self):
        '''更新权限:identify重复修改权限'''
        name = str(time.time())
        sql = '''
                            select max(id) from permission where is_delete=0;
                        '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": 'sys:index:menu',
            "name": name,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'权限名称或权限标识或Url已经存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update80(self):
        '''更新权限:resourceType类型错误修改权限'''
        name = str(time.time())
        identify = str(time.time())
        sql = '''
                                    select max(id) from permission where is_delete=0;
                                '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": name,
            "resourceType": [1],
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update81(self):
        '''更新权限:name类型错误修改权限'''
        identify = str(time.time())
        sql = '''
                                            select max(id) from permission where is_delete=0;
                                        '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": [1],
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update82(self):
        '''更新权限:identify类型错误修改权限'''
        name = str(time.time())
        sql = '''
                                                    select max(id) from permission where is_delete=0;
                                                '''
        id = query(sql)[0]
        updata_data = {
            "id": id,
            "identify": [1],
            "name": name,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update83(self):
        '''更新权限:id类型错误修改权限'''
        name = str(time.time())
        identify = str(time.time())
        sql = '''
                                                            select max(id) from permission where is_delete=0;
                                                        '''
        id = query(sql)[0]
        updata_data = {
            "id": 'a',
            "identify": identify,
            "name": name,
            "resourceType": "button",
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def test_permission_update84(self):
        '''更新权限:url重复修改权限'''
        name = str(time.time())
        identify = str(time.time())
        sql = '''
                                                                    select max(id) from permission where is_delete=0;
                                                                '''
        id = query(sql)[0]
        url_sql = '''
            select url from permission where is_delete=0 order by id asc limit 1;
        '''
        url = query(url_sql)[0]
        updata_data = {
            "id": id,
            "identify": identify,
            "name": name,
            "resourceType": "button",
            "url": url
        }
        json_data = json.dumps(updata_data)
        response = self.session.post(permission_update_api, headers=json_header, data=json_data)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'权限名称或权限标识或Url已经存在', msg)
        self.assertFalse(success)
        self.assertIsNone(result)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")


if __name__ == '__main__':
    unittest.main()