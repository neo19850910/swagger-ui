#-*- coding:utf8 -*-
#__author__ = "neo"

import xlrd,os

class OperationExcel:
    file_name = os.path.split(os.path.dirname(__file__))[0] + '\\swagger_test.xlsx'
    def __init__(self,sheet_name=None):
        self.sheet_name = sheet_name
        self.data = self.get_data()

    # 获取sheets的内容
    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheet_by_name(self.sheet_name)
        return tables

    # 获取单元格的行数
    def get_lines(self):
        tables = self.data
        return tables.nrows

    # 获取某一个单元格的内容
    def get_value(self, row, col):
        return self.data.cell_value(row, col)
