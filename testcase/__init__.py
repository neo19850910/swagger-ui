#-*- coding:utf8 -*-

import unittest
from login import get_session
import requests
from config.config import getConfig
from command.optionexcel import OperationExcel

headers = eval(getConfig('header', 'headers'))
json_header = eval(getConfig('header','json_header'))
data_no_permission = {'username':'huhuan','password':'123456','rememberMe':False}   #无权限用户
login_admin = {'username':'admin','password':'123456','rememberMe':False}   #超级管理员
dict_add_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'字典管理').get_value(4,1) #添加字典
session_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'会话管理').get_value(12,1) #查询在线用户列表
delete_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'会话管理').get_value(4,1) #踢出用户
dict_delete_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'字典管理').get_value(13,1) #删除字典
captcha_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'其他组件').get_value(4,1) #获取验证码
dicts_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'字典管理').get_value(22,1) #检索字典
dict_update_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'字典管理').get_value(30,1) #修改字典
log_delete_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'日志管理').get_value(4,1) #删除系统日志
log_page_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'日志管理').get_value(12,1) #分页检索系统日志列表
permission_add_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'权限管理').get_value(4,1) #添加权限
permission_delete_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'权限管理').get_value(18,1) #删除权限
permission_list_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'权限管理').get_value(26,1) #获得所有权限（数组形式）
permission_menu_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'权限管理').get_value(32,1) #查询用户的所有权限的菜单权限
permission_tree_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'权限管理').get_value(38,1) #获得所有权限（树状形式）
permission_update_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'权限管理').get_value(44,1) #更新权限
user_login_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户个人管理').get_value(4,1) #用户登录
user_register_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户个人管理').get_value(14,1) #用户注册
user_info_update_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户个人管理').get_value(34,1) #更新个人信息
user_logout_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户个人管理').get_value(46,1) #用户退出
user_password_update_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户个人管理').get_value(51,1) #修改密码
user_info_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户个人管理').get_value(66,1) #获取个人信息
user_add_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户管理').get_value(4,1) #添加用户
user_delete_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户管理').get_value(32,1) #删除用户
user_page_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户管理').get_value(41,1) #分页查询用户
user_update_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'用户管理').get_value(50,1) #更新用户
role_add_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'角色管理').get_value(4,1) #添加角色信息
role_delete_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'角色管理').get_value(25,1) #删除角色信息
role_list_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'角色管理').get_value(34,1) #获得简单的角色信息(没有权限信息)
role_page_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'角色管理').get_value(40,1) #分页获得角色信息
role_update_api = getConfig('swagger','baseurl')+':'+getConfig('swagger','port') + OperationExcel(u'角色管理').get_value(51,1) #修改角色信息