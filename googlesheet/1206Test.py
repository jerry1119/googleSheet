# import re
# patt = r'\w+\-\w+\-\w+\-\d+'
# path = r'\\10.18.6.47\sel_monitor\Joplin_Test_Logs\Joplin_Process_log\Joplin-fail-log\SUB_LED\J-029-LED-03_WIP7B29L77MGW_2017_12_01_11_06_28_1.csv'
# m = re.search(patt, path)
# if m is not None:
#     print(m.group())
# else:
#     print('ss')
# import csv
# path = r""
# RFlog = csv.reader(open(r'C:\Users\1\Desktop\CMW100_RF_OTA.csv', 'r'))
# RFlog = list(RFlog)
# # print(RFlog)
# print(RFlog[2])
# print(RFlog[2][1])
# print(len(str("")))

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

lena = mpimg.imread(r'C:\Users\1\Desktop\相机二维码\2018-01-17-09-58-22-65.jpg')
# lena.shape
# plt.imshow(lena)
# plt.axis('off')
# plt.show()
print(lena)
