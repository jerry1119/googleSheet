# with open('qwe.txt', 'r') as f:
#     for line in f.readlines():
#         print(line.strip())
# # 要读取二进制文件，比如图片，视频，用'rb'打开
# f = open('test.jpg', 'rb')
# f.read()
#
# # 要读取非UTF-8编码的文本文件，需要给open（）函数传入encoding参数，例如，读取GBK编码的文件
# f = open('gbk.txt', 'r', encoding='gbk')
# f.read()
#
# # 若文件中有UnicodeDecodeError，可直接忽略掉:error='ignore'
# # 类似的，写文件：'w', 'wb'
# f = open('qwe.txt', 'w')
# f.write('Hello,World')
# f.close()
#
# import os
# # 查看操作系统类型，windows为nt
# print(os.name)
# # 查看环境变量
# print(os.environ.get('PATH'))
# # 查看当前目录下绝对路径
# print(os.path.abspath('.'))
# # 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来
# os.path.join('C:\\Users\\shopfloornb4.F2-QCMC\\PycharmProjects\\11.1', 'testdir')
# # 然后创建一个目录，实际我试的时候，直接创建也行
# os.mkdir('C:\\Users\\shopfloornb4.F2-QCMC\\PycharmProjects\\11.1\\testdir')
# # 删掉一个目录
# os.rmdir('C:\\Users\\shopfloornb4.F2-QCMC\\PycharmProjects\\11.1\\testdir')
# # 拆分一个路径：把路径拆分为两个部分，最后一个部分总是最后级别的目录或文件名
# os.path.split('C:\\Users\\shopfloornb4.F2-QCMC\\PycharmProjects\\11.1\\testdir')
# # 将文件扩展名拆分出来
# os.path.splitext('/path/to/file.txt')
# # 对文件重命名：
# os.rename('test.txt', 'test.py')
# # 删除文件：
# os.remove('test.py')
# # shutil模块提供了很多函数，可以当做是os模块的补充,比如copyfile()函数
# # 列出当前目录下的所有目录：
# s = [x for x in os.listdir('.') if os.path.isdir(x)]
# print(s)
# # 列出所有的py文件：
# d = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
# print(d)

# 当前目录以及当前目录下查找文件名包含指定字符串的文件
from datetime import datetime
import os

pwd = os.path.abspath('.')

print('  Size   Last Modified Name')
print('-----------------------------------------------')

for f in os.listdir(pwd):
    fsize = os.path.getsize(f)
    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M')
    flag = '/' if os.path.isdir(f) else ''
    print('%10d %s %s%s' % (fsize, mtime, f, flag))

