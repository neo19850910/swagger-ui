#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
from command.con_mysql import query
import time

class DictDelete(unittest.TestCase):
    '''删除字典'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.name = str(time.time())
        self.datas = {
            "description": '13',
            "name": self.name,
            "parentId": 0,
            "value": 1,
        }

    def test_dict_delete17(self):
        '''删除字典:正常删除'''
        data1 = json.dumps(self.datas)
        self.session.post(dict_add_api,headers=json_header,data=data1)
        sql1 = '''
              select id from dict where name =%s  
                '''
        result1 = [query(sql1, self.name)[0]]
        sql2 = '''
                     select is_delete from dict where name =%s  
                       '''
        result2 = query(sql2, self.name)[0]

        data2 = json.dumps(result1)
        del_response = self.session.post(dict_delete_api,headers=json_header,data=data2)
        del_data = del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        result3 = query(sql2, self.name)[0]
        assert result2 == 0
        assert result3 == 1
        assert msg==u'操作成功'
        assert success is True
        assert result is None
        assert del_response.status_code == 200

    def test_dict_delete18(self):
        '''删除字典:删除不存在的字典'''
        string = [99999]
        data = json.dumps(string)
        del_response = self.session.post(dict_delete_api, headers=json_header, data=data)
        del_data = del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        assert msg == u'操作成功'
        assert success is True
        assert result is None

    def test_dict_delete19(self):
        '''删除字典:无权限用户删除字典'''
        response = get_session(data=data_no_permission)
        sql = '''
            select id from dict;
                '''
        result = [query(sql)[0]]
        datas = json.dumps(result)
        del_response = response.post(dict_delete_api,headers=json_header, data=datas)
        del_data= del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        assert msg == u'没有权限'
        assert success is False
        assert result is None
        assert del_response.status_code == 401

    def test_dict_delete20(self):
        '''删除字典:传入数据非数组'''
        string = '1'
        response = self.session.post(dict_delete_api, headers=json_header,data=string)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        self.assertEqual(u'传入数据有误', msg)
        assert success is False
        assert result is None
        assert response.status_code == 200

    def test_dict_delete21(self):
        '''删除字典:未登录删除字典'''
        string = 1
        data = json.dumps([string])
        response = requests.post(dict_delete_api, headers=json_header, data=data)
        del_data = response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        self.assertEqual(msg,u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(response.status_code,401)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual(self.verificationErrors, [], 'test has bug!')

if __name__ == '__main__':
    unittest.main()