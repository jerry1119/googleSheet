#Box Calibration
#Run this script to calibrate the boxes
"""
Steps:
1. AutoExposure
2. Turn on sRGB primaries
3. record sRGB primaries in camera rgb values
4. record camera serial number
If a non-Golden Chirp is inserted, it will NOT be successful (adb pull will 
fail since the file does NOT exist on non-Golden Chirp units)
"""
#Create "camera.ini". 
exec(open('./conveniencefuncs.py').read())
#*************************
#start here
printmessages = True
cal_ratio_failure_thres = 0.9
ret = InitializeCamera()
if(ret == 1):
    snstring = GetChirpSerialNumber()
    if printmessages:
        print('device serial number: ' + snstring)
    led_cal = ChirpLEDCalibrator()
    #Turn all LEDs to 100% duty cycle, perform auto-exposure
    led_cal.RunShellOnChirp(led_cal.all_on_filename)
    AutoExposure(150, 200, 1, fastmode = True)
    all_on_img = GetPictureReliably()
    #Turn off all LEDs, get dark frame
    led_cal.RunShellOnChirp(led_cal.all_dark_filename)
    time.sleep(1) #just to be safe
    all_dark_img = GetPictureReliably()
    #Turn on all LEDs, get dot locations and sizes
    all_on_ds_img = cv.addWeighted(all_on_img, 1.0, all_dark_img, -1.0, 0.0)
    #Detect dots locations and sizes
    w_stats = DotStats(all_on_ds_img)
    w_stats.DetectAnalyze(expected_dot_size, False, False)
    if printmessages:
        print(w_stats.dot_sizes)
        print(w_stats.rgbvalues)
        print(w_stats.coordinates)  
    dot_coordinates = w_stats.coordinates
    dot_sizes = w_stats.dot_sizes
    num_dots = w_stats.num_dots
    if not led_cal.CheckNumLEDs(w_stats, echomessages = printmessages):
        quit()
    #Initialize Golden Chirp
    led_cal.RunShellOnChirp(led_cal.mode10_filename) #mode 10
    led_cal.LoadCCMfromCoords()
    ###Red
    led_cal.DispCalibratedUniform([255, 0, 0])
    sRGB_R_img = GetPictureReliably()
    sRGB_R_img_ds = cv.addWeighted(sRGB_R_img, 1.0, all_dark_img, -1.0, 0.0)
    sRGB_R_stats = DotStats(sRGB_R_img_ds)
    sRGB_R_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    sRGB_R_stats.AnalyzeDots()
    if not led_cal.CheckBrightnessRatio(sRGB_R_stats, \
                    ratio_thres = cal_ratio_failure_thres, \
                    echomessages = printmessages):
        quit()
    if printmessages:
        print(sRGB_R_stats.rgbvalues)
    ###Green
    led_cal.DispCalibratedUniform([0, 255, 0])
    sRGB_G_img = GetPictureReliably()
    sRGB_G_img_ds = cv.addWeighted(sRGB_G_img, 1.0, all_dark_img, -1.0, 0.0)
    sRGB_G_stats = DotStats(sRGB_G_img_ds)
    sRGB_G_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    sRGB_G_stats.AnalyzeDots()
    if not led_cal.CheckBrightnessRatio(sRGB_G_stats, \
                    ratio_thres = cal_ratio_failure_thres, \
                    echomessages = printmessages):
        quit()
    if printmessages:
        print(sRGB_G_stats.rgbvalues)
    ###Blue
    led_cal.DispCalibratedUniform([0, 0, 255])
    sRGB_B_img = GetPictureReliably()
    sRGB_B_img_ds = cv.addWeighted(sRGB_B_img, 1.0, all_dark_img, -1.0, 0.0)
    sRGB_B_stats = DotStats(sRGB_B_img_ds)
    sRGB_B_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    sRGB_B_stats.AnalyzeDots()
    if not led_cal.CheckBrightnessRatio(sRGB_B_stats, \
                    ratio_thres = cal_ratio_failure_thres, \
                    echomessages = printmessages):
        quit()
    if printmessages:
        print(sRGB_B_stats.rgbvalues)    
    #Create calibration file
    cam_sn_str = '%d' % GetCameraSerialNumber() 
    led_cal.WriteBoxCalFile(sRGB_R_stats, sRGB_G_stats, sRGB_B_stats, cam_sn_str)
    
    
# de-init
led_cal.RunShellOnChirp(led_cal.all_dark_filename)
ReleaseCamera()
