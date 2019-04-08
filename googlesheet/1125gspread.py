import pygsheets

gc = pygsheets.authorize(no_cache=True)
sh = gc.open_by_key('1e_XV8e2_9Z8cxsidE9ukUUxW693BKZYmo0-EkYKe1M8')
wks = sh.sheet1
print('ss')
# 在末尾插入数据
# num = 0
# for row in wks:
#     num += 1
# wks.insert_rows(row=num, values=['sas', 'fewfe', 'hello'])
# print(wks[10][5])   #打印出第10行第5列的值
# wks.append_table(values=[1, 2, 3, 4])   #直接在末尾插入一坨数据
# 导出CSV文件
# wks.export(pygsheets.ExportType.CSV)  #这个是导出到根目录
# 查找某个字符
# cell_list = wks.find("fail")
# working with named ranges   报错，懒得看了
# wks.create_named_range('A1', 'A10', 'prices')
# wks.get_named_range('prices')
# wks.get_named_ranges()  # will return a list of DataRange objects
# wks.delete_named_range('prices')
