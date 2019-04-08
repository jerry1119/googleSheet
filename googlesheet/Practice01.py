# print("Hello world")
# age = 20
# if age >= 6:
#     print("teenager")
# elif age >= 18:
#     print("adult")
# else:
#     print('kid')
# age = 20
# if age:
#     print('true')
# names = ['Micheal' ,'Bob','Tracy']
# for name in names:
#     print(name)
# sum = 0
# for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
#     sum = sum + x
# print(sum)
# sum = 0
# for x in range(100):  #这里range生成的是0-99整数序列
#     sum = sum + x
# print(sum)
#计算100以内所有奇数的和
# sum = 0
# n = 99
# while n > 0:
#     sum = sum + n
#     n = n - 2
# print(sum)
# from Tools.scripts.treesync import raw_input
#
# birth = raw_input('birth:')
# if  int(birth) < 2000:
#     print('001')
# else:
#     print('002')
# s = abs(-20)
# print(s)

# list = ['hejie','sss','we','snake']
# for name in list:
#     if name =='we':
#         break
#     print('Hello,'+name+'!')
# print(int(12.222))
# print(str(100))
# print(bool(1))
# print(bool(''))

# def my_abs(x):  #定义函数my_abs,python中定义函数需要使用def语句
#     if x>0:
#         return x
#     else:
#         return -x
# print(my_abs(-9))

#如果想定义一个 什么事也不做的空函数，可以用pass语句，pass起站位的作用
# def nop():
#     pass

# def my_abs(x):
#     # 让我们修改一下my_abs的定义，对参数类型做检查，只允许整数和浮点数类型的参数。数据类型检查可以用内置函数isinstance()
#     # 实现：
#     if not isinstance(x,(int,float)):
#         raise TypeError('bad operand type')
#     if x>= 0:
#         return x
#     else:
#         return -x
# print(my_abs('sss'))

# import math
#
# def move(x,y,step,angle = 0):
#     nx = x + step * math.cos(angle)
#     ny = y + step * math.sin(angle)
#     return nx,ny
# x,y =  move(100,90,20,math.pi/6)
# print(x,y)
# r = move(90,50,30,math.pi/6)
# print(r) #返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值，所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便

#求 ax*x  + bx + c = 0
# import math
# def quadratic(a,b,c):
#     if a == 0:
#         return -b/c
#     gen = b * b - 4*a*c
#     if gen < 0:
#         return '无解'
#     else:
#         x1 = (math.sqrt(gen) - b)/(2*a)
#         x2 = (-math.sqrt(gen) - b)/(2*a)
#         return x1, x2
# print(quadratic(1,4,4))

# def power(x,n=2):#默认参数n = 2 ，如果不传入n ，则不会报错，当成2
#     #注意：需要将必选参数在前，默认参数在后，
#     # 当函数有多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数。
#     # 使用默认参数有什么好处？最大的好处是能降低调用函数的难度。
# 也可以不按顺序提供部分默认参数。当不按顺序提供部分默认参数时，需要把参数名写上
#     s = 1
#     while n > 0:
#         n = n - 1
#         s = s * x
#     return s
# print(power(5))
# print(345592425)
# 去重複，并排序
# a = [4,7,3,4,1,9,8,3,7]
# b = sorted(set(a))
# print(b)

#默认参数必须指向不变对象
# 为什么要设计str、None这样的不变对象呢？因为不变对象一旦创建，对象内部的数据就不能修改，这样就减少了由于修改数据导致的错误。
# 此外，由于对象不变，多任务环境下同时读取对象不需要加锁，同时读一点问题都没有。我们在编写程序时，如果可以设计一个不变对象，那就尽量设计成不变对象
# def add_end(L=None):
#     if L is None:
#         L = []
#     L.append('END')
#     return L
# print(add_end())
# print(add_end())

# 可变参数，在参数前加一个*
# numbers接收到的是一个tuple，因此，调用该函数时可以传入任意个参数，包括0个
# def calc(*numbers):
#     sum = 0
#     for n in numbers:
#         sum = sum + n*n
#     return sum
# print(calc(1,2))
# print(calc())
# # 如果已经有一个list或者tuple，要调用一个可变参数可以：
# nums = [1,2,3,4]
# calc(nums[0],nums[1],nums[2],nums[3])   #这样也繁琐
# # 可以在list或tuple前加一个*号，把list或tuple的元素变成可变参数传进去
# print( calc(*nums))

# 关键字参数
# 可变参数允许传入0个或任意个参数，这些可变参数在函数调用时自动组装成一个tuple。
# 而关键字参数允许传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为
# 一个dict
# def person(name,age,**kw):
#     print('name:',name,'age:',age,'other:',kw)
# print(person('Michael',30)) #可以只传入必选参数
# # 也可以传入任意个数的关键字参数：
# print(person('Bob',35,city='Beijing',job='Engineer'))
# # 和可变参数类似，也可先组装出一个dict，然后把dict传进去
# extra = {'city':'beijing','job':'engineer'}
# print(person('jack:', 24, city=extra['city'],job=extra['job']))
# # 简化的写法
# print(person('Jack', 25, **extra))

# def f1(a, b, c=0, *args, **kw):
#     print('a =', a, 'b=', b, 'c=', c, 'args=', args, 'kw=', kw)
#
# def f2(a, b, c=0, *, d, **kw):
#     print('a =', a, 'b=', b, 'c=', c, 'd=', d, 'kw=', kw)

#递归函数
# def func(n):
#     if n==1:
#         return 1
#     return n*func(n-1)
# print(func(5))
# print(func(1000))#python标准的解释器没有针对尾递归做优化，任何函数都存在栈溢出的问题

# 练习汉诺塔的移动：
#可以抽象为3步，上面一坨移到中间，底部移到右边，中间移到右边
# def move(n, a, b, c):
#     if n==1:
#         print('Move',a,'-->',c)
#     else:
#         move(n-1,a,c,b)
#         move(1,a,b,c)
#         move(n-1,b,a,c)
# move(2,'A','B','C')
from _ast import Slice

#切片,python中没有substring，切片方便很多
# L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
# print(L[1:3])   #左闭右开，从索引1取到3
# print(L[-3:-1])  #取倒数3到1

# L = list(range(100))
# print(L[:10:2])  #前十个数，每两个取一个
# print(L[::5])   #所有数，每5个取一个
#tuple也是一种list，只是tuple不可变，所以tuple也可切片，结果仍是tuple
#字符串‘xxxxxxx’ 也可看成是一种list
print("ASDADDADD"[:4])
print('dfsfsdef'[::3])