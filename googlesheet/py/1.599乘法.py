# for i in range(1, 10):
#     for j in range(1, i+1):
#         print(str(i)+"*"+str(j), end=" ")
#     print(" ")

# a = 3, b = 4
# a = 3
# b = 4
# a = a+b
# b = a-b
# a = a-b
# print(a, b)
# n = 1
#
# for x in range(9):
#     n = (n+1)*2
#     print(n)
# print((n/2)+1)

import random
a = random.randint(1, 10)
b = 1
c = int(input("猜10以内的数:"))
while 0 <= c < 10:
    if b<= 3:
        if c != a:
            b = b + 1
            print("猜错了")
            c = int(input("猜10以内的数:"))
        else:
            print("猜对了")
            break
    else:
        print("次数不够")
        break


