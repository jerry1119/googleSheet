from ctypes import *

import time

import ctypes

Fly2 = ctypes.windll.LoadLibrary("PointGrey.dll")

PT_SetWhiteBalance = Fly2.PT_SetWhiteBalance #WB(Red/Blue)
PT_SetGamma =  Fly2.PT_SetGamma #Gamma
PT_CamInitFromIndex = Fly2.PT_CamInitFromIndex #Initialization
PT_CamInitFromSerial = Fly2.PT_CamInitFromSerial
PT_StartCapture = Fly2.PT_StartCapture #Start continuous capture
PT_FreezeCapture = Fly2.PT_FreezeCapture #Stop continuous capture
PT_PreViewImage = Fly2.PT_PreViewImage #Pop up preview dialog
PT_PreViewHide = Fly2.PT_PreViewHide   #Hide preview dialog
PT_GetImageData= Fly2.PT_GetImageData#get raw data
PT_SnapImageAndSaveBmp= Fly2.PT_SnapImageAndSaveBmp#save image
PT_DestroyWnd =Fly2.PT_DestroyWnd #destroy preview window
PT_SetGain = Fly2.PT_SetGain#
PT_SetShutter = Fly2.PT_SetShutter #
print("1")
ret = PT_CamInitFromIndex(0)
print("2")
if(ret==1):
    print("Camera Init OK")
    PT_PreViewImage('video',800,10,1200,900)
    PT_StartCapture()
    while(1):
        pass
else:
    print("Camera Init Fail")




 

