from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
import gspread
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

# drive = GoogleDrive(gauth)
gc = gspread.authorize(gauth)
print('test1')
sh = gc.open_by_key('1CtduA1iumQNH6ksFII0h3zNlQkqKI6cN5ykuj5dD30s')
print('test2')
sh.update_acell('A1', "what the fuck man")
print('what')
# sh = gc.open("SheetTest").sheet1
# sh.update_acell('B2', "test?")
# file1 = drive.CreateFile({'mimeType': 'text/csv'})
# # file1.SetContentString('Hello')
# file1.SetContentFile('files.csv')
#
# # file1.Upload()
#
# folder_name = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
# # # 创建文件夹
# folder_metadata = {
#     'title': folder_name,
#     'mimeType': 'application/vnd.google-apps.folder'
# }
# folder = drive.CreateFile(folder_metadata)
# folder.Upload()
# # 获取文件夹信息
# folder_title = folder['title']
# folder_id = folder['id']
# print('title:%s,id:%s' % (folder_title, folder_id))
# # 上传文件到文件夹
# f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}],
#                       'mimeType': 'text/csv'})
# f.SetContentFile('qwe.txt')
# f.Upload(param={'convert': True})
# # 列出文件
# file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
# for file2 in file_list:
#     print('title: %s, id: %s' % (file2['title'], file2['id']))
