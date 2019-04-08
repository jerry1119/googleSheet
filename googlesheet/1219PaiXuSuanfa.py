L = [4, 45, 32, 56, 23, 234, 6, 3, 2, 90, 12, 3, 3, 5, 4]

# def maopao(list, times):
#
#     for x in range(times):
#         if L[x] > L[x + 1]:
#             a = L[x + 1]
#             L[x + 1] = L[x]
#             L[x] = a
#         else:
#             continue
#     if times > 0:
#         maopao(L, times - 1)
#
#
# maopao(L, len(L)-1)
# print(L)

# def xuanZhe(list, times):
#     min = list[0]
#     for x in range(times):
#         if list[x] < min:
#             min = list[x]
#         else:
#             continue
L = [12, 34, 5, 5, 6, 77, 834, 56, 67, 34, 45, 67, 90, 6]


print(["Double" if x % 3 == 0 | x % 5 == 0 else "True" if x % 3 == 0 else "False" if x % 5 == 0 else x for x in L])
for x in range(len(L)):
    if L[x] % 3 == 0:
        if L[x] % 5 == 0:
            L[x] = "Double"
        else:
            L[x] = "True"
    elif L[x] % 5 == 0:
        L[x] = "False"
print(L)
