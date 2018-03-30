#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
import time

class DictAdd(unittest.TestCase):
    '''添加字典'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []
        self.name = str(time.time())

    def test_dict_add11(self):
        '''添加字典:正常添加'''
        datas = {
            "description": '12',
            "name": self.name,
            "parentId": 0,
            "value": 1,
                 }
        req_data = json.dumps(datas)
        response = self.session.post(dict_add_api,data=req_data,headers=json_header)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        assert success is True
        assert result is None
        assert msg == u'操作成功'
        assert response.status_code == 200

    def test_dict_add12(self):
        '''添加字典:父类字典不存在'''
        datas = {"description": '12',
                 "name": self.name,
                 "parentId": 99999,
                 "value": 1, }
        req_data = json.dumps(datas)
        response = self.session.post(dict_add_api, data=req_data, headers=json_header)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        assert success is False
        assert result is None
        assert msg == u'父类字典不存在'
        assert response.status_code == 200

    def test_dict_add13(self):
        '''添加字典:不是顶级字典'''
        datas = {"description": '12',
                 "name": self.name,
                 "parentId":8,
                 "value": 1, }
        req_data = json.dumps(datas)
        response = self.session.post(dict_add_api, data=req_data, headers=json_header)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        assert success is True
        assert result is None
        assert msg == u'操作成功'
        assert response.status_code == 200

    def test_dict_add14(self):
        '''添加字典:父类字典下的字典名称唯一'''
        name = str(time.time())
        data = {
                "description": '12',
                 "name": name,
                 "parentId":0,
                 "value": 1,
                }
        req_data = json.dumps(data)
        response1 = self.session.post(dict_add_api, data=req_data, headers=json_header)
        response2 = self.session.post(dict_add_api, data=req_data, headers=json_header)
        data2 = response2.json()
        msg = data2['msg']
        success = data2['success']
        result = data2['result']
        assert success is False
        assert result is None
        assert msg == u'字典名称已经存在'
        assert response2.status_code == 200

    def test_dict_add15(self):
        '''添加字典:未登陆添加字典'''
        data = {
            "description": '12',
            "name": self.name,
            "parentId": 0,
            "value": 1,
        }
        req_data = json.dumps(data)
        response = requests.post(dict_add_api,data=req_data, headers=json_header)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        assert success is False
        assert result is None
        assert msg == u'没有登录'
        assert response.status_code == 401

    def test_dict_add16(self):
        '''添加字典:无权限用户添加字典'''
        data = {
            "description": '12',
            "name": self.name,
            "parentId": 0,
            "value": 1,
        }
        req_data = json.dumps(data)
        self.session = get_session(data=data_no_permission)
        response = self.session.post(dict_add_api,data=req_data, headers=json_header)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        assert success is False
        assert result is None
        assert msg == u'没有权限'
        assert response.status_code == 401

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual(self.verificationErrors, [], 'test has bug!')

if __name__ == "__main__":
    unittest.main()