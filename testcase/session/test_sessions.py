#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *

class Sessions(unittest.TestCase):
    '''查询在线用户列表'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_sessions6(self):
        '''查询在线用户列表:admin查询'''
        response = self.session.get(session_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        assert msg == u'操作成功'
        assert success is True
        assert result is not None

    def test_sessions7(self):
        '''查询在线用户列表:无权限角色查询'''
        resq = get_session(data=data_no_permission)
        response = resq.get(session_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        assert msg == u'没有权限'
        assert success is False
        assert result is  None
        assert response.status_code == 401

    def test_sessions8(self):
        '''查询在线用户列表:没有登录直接查询'''
        response = requests.get(session_api)
        data = response.json()
        msg = data['msg']
        success = data['success']
        result = data['result']
        response.cookies.clear_session_cookies()
        assert msg == u'没有登录'
        assert success is False
        assert result is None
        assert response.status_code == 401

    def test_session9(self):
        '''查询在线用户列表:同一个用户多地登录查询'''
        response = get_session(data=login_admin)
        data = response.get(session_api).json()
        result = data['result']
        response.cookies.clear_session_cookies()
        count = 0
        for (result_set) in result:
            if result_set['username'] == 'admin':
                count+=1
        self.assertEqual(1, count)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual(self.verificationErrors,[],'test has bug!')

if __name__ =='__main__':
    unittest.main()