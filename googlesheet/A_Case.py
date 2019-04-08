#coding=utf8

'''
author @ orange
06/22/2017
'''
import Tkinter as tk
import threading
import ScrolledText
import time
import datetime
import os
import subprocess
import ConfigParser
import copy
import csv
import shutil
import tkMessageBox
import signal
import re
import SFdB
from collections import Counter

class A50_GUI():

    def __init__(self, master):
        self.master = master
        self.gui_show(self.master)

    def gui_show(self, master):

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('setting.ini')
            self.version_pro = cf.get('ProgramInfo','version')
        except Exception as e:
           pass

        '''设置窗体的基本信息'''
        master.minsize(800,600)
        master.resizable(False,False)

        #控件之家的间距
        _padx = 20
        _pady = 20

        #label的值
        _program_info_label = self.version_pro
        _dut_info_labelframe = 'DUT Info'
        _dut_sn_label = 'SN'
        _dut_result_label = 'Result'
        _dut_test_time = 'Test Count'

        _program_meassage_info = 'Program Messsage'

        #背景颜色
        _color_1 = '#bdbdbd'
        self._pass_color = 'GREEN'
        self._fail_color = 'RED'
        self._normal_color = '#97ffff'

        #字体样式
        _font_1 = ('Tiems','25','bold')
        _font_2 = ('Tiems','20','bold')

        #项目/站别信息
        Program_Info_Label = tk.Label(master, text = _program_info_label,font = _font_2, justify = 'left')
        Program_Info_Label.grid(row=0,column=0,sticky='w')

        #DUT信息，包含SN,结果以及测试次数
        DUT_Info_LabelFrame = tk.LabelFrame(master, text = _dut_info_labelframe, bg = _color_1, font = _font_1)
        DUT_SN_Label_LabelFrame = tk.Label(DUT_Info_LabelFrame,wraplength = 100, text = _dut_sn_label, bg = _color_1, font = _font_1)
        self.SN_Entry_text = tk.StringVar()    #设置DUT SN
        DUT_SN_Entry = tk.Entry(DUT_Info_LabelFrame,textvariable=self.SN_Entry_text, state = 'readonly',width = 20, justify = 'left', font = _font_1)
        DUT_Result_Label = tk.Label(DUT_Info_LabelFrame,text = _dut_result_label,bg = _color_1,font=_font_1)
        self.DUT_Result_Status = tk.StringVar()    #设置结果PASS/FAIL
        self.DUT_Result_Status_Label = tk.Label(DUT_Info_LabelFrame, textvariable=self.DUT_Result_Status,bg=_color_1,font=_font_1)
        DUT_Test_Times_Label = tk.Label(DUT_Info_LabelFrame, text = _dut_test_time,bg=_color_1,font=_font_1)
        self.DUT_test_time = tk.StringVar()    #设置测试次数！
        self.DUT_Test_Times_Status_Label = tk.Label(DUT_Info_LabelFrame,textvariable=self.DUT_test_time,bg=_color_1,font=_font_1)
        
        DUT_SN_Label_LabelFrame.grid(row=0,column=0, padx = _padx,pady=_pady)
        DUT_SN_Entry.grid(row=0,column=1, padx = _padx,pady=_pady)
        DUT_Result_Label.grid(row = 1, column=0)
        self.DUT_Result_Status_Label.grid(row = 1, column=1)
        DUT_Test_Times_Label.grid(row=2,column=0, padx = _padx,pady=_pady)
        self.DUT_Test_Times_Status_Label.grid(row=2,column=1)

        DUT_Info_LabelFrame.grid(row = 1, column=0,columnspan=2)
        
        #DUT目前站别状态！
        #DUT_Now_Status_LabelFrame()

        #测试细项

        #程序运行信息
        Program_Message_LabelFrame = tk.LabelFrame(master,text= _program_meassage_info)
        self.textscroll = ScrolledText.ScrolledText(Program_Message_LabelFrame,width=125,height=25,wrap=tk.WORD,bg= self._normal_color,font=16)
        self.textscroll.grid(row=0,column=1,columnspan=4)
        self.textscroll.bind('<Button>', lambda e: 'break')

        Program_Message_LabelFrame.grid(row=3,column=0,columnspan=4,padx = _padx, pady = _pady)

    def GUI_Show_Detail(self,event,gui_Info):
        '''
        通过传入gui_Info = {'code':'MSG/ERROR/PASS/FAIL', 'SN':'8********','test_time':1,'show':'initial show info'}
        进行信息的打印显示
        '''
        ui_Info = {}
        pass_fail = ["PASS","FAIL"]
        error_msg = ["ERROR","MSG"]
        try:
            if gui_Info.get('code').upper() in pass_fail:
                self.pass_fail_gui(gui_Info)
            elif gui_Info.get('code').upper() in error_msg:
                self.error_msg_gui(gui_Info)
            else:
                ui_Info['code'] = 'ERROR'
                ui_Info['show'] = 'please check info setting!'+str(gui_Info)
                self.error_msg_gui(ui_Info)
        except Exception as e:
            print (e.message)
            ui_Info['code'] = 'ERROR'
            ui_Info['show'] = 'please check info setting!'+str(gui_Info)
            self.error_msg_gui(ui_Info)

    def pass_fail_gui(self,info):
        '''
        显示Pass/Fail状态
        '''
        if info.get('code').upper() == 'PASS':
            self.SN_Entry_text.set(info.get('SN'))
            self.DUT_Result_Status.set(info.get('code'))
            self.DUT_Result_Status_Label.configure(bg=self._pass_color)
            self.DUT_test_time.set(info.get('test_time'))
            self.textscroll.configure(bg = self._pass_color)
            self.textscroll.insert(tk.INSERT,info.get('show'))
            self.textscroll.insert(tk.INSERT,'\r\n')
            self.textscroll.update()
        else:
            self.SN_Entry_text.set(info.get('SN'))
            self.DUT_Result_Status.set(info.get('code'))
            self.DUT_Result_Status_Label.configure(bg=self._fail_color)
            self.DUT_test_time.set(info.get('test_time'))
            self.textscroll.configure(bg = self._fail_color)
            self.textscroll.insert(tk.INSERT,info.get('show'))
            self.textscroll.insert(tk.INSERT,'\r\n')
            self.textscroll.update()

    def error_msg_gui(self,info):
        '''显示Error/Msg信息'''
        print ('error test')
        if info.get('code').upper() == 'ERROR':
            self.textscroll.configure(bg=self._fail_color)
            #time.sleep(0.5)
            self.textscroll.insert(tk.END,info.get('show'))
            self.textscroll.update()
            print (info.get('show'))
        else:
            #self.textscroll.configure(bg=self._normal_color)
            self.textscroll.insert(tk.INSERT,info.get('show'))
            self.textscroll.update()
            print (info.get('show'))

    def destroy_gui(self):
        '''关闭窗口，并杀死进程'''
        if tkMessageBox.askyesno('Close',u'是否关闭？'):
            self.master.destroy()
            PID = os.getpid()
            print (PID)
            os.kill(PID, signal.SIGBREAK)
            


class ThreadPart():
    def __init__(self,master):
        self.master = master
        self.gui = A50_GUI(self.master)
        self.ThreadLog_1 = threading.Thread(target=self.processLogSF)
        self.ThreadLog_1.start()

        self.info_show = {'code':'MSG', 'SN':'8********','test_time':1,'show':'initial show info'}    #传入需要显示的信息

        def handler_info_show(event,self = self,info = self.info_show):
            '''操作ERROR/MSG/PASS/FAIL'''
            return self.gui.GUI_Show_Detail(event,info)
        
        #设置监听事件
        self.master.bind("<<UploadGS>>",handler_info_show)
        self.master.bind("<<ERROR>>",handler_info_show)
        self.master.bind("<<MSG>>",handler_info_show)
        self.master.bind("<<PASS>>",handler_info_show)
        self.master.bind("<<FAIL>>",handler_info_show)



    
    def processLogSF(self):
        '''
        处理Log,获取测试结果并上传至Google Server
        '''
        try:
            cf = ConfigParser.ConfigParser()
            cf.read('setting.ini')
            log_Path = cf.get('Path','logpath')
            self.station_Name = cf.get('StationInfo', 'stationname')
            self.station_type = cf.get('StationInfo', 'stationtype')
            self.sfstation = cf.get('SFStation','station')
        except Exception as e:
            print (u'load configure file error >>>>>>>>>>',e.message)
        
        #创建本地保存Log的路径！
        self.log_list = ['//10.18.6.33/SEL_Monitor/A50_eve/A50_Audio/'+self.station_Name+'/Pass/','//10.18.6.33/SEL_Monitor/A50_eve/A50_Audio/'+self.station_Name+'/Fail/','//10.18.6.33/SEL_Monitor/A50_eve/A50_Audio/'+self.station_Name+'/Error/']
        self.createDir(self.log_list)

        self.test_status = ''
        while True:
            try:
                log_file_list = os.listdir(log_Path)
            except Exception as e:
                self.setErrorMsg(msgType='Error',Info=str(e))
            if len(log_file_list) != 0:
                for log_file in log_file_list:
                    log_file_path = log_Path + log_file
                    try:
                        if not self.judgeformat(log_file,['.csv','8',10]):
                            print ('log format error')
                            self.setErrorMsg(msgType='Error',Info=u'log format error ==  '+log_file)
                            shutil.move(log_file_path,self.log_list[2]+log_file)
                            continue

                        file_open = open(log_file_path)
                        file_csv_reader = csv.reader(file_open)
                        result_t = self.get_result_from_log(file_csv_reader)
                        file_open.close()
                        if result_t == 'Pass':
                            self.test_status = 'PASSED'
                        else:
                            self.test_status = 'FAILED'
                        SN_T = re.split('_',log_file)[0].upper()
                        self.gui.textscroll.delete(0.0,tk.END)
                        get_sf_info = self.DB_update(SN_T,self.test_status,result_t)
                        print (get_sf_info)
                        dut_test_time = get_sf_info.get('testTime')
                        show_detail = get_sf_info.get('detail')
                        if get_sf_info.get('code') == 'PASS':
                            self.setErrorMsg(msgType='Msg',Info=show_detail)
                            if self.processGoogleSF_txt(self.test_status,log_file_path):
                                self.setErrorMsg(msgType='Msg',Info='upload pass log done!>>>>>>'+log_file_path)
                        elif get_sf_info.get('code') == 'FAIL':
                            self.setErrorMsg(msgType='Error',Info=show_detail)
                            if self.processGoogleSF_txt(self.test_status,log_file_path):
                                self.setErrorMsg(msgType='Msg',Info='upload pass log done!>>>>>>'+log_file_path)
                        if self.test_status == 'PASSED':
                            shutil.move(log_file_path,self.log_list[0] +log_file)
                        else:
                            shutil.move(log_file_path,self.log_list[1]+log_file)
                        print ('perfect>>>>>>>>>>>>>>>>>>>>>')
                    except Exception as e:
                        print (e,'===================')
                        self.setErrorMsg(msgType='Error',Info=str(e))
            time.sleep(1)

    def DB_update(self, SN, status, test_ERROR_CODE):
        return_info = {}
        #test_ERROR_CODE = 'FAIL'
        ftest_code = 'FAIL'
        count_fail = self.count_fail_times(SN,self.log_list[1])
        testTime = count_fail+1
        return_info['testTime'] = testTime
        if status == 'PASSED':
            test_ERROR_CODE = 'PASS'
            if count_fail ==0:
                ftest_code = 'PASS'
            elif count_fail == 1:
                ftest_code = 'RETEST'
            elif count_fail == 2:
                ftest_code = 'NTF'
            else:
                ftest_code = 'FAIL'
        elif status == 'FAILED':
            #test_ERROR_CODE = 'FAIL'
            ftest_code = 'FAIL'
        if test_ERROR_CODE == 'PASS' or count_fail >= 2:
            getresult =SFdB.SF_Station().uploadInfo(self.sfstation,SN,test_ERROR_CODE,ftest_code)
            self.setPF_info(msgType='Pass',SN=SN,test_Time=testTime ,info='This time test Pass>>>>>' + SN)
            return_info['detail'] = getresult
            if getresult.find('SET SF_CFG_CHK=PASS') != -1:
                return_info['code'] = 'PASS'
            else:
                return_info['code'] = 'FAIL'
        else:
            self.setPF_info(msgType='Fail',SN=SN,test_Time=testTime,info='This time test Fail>>>>>' + SN)
            return_info['code'] = 'FAIL'
            return_info['detail'] = 'This time test Fail>>>>>' + SN
        
        return return_info

    def count_fail_times(self,SN,folder_path):
        '''
        传入SN和文件夹路径，返回SN出现次数
        '''
        print (folder_path)
        sn_list =[re.split('_',sn)[0] for sn in os.listdir(folder_path)]
        count_f = Counter(sn_list)
        fail_time = count_f[SN]
        return fail_time

    def judgeformat(self,filename,usr_format):
        '''
        判断文件的格式和前缀是否符合要求:
        usr_format[0] 文件格式;
        usr_format[1] 文件名开头
        usr_format[2] SN长度
        不符合要求返回False
        '''
        try:
            SN = re.split('_',filename)[0]
            len_sn = len(SN)
            usr_format_len = 0-len(usr_format[0])
            usr_start_len = len(usr_format[1])
        except Exception as e:
            return False
        if filename[usr_format_len:] == usr_format[0] and filename[:usr_start_len] == usr_format[1] and len_sn == usr_format[2]:
            return True
        return False
    
    def get_result_from_log(self,csv_reader):
        '''传入csv.reader()实例，返回测试结果，Pass/Fail/Error'''
        result = 'Pass'
        resultCount=0
        errorcodeList=['FCMF2','FCMT3','FCMF3','FCMT4']
        try:
            for row in csv_reader:
                if '@_Result' in row[0]:
                    result_temp = row[3].strip()
                    if result_temp == 'Fail':
                        result = errorcodeList[resultCount]
                        resultCount+=1
            return result
        except Exception as e:
            print (e.message)
            result = 'Error'
            return result

    def createDir(self,path_name):
        '''
        创建文件目录,
        支持string和list,必须是完整路径
        '''
        path_t = copy.deepcopy(path_name)
        if isinstance(path_t,str):
            if not os.path.exists(path_name):
                os.makedirs(path_name)
        elif isinstance(path_t,list):
            print (path_name)
            for item in path_name:
                if not os.path.exists(item):
                    os.makedirs(item)
        else:
            print (u'create folder fail!', path_name)

    def checkPathStr(self,path):
        '''
        暂时未实现
        检查路径是否正确，以及替换'\','\\'为'/'
        '''
        pass

    

    def setErrorMsg(self,msgType='Error',Info='some error'):
        '''
        设置错误或者其他信息
        Error/Msg
        '''
        self.info_show['code'] = msgType.upper()
        self.info_show['show'] = Info+'\n'
        print (self.info_show)
        print ("<<%s>>"%msgType)
        self.master.event_generate("<<%s>>"%msgType.upper(),when='tail')

    def setPF_info(self,msgType='Pass',SN='',test_Time = 0,info='some happen'):
        '''设置PASS/FAIL信息'''
        self.info_show['code'] = msgType.upper()
        self.info_show['SN'] = SN
        self.info_show['test_time'] = test_Time
        self.info_show['show'] = info+'\n'
        print (self.info_show)
        print ("<<%s>>"%msgType)
        self.master.event_generate("<<%s>>"%msgType.upper(),when='tail')
       


    def processGoogleSF_txt(self,test_status,file_path):
        '''
        使用curl上传Log信息到Google Big Query,上传Test Log(txt/csv) 示例
        curl -i -X POST -F 'event={"uuid": "uuid", "type": "station.test_run", "apiVersion": "0.1", "time": {"__type__": "datetime", "value": "2017-06-01T23:42:51.864Z"}, "testRunId": "runid", "testName": "testname", "testType": "testtype", "arguments": {"keyname": {"value": 0}}, "status": "PASSED", "startTime": {"__type__": "datetime", "value": "2017-06-02T15:15:22.334Z"}, "attachments": {"test2.txt": {"path": "/tmp/test2.txt", "mimeType": "text/plain"}}}'-F 'test2.txt=@/tmp/test2.txt' 10.3.0.11:8080/instalog

         上传完成之后返回True
        '''
        date_time_t = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime())
        date_time = date_time_t + '.'+ str(datetime.datetime.now().microsecond)[:3] +'Z'
        testname = self.station_Name
        testtype = self.station_type
        status = test_status    #PASSED/FAILED
        filename = os.path.basename(file_path)[:-4] +'_'+ testname +'.csv'
        others = '%s=@%s'%(filename,file_path)
        sn_dut = re.split('_',filename)[0]
        #curlCommand需要补充信息依次为 time,testname,testtpye,status(PASSED/FAILED),time,filename,filedirctpath,others
        curlCommand = '''curl -i -X POST -F 'event={"uuid": "uuid", "type": "station.test_run", "apiVersion": "0.1", 
        "time": {"__type__": "datetime", "value": "%s"}, 
        "testRunId": "runid", "testName": "%s", "testType": "%s", 
        "arguments": {"keyname": {"value": 0}}, "status": "%s", 
        "startTime": {"__type__": "datetime", "value": "%s"}, 
        "attachments": {"%s": {"path": "%s", "mimeType": "text/plain"}}}'
         -F '%s' 10.3.0.11:8080/instalog
         '''%(date_time,testname,testtype,status,date_time,filename,file_path,others)
        print (curlCommand)
        command_out = ''
        if self.check_network('10.3.0.11'):
            command_out = subprocess.check_output(curlCommand)
            print (command_out)
            if command_out.find('200 OK')!=-1:
                print ('upload server complete!', file_path)
                self.setErrorMsg(msgType='MSG',Info='upload server complete!>>>>>>'+file_path)
                return True
        else:
            print ('please check net error')
            self.setErrorMsg(msgType='Error',Info='please check net error')
            return False
        

    def check_network(self,ip_addr):
        '''
        如果ping不通，返回False,否则返回True
        '''
        command = 'ping -n 2 -w 100 ' + ip_addr
        t = subprocess.call(command,shell=True)
        if t == 1:
            return False
        return True

    

if __name__ == '__main__':
    
    root = tk.Tk()
    client = ThreadPart(root)
    def closeWindow():
        '''关闭窗口，并杀死进程'''
        if tkMessageBox.askyesno('Close',u'是否关闭？') :
            PID = os.getpid()
            print (PID)
            os.kill(PID, signal.SIGBREAK)
            root.destroy()
    root.wm_protocol('WM_DELETE_WINDOW',closeWindow)
    root.mainloop()
