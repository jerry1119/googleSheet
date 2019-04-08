from ctypes import *
import sys
import time
import numpy as np

import ctypes
Fly2 = ctypes.windll.LoadLibrary("PointGrey.dll")

class Buff(Structure):
        _fields_ =[('Rgbdata', (c_ubyte) * (4* 2448 * 2048))]
    
m_pRgbData=Buff()
m_pRgbData_p=pointer(m_pRgbData)

str0 = u"123.bmp"
import unicodedata
FileName=unicodedata.normalize('NFKD',str0).encode('ascii','ignore')

PT_SetWhiteBalance = Fly2.PT_SetWhiteBalance  #WB(Red/Blue)
PT_SetGamma =  Fly2.PT_SetGamma  #Gamma
PT_CamInitFromIndex = Fly2.PT_CamInitFromIndex #Initialize
PT_CamInitFromSerial = Fly2.PT_CamInitFromSerial
PT_StartCapture = Fly2.PT_StartCapture #Start continuous capture
PT_FreezeCapture = Fly2.PT_FreezeCapture #Stop continuous capture
PT_PreViewImage = Fly2.PT_PreViewImage #Pop up preview dialog
PT_PreViewHide = Fly2.PT_PreViewHide   #Hide preview dialog
PT_GetImageData= Fly2.PT_GetImageData #get raw data
PT_SnapImageAndSaveBmp= Fly2.PT_SnapImageAndSaveBmp #save image
PT_DestroyWnd =Fly2.PT_DestroyWnd #destroy preview window
PT_SetGain = Fly2.PT_SetGain #get gain
PT_SetShutter = Fly2.PT_SetShutter #set exposure
PT_GetShutterRange = Fly2.PT_GetShutterRange
PT_GetGainRange = Fly2.PT_GetGainRange

ret = PT_CamInitFromIndex(0)
if(ret==1):
    print("Camera Init OK")
    PT_SetWhiteBalance(698, 0) #--WB(Red)
    PT_SetWhiteBalance(741, 1) #--WB(Blue)
    PT_SetGamma(0)  #--Gamma
    PT_SetShutter(c_float(100.000)) #--Set Shutter
    PT_SetGain(c_float(4.000))  #--Set Gain
    
    time.sleep(1)
    
    PT_PreViewImage('video',800,10,1200,900)
    PT_StartCapture()    
    while(1):
        #time.sleep(1)
        PT_SnapImageAndSaveBmp(FileName) #--Save bmp
        PT_GetImageData(m_pRgbData)
        a0 = np.frombuffer(m_pRgbData, dtype="uint8")
        for i in range(0,(1000)): #--print pre 1000 values
                print(a0[i])
        time.sleep(3)
else:
    print("Camera Init Fail")




 

