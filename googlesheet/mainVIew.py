from Function import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import *
from PyQt5 import QtCore
import configparser
import os, csv, sys
import pyodbc
import time, datetime

allsn = None
station = None


class upDateSN(QtCore.QThread):
    # 声明一个信号，同时返回一个list
    _connectSignal = QtCore.pyqtSignal(list)

    # 构造函数里增加形参
    def __init__(self, t, parent=None):
        super(upDateSN, self).__init__(parent)
        # 储存参数
        self.t = t

    # 重写 run() 函数
    def run(self):
        while (True):
            # allsn = os.popen('adb devices').readlines()
            allsn = ['dwdwdwqd', 'ddfsdf', 'WIP1234567890', 'WIP1234234333', 'WIP324325245245']
            self._connectSignal.emit(allsn)
            self.sleep(1)


class view(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        # self.showFullScreen()
        self.showMaximized()
        movie = QMovie("image/auto.gif")
        self.picLeft.setMovie(movie)
        self.picRight.setMovie(movie)
        movie.start()
        # 读配置文档ini文件，获取当前站别
        config = configparser.ConfigParser()
        config.read('SEL-SF.ini')
        global station
        station = config.get('Station', 'NextStation')
        # 读取csv模板
        self.readCsv()
        # 实例化读SN的线程类，连接信号
        self.update_SN = upDateSN(self)
        self.update_SN._connectSignal.connect(self.showSN)
        self.update_SN.start()

        # 读取本地csv模板


        # # 定时器读取SN
        # self.timer = QTimer(self) #初始化一个定时器
        # self.timer.start(1000)  #设置间隔
        # self.timer.timeout.connect(self.updateSN)
        # def updateSN(self):
        #     global allsn
        #     # allsn = os.popen('adb devices').readlines()[1].split('\t')[0]
        #     allsn = 'WIP1234567890'
        # 扫SN并回车
        self.SerialNumber.returnPressed.connect(self.backCar)

    def showSN(self, list):
        global allsn
        allsn = []
        for i in range(len(list)):
            if list[i].__contains__('WIP'):
                allsn.append(list[i].split('\t')[0])
        if len(allsn) > 0:
            self.dut_groupbox.setTitle('Device Online')
            self.dut_groupbox.setStyleSheet(
                "QGroupBox#dut_groupbox{ font:75 13pt \"微软雅黑\";  background-color: rgb(11, 255, 47)}")
            for j in range(len(allsn)):
                self.SN_TableWidget.setItem(j, 0, QTableWidgetItem(allsn[j]))
                self.SN_TableWidget.item(j, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        else:
            self.dut_groupbox.setTile("Waiting...")
            self.dut_groupbox.setStyleSheet("QGroupBox#dut_groupbox{ font:75 13pt \"微软雅黑\";  background-color: yellow}")
            self.dut_groupbox.clearContents()

    def backCar(self):
        if (len(self.SerialNumber.text()) != 13):
            msg = QMessageBox.information(self, "提示：", "SN错误", QMessageBox.Yes)
            self.SerialNumber.clear()
        else:
            global allsn
            self.SerialNumber.setEnabled(False)
            for row in range(self.template_1.rowCount()):
                self.template_1.setItem(row, 2, QTableWidgetItem('Waiting....'))
                self.template_1.item(row, 2).setBackground(QBrush(QColor(255, 255, 0)))
            # while(allsn.__contains__(self.SerialNumber.text()) == False):
            #     pass  需要扫SN后等待，判断与adb的是否符合，待解决
            info = self.queryData(self.SerialNumber.text())
            # self.RTestInfo.setText(info)
            # self.RTestInfo.setText("333333")
            if (allsn.__contains__(self.SerialNumber.text()) & len(info) > 800):
                SN_Status = info[info.find("STATUS=") + 7:info.find("STATUS=") + 9]
                WO_Number = info[info.find("WO=") + 3:info.finf("WO=") + 12]
                Mlb_SN = info[info.find("MB_NUM=") + 7:info.find("MB_NUM=") + 30]
                SKUinfo = info[info.find("SKU="):info.find("SKU=") + 10]
                SKUinfo = SKUinfo[:SKUinfo.find(";")]
                Line = info[info.find("LINE=") + 5:info.find("LINE=") + 8]
                # station_Status = {'FAT': '55', 'SUB_AUDIO': '20', 'SUB_LED': '24'}
                # 检查站别
                global station
                if (station == "FAT"):
                    station_Status = "55"
                elif (station == "SUB_TOUCH"):
                    station_Status = "23"
                else:
                    station_Status = "NA"
                if (not station_Status.__contains__(SN_Status)):
                    msg = QMessageBox.information(self, "提示：", "SN错误", QMessageBox.Yes)
                    self.SerialNumber.clear()
                    self.setEnabled(True)
                    return
                # 检查MBSN
                DUT_MB = os.popen('adb  shell cat /factory_setting/mlb_sn.txt')
                if (DUT_MB != Mlb_SN):
                    temp = os.popen('adb shell /home/flex/bin/fct.sh mount_factory')
                    self.RTestInfo.setText('\r\n mount{0}'.format(temp))
                    temp = os.popen('adb shell ls -l /factory_setting')
                    self.RTestInfo.setText('\r\n ls -l /factory_setting{0}'.format(temp))
                    time.sleep(0.5)
                    DUT_MB = os.popen('adb  shell cat /factory_setting/mlb_sn.txt')
                    if (DUT_MB != Mlb_SN):
                        msg = QMessageBox.information(self, "主板序列号错误：", "请确认主板序列号", QMessageBox.Yes)
                        return
                self.RTestInfo.setText("开始测试：")
                if (station == "FAT"):
                    self.FAT()
            else:
                msg = QMessageBox.information(self, "提示：", "SN错误", QMessageBox.Yes)
                pass

    def FAT(self):
        self.RTestInfo.setText("\r\n FAT Start")
        testItemc = 1
        self.template_1.setItem(testItemc, 8, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        #     检查touch_detect
        testStr = os.popen('adb shell /home/flex/bin/fct.sh touch_detect')
        self.RTestInfo.setText('\nDetect Sensor Board over I2C:{0}'.format(testStr))
        if (testStr.lower().__contains__("pass")):
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Pass"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(11, 255, 47)))
        else:
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Fail"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(255, 0, 0)))
        self.template_1.setItem(testItemc, 9, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        #     Component check
        testItemc += 1
        self.template_1.setItem(testItemc, 8, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        test_mlb = os.popen('adb shell /home/flex/bin/fct.sh component_check_mlb')
        if(test_mlb.lower().__contains__("pass")):
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Pass"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(11, 255, 47)))
        else:
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Fail"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(255, 0, 0)))
        self.template_1.setItem(testItemc, 9, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))

        SEL_bad_blocks = os.popen('adb shell /home/flex/bin/fct.sh bad_blocks')
        self.RTestInfo.setText('\nNand_check:{0}'.format(SEL_bad_blocks))
        # Nand Flash Scan
        testItemc += 1
        self.template_1.setItem(testItemc, 8, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        test_nand = os.popen('adb shell /home/flex/bin/fct.sh nand_check 10')
        if (test_nand.lower().__contains__("pass")):
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Pass"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(11, 255, 47)))
        else:
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Fail"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(255, 0, 0)))
        self.template_1.setItem(testItemc, 9, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        # Reset Button----------------------------
        testItemc += 1
        self.template_1.setItem(testItemc, 8, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        test_reset = os.popen('adb shell /home/flex/bin/fct.sh button')
        if (test_reset.upper().__contains__("FAIL")):
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Pass"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(11, 255, 47)))
        else:
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Fail"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(255, 0, 0)))
        self.template_1.setItem(testItemc, 9, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        # led_check_error-----------------------
        testItemc += 1
        self.template_1.setItem(testItemc, 8, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        test_led_check = os.popen('adb shell /home/flex/bin/fct.sh led_check_error')
        if (test_led_check.upper().__contains__("FAIL")):
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Pass"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(11, 255, 47)))
        else:
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Fail"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(255, 0, 0)))
        self.template_1.setItem(testItemc, 9, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    #     Mute Check -----not  Mute
        testItemc += 1
        self.template_1.setItem(testItemc, 8, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        test_mute = os.popen('adb shell /home/flex/bin/fct.sh FCT.2.3')
        if (test_mute.upper().__contains__("FAIL")):
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Pass"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(11, 255, 47)))
        else:
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Fail"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(255, 0, 0)))
        self.template_1.setItem(testItemc, 9, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    #     Muted
        msg = QMessageBox.information(self, "提示：", "请将Mute Button拨至另一方,显现出红色区域", QMessageBox.Yes)
        testItemc += 1
        self.template_1.setItem(testItemc, 8, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        test_muted = os.popen('adb shell /home/flex/bin/fct.sh FCT.2.3')
        if (test_muted.lower().__contains__("pass")):
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Pass"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(11, 255, 47)))
        else:
            self.template_1.setItem(testItemc, 2, QTableWidgetItem("Fail"))
            self.template_1.item(testItemc, 2).setBackground(QBrush(QColor(255, 0, 0)))
        self.template_1.setItem(testItemc, 9, QTableWidgetItem(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    #     ***************************unmount测试***************************
        chkPartHome = os.popen('adb shell /home/flex/bin/fct.sh umount_factory')
        self.RTestInfo.setText("\n" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "\numount_factory:{0} ".format(chkPartHome))
        if(not chkPartHome.upper().__contains__("PASS")):
            self.RTestInfo.setText(
                "\n" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "\numount_factory failed:{0} ".format(chkPartHome))
            self.RTestInfo.setStyleSheet("QtWidgets#template_1{background-color: red}")
            return
        self.RTestInfo.setStyleSheet("QtWidgets#template_1{background-color: green}")
    def readCsv(self):
        csv_reader = csv.reader(open('FAT.csv', 'r'))
        self.template_1.setColumnCount(10)
        for index, line in enumerate(csv_reader):
            if (index == 0):
                self.template_1.setHorizontalHeaderLabels(line)
            else:
                self.template_1.insertRow(index - 1)
                for item in line:
                    self.template_1.setItem(index - 1, line.index(item), QTableWidgetItem(item))
                    # self.template_1.item(index - 1, line.index(item)).setTextAlignment(QtCore.Qt.AlignCenter)

    def queryData(self, SN):
        conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=10.18.6.53;DATABASE=QMS;UID=sdt;PWD=SDT#7')
        data = "SN=" + SN + ";$;Station=QueryData;$;MonitorAgentVer=VL20151102.01;$;"
        sqlcommand = '''DECLARE @ReturnValue varchar(7400)
                        EXEC %s '%s', '%s', '%s', '%s', @ReturnValue output
                        SELECT @ReturnValue''' % ('MonitorPortal', 'PU4', 'SWDL', 'QueryData', data)
        cursor = conn.cursor()
        cursor.execute(sqlcommand)
        returnResult = cursor.fetchall()[0]
        cursor.commit()
        cursor.close()
        return returnResult


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainView = view()
    mainView.show()
    sys.exit(app.exec_())
