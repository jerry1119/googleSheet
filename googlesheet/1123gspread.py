import pygsheets
from webcolors import name_to_rgb

gc = pygsheets.authorize(no_cache=True)

# Open spreadsheet and then workseet
sh = gc.open('A new spreadsheet')
wks = sh.sheet1

# Update a cell with value (just to let him know values is updated ;) )
# wks.update_cell('A1', "Hey yank this numpy array")

# update the sheet with array
# wks.update_cells('A2', my_nparray.to_list())

# share the sheet with your friend
# sh.share("myFriend@gmail.com")
header = wks.cell('A1')
header.set_text_alignment('RIGHT')
# header.set_text_format('foregroundColor', (0.4, 0.9, 0, 1.0))
header.value = 'Name'
header.set_text_format('fontSize', 15)
header.text_format['bold'] = False
# header.text_format['fontSize'] = 15
# header.text_format['foregroundColor'] = (0.4, 0.9, 0, 1.0)
header.color = (0.4, 0.9, 0, 1.0)
header.update()

# wks.cell('B1').set_text_format('bold', True).value = 'height'
# # 设置姓名
# wks.update_cells('A2:A6', [['何杰'], ['秦渝涛'], ['龚钟密'], ['方清旭'], ['徐兆宇']])
# # 设置体重
# wks.update_cells('B2:B6', [[62], [60], [46], [65], [60]])
# heights = wks.range('B2:B6', returnas='range')  # 拿到数据范围对象
# # 经过多次调试，发现，拿到范围时要原先范围有值才行，其次给范围命名时，如果原先
# # 存在这个名字会报错
# heights.name = 'heights7'  # 给这个范围命名
# # heights3.update_values([[50], [60], [66], [65], [60]])  # 更新数据
# wks.update_cell('A7', '平均值')
# wks.update_cell('B7', '=average(heights7)')  # 平均数
# print('yes')
