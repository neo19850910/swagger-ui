#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
from command.con_mysql import query

class DictUpdate(unittest.TestCase):
    '''修改字典'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_dict_update27(self):
        '''修改字典:正常修改'''
        sql = '''
            select id from dict limit 1;
        '''
        sql_data = query(sql)[0]
        data = {
                  "description": "string",
                  "id": sql_data,
                  "name": "1",
                  "value": 0
                 }
        json_data = json.dumps(data)
        response = self.session.post(dict_update_api,headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'操作成功')
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_dict_update28(self):
        '''修改字典:修改不存在的字典'''
        sql = '''
                    select max(id) from dict ;
                '''
        sql_data = query(sql)[0] + 1
        data = {
            "description": "string",
            "id": sql_data,
            "name": "1",
            "value": 0
        }
        json_data = json.dumps(data)
        response = self.session.post(dict_update_api, headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'修改字典信息失败')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_dict_update29(self):
        '''修改字典:无权限用户修改字典'''
        sql = '''
                    select id from dict limit 1;
                '''
        sql_data = query(sql)[0]
        data = {
            "description": "string",
            "id": sql_data,
            "name": "1",
            "value": 0
        }
        json_data = json.dumps(data)
        login_session = get_session(data=data_no_permission)
        response = login_session.post(dict_update_api, headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'没有权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_dict_update30(self):
        '''修改字典:未登陆修改字典'''
        sql = '''
                            select id from dict limit 1;
                        '''
        sql_data = query(sql)[0]
        data = {
            "description": "string",
            "id": sql_data,
            "name": "1",
            "value": 0
        }
        json_data = json.dumps(data)
        response = requests.post(dict_update_api, headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 401)

    def test_dict_update31(self):
        '''修改字典:修改值为非整形数据类型'''
        sql = '''
                    select id from dict limit 1;
                '''
        sql_data = query(sql)[0]
        data = {
            "description": "string",
            "id": sql_data,
            "name": "1",
            "value": 'test_update_value'
        }
        json_data = json.dumps(data)
        response = self.session.post(dict_update_api, headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'传入数据有误')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_dict_update32(self):
        '''修改字典:修改name超过50个字节'''
        sql = '''
                            select id from dict limit 1;
                        '''
        sql_data = query(sql)[0]
        name = '1'*51
        data = {
            "description": "string",
            "id": sql_data,
            "name": name,
            "value": 1
        }
        json_data = json.dumps(data)
        response = self.session.post(dict_update_api, headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'[name长度需要在1和50之间]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_dict_update33(self):
        '''修改字典:修改name为空'''
        sql = '''
                            select id from dict limit 1;
                        '''
        sql_data = query(sql)[0]
        name = None
        data = {
            "description": None,
            "id": sql_data,
            "name": name,
            "value": 1
        }
        json_data = json.dumps(data)
        response = self.session.post(dict_update_api, headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'[name不能为空]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def test_dict_update34(self):
        '''修改字典:修改value为空'''
        sql = '''
                            select id,name from dict order by id limit 1;
                        '''
        sql_id = query(sql)[0]
        sql_name = str(query(sql)[1])
        data = {
            "description": None,
            "id": sql_id,
            "name": sql_name,
            "value": None
        }
        json_data = json.dumps(data)
        response = self.session.post(dict_update_api, headers=json_header, data=json_data)
        res_data = response.json()
        msg = res_data['msg']
        success = res_data['success']
        result = res_data['result']
        self.assertEqual(msg, u'[value不能为null]')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual(self.verificationErrors, [], 'test has bug!')

if __name__ == '__main__':
    unittest.main()