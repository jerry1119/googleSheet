# L1 = ['Hello', 'World', 'Apple', 14, None]
# L2 = [d.lower() for d in L1 if isinstance(d, str)]
# print(L2)
# 用generator输出杨辉三角
# def triangles():
#     L = [1]
#     while 1:
#         yield L
#         L = [1]+[L[i] + L[i + 1] for i in range(len(L)-1)] + [1]
#
# n = 0
# for t in triangles():
#     print(t)
#     n = n+1
#     if n == 10:
#         break

# 可直接用于for循环的对象，称为可迭代对象：Iterable
# # 可使用过isinstance() 判断对象是否为Iterable对象
#
# from collections import Iterable
# print(isinstance([], Iterable))
# print(isinstance({}, Iterable))
# print(isinstance('asdd', Iterable))
# print(isinstance(100, Iterable))
#
# # 可以被函数调用并不断返回下一个值的对象称为迭代器：Iterator
# from collections import Iterator
# print(isinstance((x for x in range(10)), Iterator))
# print(isinstance([], Iterator))
# print(isinstance({}, Iterator))
# print(isinstance('abc', Iterator))
#
# # 把list,dict,str等Iterable变成Iterator可以使用iter()函数：
# print(isinstance(iter([]), Iterator))
# print(isinstance(iter('abc'), Iterator))
# # 凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
# # Python 的 for 循环本质上就是通过不断调用next()函数实现的

# --------------------函数式编程--------------------------
# x = abs(-10)
# print(x)
#
# # 变量可以指向函数，可以通过调用该变量来调用函数
# f = abs
# print(f(-10))
# # 函数名也是变量
# abs  = 10
# # abs(-10)  # 把abs指向10以后这里调用就会出错
#
# # 将函数作为参数传给另一个函数，即高阶函数
# def add(x, y, f):
#     return f(x) + f(y)
# print( add(-5, -9, f))

