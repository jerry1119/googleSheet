import datetime
import os
import csv
from io import StringIO
from apscheduler.schedulers.blocking import BlockingScheduler
import pygsheets
import re
from openpyxl import load_workbook
RFlog = []
Dict = {}
def main():
    # 打开rf模板
    global RFlog
    RFlog = csv.reader(open(r'C:\Users\1\Desktop\CMW100_RF_OTA.csv', 'r'))
    RFlog = list(RFlog)
    f_read = open(r'C:\Users\1\Desktop\格式.txt','r')
    for line in f_read:
        key = line.split('$')[1].replace('\t','').replace('\n','').strip()
        value = line.split('$')[0]
        if not key in Dict:
            Dict[key] = value
    # 打开excel
    print('start')

    FPYpath = r'\\10.18.6.47\acer_m\Hejie\NU9_FPY_20180507-D.xlsx'
    sh = load_workbook(FPYpath)
    wk_Touch = sh.get_sheet_by_name('Touch_issues')
    wk_FAT = sh.get_sheet_by_name('Sub-assy_issues')
    wk_Led = sh.get_sheet_by_name('LED-calibration_issue')
    wk_RF = sh.get_sheet_by_name('RF-OTA_issues')
    # 打开google
    googlePath = "1jMkDQmWP8gTSp-ghpRaQvveBVCJGvsG0GnOUPbLlkc8"
    gc = pygsheets.authorize(no_cache=True)
    sh = gc.open_by_key(googlePath)
    wks_Touch = sh.worksheet_by_title('SYS_TOUCH issue')
    wks_FAT = sh.worksheet_by_title('FAT issue')
    wks_Led = sh.worksheet_by_title('SYS_LED issue')
    wks_RF2 = sh.worksheet_by_title('RF2 issue')
    print("dakaigoogle")
    logPath_Touch = r"\\10.18.6.47\sel_monitor\Joplin_Test_Logs\Joplin-fail-log\SUB_TOUCH"
    logPath_FAT = r"\\10.18.6.47\sel_monitor\Joplin_Test_Logs\Joplin-fail-log\FAT"
    logPath_Led = r"\\10.18.6.47\sel_monitor\Joplin_Test_Logs\Joplin_Process_log\Joplin-fail-log\SUB_LED"
    logPath_RF2 = r"\\10.18.6.47\sel_monitor\Joplin_Test_Logs\Joplin-fail-log\RF2"
    ls_Touch = getListFiles(logPath_Touch)
    ls_FAT = getListFiles(logPath_FAT)
    ls_Led = getListFiles(logPath_Led)
    ls_RF2 = getListFiles(logPath_RF2)
    print("打开47")
    # 参数为 wk, ls,  reTest的位置 rIndex , sh的sheet  wks, 站别
    upload(wk_Touch, ls_Touch, 10, wks_Touch, "Touch")
    upload(wk_FAT, ls_FAT, 10, wks_FAT, "FAT")
    upload(wk_Led, ls_Led, 10, wks_Led, "Led")
    upload(wk_RF, ls_RF2, 9, wks_RF2, "RF")
def upload(wk, ls, rIndex, wks, station):
    failInfo = []  # failInfo存的是log抓出的Fail信息
    time = datetime.datetime.now().strftime("%H")
    # 判断白夜班
    if int(time) < 12:
        DorN = 'N'
        yesterday = datetime.datetime.today() + datetime.timedelta(-1)
        Date = yesterday.strftime("%m/%d")
    else:
        DorN = 'D'
        Date = datetime.datetime.today().strftime("%m/%d")
    for row in wk:
        if len(str(row[3].value)) < 6:
            continue
        for filePath in ls:
            if filePath.__contains__(row[3].value):
                testState = ""
                returnList = getValues(filePath)
                reTest = row[rIndex].value
                NTF = row[rIndex+1].value
                Repair = row[rIndex+2].value
                if reTest == '1':
                    Repair = 0
                    NTF = 0
                    testState = 'Retest pass'
                elif NTF == '1':
                    Repair = 0
                    reTest = 0
                    testState = 'NTF'
                elif Repair == '1':
                    reTest = 0
                    NTF = 0
                    testState = 'Repair pass'
                else:
                    reTest = 0
                    NTF = 0
                    Repair = 0
                    testState = ''
                if len(str(returnList[2])) < 6 :
                    fixtrue = returnList[2]
                    line = ""
                elif returnList[2].__contains__("-"):
                    fixtrue = returnList[2]
                    line = fixtrue.split('-')[1]
                else:
                    fixtrue = returnList[2]
                    line = fixtrue[2:5]
                if station == "RF":
                    info = [Date, testState,"", Date, DorN, line, fixtrue, "", row[3].value,
                            "", "",returnList[0],
                            returnList[1], reTest, NTF, Repair]
                else:
                    info = [Date, testState, "", Date, DorN, line, fixtrue, row[3].value,
                            returnList[0],
                            returnList[1], reTest, NTF, Repair]
                failInfo.append(info)
                break #取匹配到sn的第一个log的值
            else:
                continue
    print("failInfo的长度：")
    print(len(failInfo))


    num = 0
    for row in wks:
        num += 1
    wks.insert_rows(row=num, values=failInfo, inherit= True) #row 大于1088时，应该将继承inherit设为True
    print("上传完毕")

def getValues(path):
    sb = StringBuilder()
    sb1 = StringBuilder()
    fixture = ""
    if path.__contains__('LED'):
        patt = r'[A-Z]-\w+-\w+-\d+'
        m =re.search(patt , path)
        if m is not None:
            fixture = m.group()
    if path.__contains__('RF2'):
        fi = open(path, 'r')
        csv_reader = csv.reader(fi)
        csv_reader = list(csv_reader)
        fi.close()
        global RFlog
        if csv_reader[11].__contains__(RFlog[11][5]):
            for i, line in enumerate(csv_reader):
                if line[0].__contains__("Fixture"):
                    fixture = line[0].split('=')[1]
                if i > 35 and line.__contains__('Failed'):
                    failValue = line[5]
                    key = RFlog[i][8]
                    if key in Dict:
                        value = Dict[key]
                        sb.Append(value + "\n")
                        sb1.Append(value + "  " + failValue + "\n")
        else:
            sb.Append("error\n")
            sb1.Append("only test part of items\n")
        return str(sb)[:-1], str(sb1)[:-1], fixture
    else:
        fi = open(path, 'r')
        csv_reader = csv.reader(fi)
        for line in csv_reader:
            if line[0].__contains__("Fixture"):
                fixture = line[0].split('=')[1]
            if len(line) > 4 and line[2].upper() == "FAIL":
                sb.Append(str(line[1]) + '\n')
                sb1.Append(str(line[1]) + "   " + str(line[3]) + "\n")
            if len(line) > 4 and line[3].upper() == "FAIL":
                if str(line[0]) == 'Check Reset Function':
                    sb.Append(str(line[0]) + '\n')
                else:
                    sb.Append(str(line[0]) + '\n')
                    sb1.Append(str(line[0]) + "   " + str(line[5]) + "\n")
        # return "\"" + str(sb) + "\"" + "," + "\"" + str(sb1) + "\"" + "\n"
        fi.close()
        return str(sb)[:-1], str(sb1)[:-1], fixture

# def getFilePaths(path, ls):
#     fileList = os.listdir(path)
#     try:
#         for temp in fileList:
#             pathTemp = os.path.join(path, temp)
#             if os.path.isdir(pathTemp):
#                 getFilePaths(pathTemp, ls)
#             elif pathTemp[pathTemp.rfind('.') + 1:].upper() == 'CSV':
#                 ls.append(pathTemp)
#     except PermissionError:
#         pass
def getListFiles(path):
    ls = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ls.append(os.path.join(root,filespath))
    return ls
class StringBuilder:
    _file_str = None
    def __init__(self):
        self._file_str = StringIO()
    def Append(self, str):
        self._file_str.write(str)
    def __str__(self):
        return self._file_str.getvalue()

scheduler = BlockingScheduler()
# scheduler.add_job(main, 'cron', hour=8, minute=15)
# scheduler.add_job(main, 'cron', hour=14, minute=45)
# scheduler.add_job(main, 'cron', hour=14, minute=23)
# # scheduler.add_job(main, 'interval', seconds=20)
# scheduler.start()
main()
