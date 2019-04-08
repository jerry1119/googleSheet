# 1.--------------------------------
# Dict1 = {"xiaoming": 20, "xiaozhang": 15}
# Dict1["xiaodong"] = 18
# del Dict1["xiaozhang"]
# print(Dict1)

# 2.------------------------------------
# 有4种参数，必须参数、关键字参数、默认参数、不定长参数

# 3.-------下面函数有多少个参数-----------------
# def add((x,y),(a,b)):
#     return x*y - a*b
# 两个
# 4.编写一个函数计算x的y次幂
def cal(x, y):
    return x**y
print(cal(3, 5))
def cal1(a, b):
    num = 0
    count = 1
    while num < b:
        count = count*a
        num += 1
    return count
print(cal1(3,5))
# 5.指出哪个是行参，哪个是实参？将实参转换为关键字参数!
def func(x):
    return x**3
y = 3
print(func(y))
# 行参为 x ,实参为 y，
def func(x=3):
    return x**3
print(func())
# 6.一个函数可以有多个返回值么？返回值类型有多少种：
# 可以
# 有bool, str, int, float, tuple, list, .....
# 7. 递归函数必须满足的基本条件是什么？
# 有一个可迭代对象，
#
# 8.汉诺塔游戏
# def hanluota(x, A, B, C):
#     if x == 1:
#         print(A+"----->"+C)
#     else:
#         hanluota(x-1, A, C, B)
#         hanluota(1, A, B, C)
#         hanluota(x-1, B, A, C)
# hanluota(3, 'a', 'b', 'c')
# import Tkinter




