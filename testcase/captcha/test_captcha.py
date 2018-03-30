#-*- coding:utf8 -*-
#__author__ = "neo"

from testcase import *

class Captcha(unittest.TestCase):
    '''获取验证码'''
    def setUp(self):
        self.verificationErrors = []

    def test_Captcha10(self):
        '''获取验证码:能正常请求'''
        self.response = requests.get(captcha_api)
        code = self.response.status_code
        assert code == 200

    def tearDown(self):
        self.assertEqual([], self.verificationErrors, "test has bug!")
if __name__ == '__main__':
    unittest.main()