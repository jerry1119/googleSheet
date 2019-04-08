# python的for循环抽象程度远高于java,C#，只要是可迭代对象，无论有无下标，都可以迭代
# d = {'a': 1, 'b': 2, 'c': 3}
# for key in d:
#     print(key)
# for value in d.values():
#     print(value)
# #Python内置的enumerate函数可以把一个list变成索引-元素对，这样就可以在for循环中同时迭代索引和元素本身：
# for i, value in enumerate(['A', 'B', 'C']):
#     print(i, value)
# 同时引用两个变量在python中也很常见
# for x, y in [(1, 2), (2, 4), (3, 9)]:
#     print(x, y)
# # 把要生成的元素放在前面，后面跟for循环，即列表生成式
# L = [x*x+x for x in range(1, 20) if x % 2 == 0]
# print(L)
# # 还可使用多层循环，生成全排列
# L = [m + n for m in 'ABC' for n in 'XYZ']
# print(L)
# # 列出当前目录下所有的文件和文件夹，这里用列表生成式非常简洁
# import os
# L = [d for d in os.listdir('.')]
# print(L)
# 列表生成式也可以用两个变量来生成list：
# d = {'x': 'A', 'y': 'B', 'z': 'C'}
# L = [k + '=' + v for k, v in d.items()]
# print(L)
# 将list中所有字符变成小写
# L = ['Hello', 'World', 'IBM', 'Apple']
# S = [s.lower() for s in L]
# print(S)
# 输出["hello", "world", "apple"]
# L = ['Hello', 'World', 18, "Apple", None]
# S = [s.lower() for s in L if isinstance(s, str)]
# print(S)

# -------------------------生成器--------------------
# 在python中，这种一边循环一边生成的机制，成为生成器：generator
# generator 与列表生成式的区别是最外层的()
# g = (x*x for x in range(10))
# print(next(g))
# print(next(g))  # 如果一个个打印出来，可通过next()函数获得generator的下一个返回值
# for n in g:   # 一般是用for循环迭代出来
#     print(n)

# 如果推算的算法比较复杂，用类似的列表生成式的for循环无法实现的时候，还可以使用函数来实现
# 比如著名的斐波拉契数列（Fibonacci）：1,1,2,3,5,8,13,21,34
# def fib(max):
#     n, a, b = 0, 0, 1
#     while n < max:
#         # print(b)
#         yield b  # 这里将print(b)改为了yield b,就把fib函数变成了generator
#         # 即，如果函数定义中包含yield关键字，那么这个函数就是generator
#         a, b = b, a + b
#         n = n + 1
#     return 'Done'
# for n in fib(6):
#     print(n)

number = 23
guess = int(input('Enter an integer:'))

if guess == number:
    print('Congratulations,you guessed it.')
    print('(but you do not win any prize!)')
elif guess < number:
    print('No,it is a little higher than that')
else:
    print('No,it is a little lower than that')
print('Done')

