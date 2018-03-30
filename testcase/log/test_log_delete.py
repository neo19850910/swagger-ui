#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *
import json
from command.con_mysql import query

class LogDelete(unittest.TestCase):
    '''删除系统日志'''
    def setUp(self):
        self.session = get_session()
        self.verificationErrors = []

    def test_log_delete35(self):
        '''删除系统日志:正常删除日志'''
        sql1 = '''
                      select id,is_delete from log where is_delete!=1 order by id limit 1;
                        '''
        sql_res1 = query(sql1)[0]
        result1 = [sql_res1]
        is_delete = query(sql1)[1]
        data = json.dumps(result1)
        del_response = self.session.post(log_delete_api, headers=json_header, data=data)
        del_data = del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        sql2 = '''
                    select is_delete from log where id = %s
        '''
        sql_res2 = query(sql2, sql_res1)[0]
        self.assertEqual(msg, u'操作成功')
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(del_response.status_code, 200)
        self.assertEqual(0, int(is_delete))
        self.assertEqual(1, sql_res2)

    def test_log_delete36(self):
        '''删除系统日志:未登录删除日志'''
        sql1 = '''
                              select id,is_delete from log where is_delete!=1 order by id limit 1;
                                '''
        sql_res1 = query(sql1)[0]
        result1 = [sql_res1]
        is_delete = query(sql1)[1]
        data = json.dumps(result1)
        del_response = requests.post(log_delete_api, headers=json_header, data=data)
        del_data = del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        sql2 = '''
                           select is_delete from log where id = %s
               '''
        sql_res2 = query(sql2, sql_res1)[0]
        self.assertEqual(msg, u'没有登录')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(del_response.status_code, 401)
        self.assertEqual(0, sql_res2)

    def test_log_delete37(self):
        '''删除系统日志:无权限删除日志'''
        response = get_session(data=data_no_permission)
        sql1 = '''
                                      select id,is_delete from log where is_delete!=1 order by id limit 1;
                                        '''
        sql_res1 = query(sql1)[0]
        result1 = [sql_res1]
        is_delete = query(sql1)[1]
        data = json.dumps(result1)
        del_response = response.post(log_delete_api, headers=json_header, data=data)
        del_data = del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        sql2 = '''
                                   select is_delete from log where id = %s
                       '''
        sql_res2 = query(sql2, sql_res1)[0]
        self.assertEqual(msg, u'没有权限')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(del_response.status_code, 401)
        self.assertEqual(0, sql_res2)

    def test_log_delete38(self):
        '''删除系统日志:传入数据有误删除日志'''
        string = 'test_delete_log'
        data = json.dumps(string)
        del_response = self.session.post(log_delete_api, headers=json_header, data=data)
        del_data = del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        self.assertEqual(msg, u'传入数据有误')
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertEqual(del_response.status_code, 200)

    def test_log_delete39(self):
        '''删除系统日志:批量删除日志'''
        sql1 = '''
                                                        select id,is_delete from log where is_delete!=1 order by id limit 1;
                                                          '''
        sql2 = '''
                                                            select id,is_delete from log where is_delete!=1 order by id limit 1,2;
                                                              '''
        sql_res1 = query(sql1)[0]
        is_delete1 = query(sql1)[1]
        sql_res2 = query(sql2)[0]
        is_delete2 = query(sql2)[1]
        result = [sql_res1,sql_res2]
        data = json.dumps(result)
        del_response = self.session.post(log_delete_api, headers=json_header, data=data)
        del_data = del_response.json()
        msg = del_data['msg']
        success = del_data['success']
        result = del_data['result']
        sql12 = '''
                                           select is_delete from log where id = %s
                               '''
        sql_res12 = query(sql12, sql_res1)[0]
        sql22 = '''
                                                  select is_delete from log where id = %s
                                      '''
        sql_res22 = query(sql22, sql_res1)[0]
        self.assertEqual(msg, u'操作成功')
        self.assertTrue(success)
        self.assertIsNone(result)
        self.assertEqual(del_response.status_code, 200)
        self.assertEqual(1, sql_res12)
        self.assertEqual(1, sql_res22)
        self.assertEqual(0, is_delete1)
        self.assertEqual(0, is_delete2)

    def tearDown(self):
        self.session.cookies.clear_session_cookies()
        self.assertEqual([], self.verificationErrors, "test has bug!")

if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(LogDelete("test_log_delete39"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    unittest.main()