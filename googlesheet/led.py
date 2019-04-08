import datetime
import os
import csv
from io import StringIO
from apscheduler.schedulers.blocking import BlockingScheduler
import pygsheets

class StringBuilder:
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def Append(self, str):
        self._file_str.write(str)

    def __str__(self):
        return self._file_str.getvalue()




def getFilePaths(path, ls):
    fileList = os.listdir(path)
    try:
        for temp in fileList:
            pathTemp = os.path.join(path, temp)
            if True == os.path.isdir(pathTemp):
                getFilePaths(pathTemp, ls)
            elif pathTemp[pathTemp.rfind('.') + 1:].upper() == 'CSV':
                ls.append(pathTemp)
    except PermissionError:
        pass


def getValues(path):
    sb = StringBuilder()
    sb1 = StringBuilder()
    fixture = ""
    csv_reader = csv.reader(open(path, 'r'))
    for line in csv_reader:
        if line[0].__contains__("Fixture"):
            fixture = line[0].split('=')[1]
        if len(line) > 4 and line[2].upper() == "FAIL":
            sb.Append(str(line[1]) + '\n')
            sb1.Append(str(line[1]) + " " + str(line[3]) + "\n")
    # return "\"" + str(sb) + "\"" + "," + "\"" + str(sb1) + "\"" + "\n"
    return str(sb)[:-1], str(sb1)[:-1], fixture
def main():
    ls = []
    gc = pygsheets.authorize(no_cache=True)
    sh = gc.open_by_key('1jMkDQmWP8gTSp-ghpRaQvveBVCJGvsG0GnOUPbLlkc8')
    wks = sh.sheet1
    num = 0
    for row in wks:
        num += 1
        # print(row)
    # time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    Date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = "20171124153409"  # 测试使用
    # fo2 = open(time + "_test.csv", 'w')
    path = r"D:\asd"  # 测试使用
    # path = r"\\10.18.6.47\sel_monitor\Joplin_Test_Logs\Joplin-fail-log\SUB_TOUCH"
    getFilePaths(path, ls)
    a = []
    SNname = []
    ThisDay = []
    # num1 = 0
    for thisDay in ls:
        thisTime = thisDay[thisDay.find("201"):thisDay.find(".")]
        if int(time[:8] + "080000") <= int(thisTime) < int(time[:8] + "143000"):
            ThisDay.append(thisDay)
    for name in ThisDay:
        SNname.append(name[name.find("WIP"):name.find("-")])
    SNnameSet = set(SNname)
    for item in SNnameSet:
        for filePath in ThisDay:
            if filePath.__contains__(item):
                testState = ""
                reTest = 0
                NTF = 0
                Repair = 0
                fileName = os.path.splitext(os.path.basename(filePath))[0]
                SN = fileName[:13]
                testTime = fileName.split('-')[1]

                if int(SNname.count(item)) == 1:
                    testState = "Retest pass"
                    reTest = 1
                elif int(SNname.count(item)) == 2:
                    testState = "NTF"
                    NTF = 1
                else:
                    testState = ""
                    Repair = 1
                # fo2.write(SN + "," + testTime + "," + getValues(filePath))
                # info = SN + "," + testTime + "," + getValues(filePath)
                returnList = getValues(filePath)
                info = [Date, testState, Date, "D", returnList[2].split('-')[1], returnList[2], SN, returnList[0],
                        returnList[1], reTest, NTF, Repair]
                a.append(info)
                # wks.insert_rows(row=num, values=info)
                # num1 += 1
                break
            else:
                continue
    # wks.insert_rows(row=num, number=num1, values=a)
    # 这里的number = 即插入多少行，这个参数可以不写，但row = 这个参数，即从多少行开始，这个参数必须写
    wks.insert_rows(row=num, values=a)
    # fo2.close()

# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(main, 'cron', hour=8, minute=15)
scheduler.add_job(main, 'cron', hour=14, minute=45)
scheduler.add_job(main, 'cron', hour=9, minute=14)
# scheduler.add_job(main, 'interval', seconds=10)
scheduler.start()
