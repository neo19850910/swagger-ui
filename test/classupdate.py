#coding:utf8

class a:
    i = 10
    def func1(self):
        i=5
        print i
    def func2(self):
        print i

m = a()
m.func1()
m.func2()