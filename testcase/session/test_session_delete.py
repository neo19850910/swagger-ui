#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *

class SessionDelete(unittest.TestCase):
    '''踢出用户'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_sessions_delete1(self):
        '''踢出用户:admin踢出其他用户'''
        response_else = get_session(data=data_no_permission)
        session_id = response_else.cookies.values()[0]
        response = self.session.post(delete_api, data={'sessionId': session_id})
        msg =  response.json()['msg']
        success = response.json()['success']
        response_else.cookies.clear_session_cookies()
        assert msg == u'操作成功'
        assert success is True
        assert response.status_code==200

    def test_sessions_delete2(self):
        '''踢出用户:踢出自己'''
        response = self.session.post(delete_api, data={'sessionId': self.session.cookies.values()[0]})
        msg = response.json()['msg']
        success = response.json()['success']
        assert msg == u'不能剔除自己'
        assert success is False
        assert response.status_code == 200

    def test_session_delete3(self):
        '''踢出用户:不输入session_id'''
        response = self.session.post(delete_api, data={'sessionId': None})
        msg = response.json()['msg']
        success = response.json()['success']
        self.assertIn('There is no session with id',msg)
        assert success is False
        assert response.status_code == 200

    def test_session_delete4(self):
        '''踢出用户:输入不存在的session_id'''
        response = self.session.post(delete_api, data={'sessionId':'121212'})
        msg = response.json()['msg']
        success = response.json()['success']
        assert 'There is no session with id' in msg
        assert success is False
        assert response.status_code == 200

    def test_session_delete5(self):
        '''踢出用户:权限不足'''
        resq = get_session(data=data_no_permission)
        response = resq.post(delete_api, headers=headers,data={'sessionId':resq.cookies.values()[0]})
        msg = response.json()['msg']
        success = response.json()['success']
        response.cookies.clear_session_cookies()
        assert msg == u'没有权限'
        assert success is False
        assert response.status_code == 401

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")
if __name__ == "__main__":
    unittest.main()
