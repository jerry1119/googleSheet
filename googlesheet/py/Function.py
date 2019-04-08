# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Function.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(911, 585)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setMaximumSize(QtCore.QSize(300, 300))
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 2, 2, 1, 1)
        self.RTestInfo = QtWidgets.QTextEdit(Form)
        self.RTestInfo.setObjectName("RTestInfo")
        self.gridLayout.addWidget(self.RTestInfo, 2, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.picLeft = QtWidgets.QLabel(Form)
        self.picLeft.setMinimumSize(QtCore.QSize(106, 260))
        self.picLeft.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.picLeft.setObjectName("picLeft")
        self.horizontalLayout.addWidget(self.picLeft)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setStyleSheet("QTabWidget::pane {\n"
"    border:none\n"
"}\n"
"QTabBar::tab-bar {\n"
"    aligment: center\n"
"}\n"
"QTabBar::tab {\n"
"    background: transparent;\n"
"    color: white;\n"
"    min-width: 16ex;\n"
"    max-height: 6ex\n"
"}\n"
"QTabBar::tab:hover{\n"
"    background: rgb(255,255,255,100)\n"
"}\n"
"QTabBar::tab:selected{\n"
"    border-color: white;\n"
"    background:lightgrey;\n"
"    color:green\n"
"\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.template_1 = QtWidgets.QTableWidget(self.tab_3)
        self.template_1.setEnabled(True)
        self.template_1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.template_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.template_1.setObjectName("template_1")
        self.template_1.setColumnCount(0)
        self.template_1.setRowCount(0)
        self.gridLayout_2.addWidget(self.template_1, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.picRight = QtWidgets.QLabel(Form)
        self.picRight.setMinimumSize(QtCore.QSize(106, 260))
        self.picRight.setObjectName("picRight")
        self.horizontalLayout.addWidget(self.picRight)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 3)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 131, 31))
        self.label_2.setStyleSheet("font: 12pt \"幼圆\";")
        self.label_2.setObjectName("label_2")
        self.SerialNumber = QtWidgets.QLineEdit(self.groupBox_2)
        self.SerialNumber.setGeometry(QtCore.QRect(10, 50, 156, 35))
        self.SerialNumber.setMinimumSize(QtCore.QSize(156, 35))
        self.SerialNumber.setObjectName("SerialNumber")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(180, 20, 131, 31))
        self.label_3.setStyleSheet("font: 12pt \"幼圆\";")
        self.label_3.setObjectName("label_3")
        self.Standby = QtWidgets.QLineEdit(self.groupBox_2)
        self.Standby.setGeometry(QtCore.QRect(180, 50, 156, 35))
        self.Standby.setMinimumSize(QtCore.QSize(156, 35))
        self.Standby.setObjectName("Standby")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(350, 40, 131, 31))
        self.label_4.setStyleSheet("font: 12pt \"幼圆\";")
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(430, 40, 131, 31))
        self.label_7.setStyleSheet("font: 12pt \"幼圆\";")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 2)
        self.dut_groupbox = QtWidgets.QGroupBox(Form)
        self.dut_groupbox.setMinimumSize(QtCore.QSize(210, 200))
        self.dut_groupbox.setMaximumSize(QtCore.QSize(220, 200))
        self.dut_groupbox.setObjectName("dut_groupbox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dut_groupbox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.SN_TableWidget = QtWidgets.QTableWidget(self.dut_groupbox)
        self.SN_TableWidget.setMinimumSize(QtCore.QSize(200, 100))
        self.SN_TableWidget.setRowCount(4)
        self.SN_TableWidget.setColumnCount(1)
        self.SN_TableWidget.setObjectName("SN_TableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.SN_TableWidget.setHorizontalHeaderItem(0, item)
        self.SN_TableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.SN_TableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.gridLayout_4.addWidget(self.SN_TableWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.dut_groupbox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.picLeft.setText(_translate("Form", "LeftGif"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "Tab 2"))
        self.picRight.setText(_translate("Form", "RightGif"))
        self.groupBox_2.setTitle(_translate("Form", "Test unit Info"))
        self.label_2.setText(_translate("Form", "Serial Number:"))
        self.label_3.setText(_translate("Form", "StanfBy:"))
        self.label_4.setText(_translate("Form", "Status:"))
        self.label_7.setText(_translate("Form", "0"))
        self.dut_groupbox.setTitle(_translate("Form", "Device Info"))
        item = self.SN_TableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "SN"))

