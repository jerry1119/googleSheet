#Golden Chirp Step 1:
#Calibrate Chirp IREF values, write a calibration file with only IREF correction
#Values
exec(open('./conveniencefuncs.py').read())
#*************************
#start here
picture_directory = '.\\pictures\\Golden_Chirps\\'
printcheckinfo = True
raw_ratio_failure_thres = 0.5
ratio_thres_calibrated = 0.9


ret = InitializeCamera()
if(ret==1):
    #append serial number to folder name
    snstring = GetChirpSerialNumber()
    picture_directory = picture_directory + snstring + '\\'
    if not os.path.isdir(picture_directory):
        os.system('mkdir ' + picture_directory)
    #Turn all LEDs to 100% duty cycle, perform auto-exposure
    RunShellOnChirp(all_on_filename)
    AutoExposure(150, 200, 1, fastmode = True)
    #Capture bright and dark images, calculate dark-subtracted image
    all_on_img = GetPictureReliably()
    RunShellOnChirp(all_dark_filename)
    time.sleep(1)
    all_dark_img = GetPictureReliably()
    all_on_ds_img = cv.addWeighted(all_on_img, 1.0, all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_on_wo_iref_cal.png', all_on_ds_img)
    #Detect dots locations and sizes
    w_stats = DotStats(all_on_ds_img)
    w_stats.DetectAnalyze(expected_dot_size, False, False)
    print(w_stats.dot_sizes)
    print(w_stats.rgbvalues)
    print(w_stats.coordinates)
    #Instantiate LED Calibrator
    led_calibrator = ChirpLEDCalibrator()
    #Check number of LEDs and ratio
    if not led_calibrator.CheckNumLEDs(w_stats, echomessages = printcheckinfo):
        quit()
    if not led_calibrator.CheckBrightnessRatio(w_stats, \
        ratio_thres = raw_ratio_failure_thres, \
        echomessages = printcheckinfo):
        quit()
    #Record dots information
    dot_coordinates = w_stats.coordinates
    dot_sizes = w_stats.dot_sizes
    num_dots = w_stats.num_dots
    #*********************************************
    #Collect brightness variation info, Correct IREF values
    #*********************************************
    ##Red
    RunShellOnChirp(all_red_filename)
    all_red_img = GetPictureReliably()
    all_red_ds_img = cv.addWeighted(all_red_img, 1.0,\
                                    all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_red_wo_iref_cal.png', all_red_ds_img)
    r_raw_stats = DotStats(all_red_ds_img)
    r_raw_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    r_raw_stats.AnalyzeDots()
    if printcheckinfo:
        print('check red raw stats:')
    if not led_calibrator.CheckBrightnessRatio(r_raw_stats, \
        ratio_thres = raw_ratio_failure_thres, \
        echomessages = printcheckinfo):
        quit()
    ##Green
    RunShellOnChirp(all_green_filename)
    all_green_img = GetPictureReliably()
    all_green_ds_img = cv.addWeighted(all_green_img, 1.0, \
                                    all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_green_wo_iref_cal.png', all_green_ds_img)
    g_raw_stats = DotStats(all_green_ds_img)
    g_raw_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    g_raw_stats.AnalyzeDots()
    if printcheckinfo:
        print('check green raw stats:')
    if not led_calibrator.CheckBrightnessRatio(g_raw_stats, \
        ratio_thres = raw_ratio_failure_thres, \
        echomessages = printcheckinfo):
        quit()
    ##Blue
    RunShellOnChirp(all_blue_filename)
    all_blue_img = GetPictureReliably()
    all_blue_ds_img = cv.addWeighted(all_blue_img, 1.0, \
                                    all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_blue_wo_iref_cal.png', all_blue_ds_img)
    b_raw_stats = DotStats(all_blue_ds_img)
    b_raw_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    b_raw_stats.AnalyzeDots()
    if printcheckinfo:
        print('check blue raw stats:')
    if not led_calibrator.CheckBrightnessRatio(b_raw_stats, \
        ratio_thres = raw_ratio_failure_thres, \
        echomessages = printcheckinfo):
        quit()
    RunShellOnChirp(all_dark_filename)
    #***************************************************************
    #Calibrate IREF values
    led_calibrator.CalculateIrefValues(r_raw_stats, g_raw_stats, b_raw_stats)
    led_calibrator.WriteIrefRegisters()
    #Write calibration file
    led_calibrator.WritePushIrefCalibrationFile(picture_directory)
    ##**********************************
    ##Verify calibration results
    ##Green
    RunShellOnChirp(all_green_no_iref_filename)
    all_green_iref_img = GetPictureReliably()
    RunShellOnChirp(all_dark_no_iref_filename)
    all_green_iref_ds_img = cv.addWeighted(all_green_iref_img, 1.0, \
                                        all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_green_with_iref_cal.png', all_green_iref_ds_img)
    g_iref_stats = DotStats(all_green_iref_ds_img)
    g_iref_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    g_iref_stats.AnalyzeDots()
    if printcheckinfo:
        print('check green iref calibrated stats:')
    if not led_calibrator.CheckBrightnessRatio(g_iref_stats, \
        ratio_thres = ratio_thres_calibrated, \
        echomessages = printcheckinfo):
        quit()
    #plot green variation
    plt.figure(figsize = (12,8), dpi = 100)
    plt.plot(g_raw_stats.luminancevalues, 'ro', markersize = 20, label = 'Before IREF Calibration')
    plt.plot(g_iref_stats.luminancevalues, 'gs', markersize = 20, label = 'After IREF Calibration')
    plt.legend()
    plt.title('green LEDs luminance level before and after IREF calibration')
    plt.xlabel('LED index')
    plt.ylabel('Luminance level')
    plt.savefig( picture_directory + 'green_before_and_after.png')
    print('green info')
    print(led_calibrator.g_iref_values)
    print(g_raw_stats.rgbvalues)
    print(g_iref_stats.rgbvalues)
    ##Red
    RunShellOnChirp(all_red_no_iref_filename)
    all_red_iref_img = GetPictureReliably()
    RunShellOnChirp(all_dark_no_iref_filename)
    all_red_iref_ds_img = cv.addWeighted(all_red_iref_img, 1.0, \
                                        all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_red_with_iref_cal.png', all_red_iref_ds_img)
    r_iref_stats = DotStats(all_red_iref_ds_img)
    r_iref_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    r_iref_stats.AnalyzeDots()
    if printcheckinfo:
        print('check red iref calibrated stats:')
    if not led_calibrator.CheckBrightnessRatio(r_iref_stats, \
        ratio_thres = ratio_thres_calibrated, \
        echomessages = printcheckinfo):
        quit()
    #plot red variation
    plt.figure(figsize = (12,8), dpi = 100)
    plt.plot(r_raw_stats.luminancevalues, 'ro', markersize = 20, label = 'Before IREF Calibration')
    plt.plot(r_iref_stats.luminancevalues, 'gs', markersize = 20, label = 'After IREF Calibration')
    plt.legend()
    plt.title('red LEDs luminance level before and after IREF calibration')
    plt.xlabel('LED index')
    plt.ylabel('Luminance level')
    plt.savefig(picture_directory + 'red_before_and_after.png')
    print('red info')
    print(led_calibrator.r_iref_values)
    print(r_raw_stats.rgbvalues)
    print(r_iref_stats.rgbvalues)    
    ##blue
    RunShellOnChirp(all_blue_no_iref_filename)
    all_blue_iref_img = GetPictureReliably()
    RunShellOnChirp(all_dark_no_iref_filename)
    all_blue_iref_ds_img = cv.addWeighted(all_blue_iref_img, 1.0, \
                                        all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_blue_with_iref_cal.png', all_blue_iref_ds_img)
    b_iref_stats = DotStats(all_blue_iref_ds_img)
    b_iref_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    b_iref_stats.AnalyzeDots()
    if printcheckinfo:
        print('check blue iref calibrated stats:')
    if not led_calibrator.CheckBrightnessRatio(b_iref_stats, \
        ratio_thres = ratio_thres_calibrated, \
        echomessages = printcheckinfo):
        quit()
    #plot blue variation
    plt.figure(figsize = (12,8), dpi = 100)
    plt.plot(b_raw_stats.luminancevalues, 'ro', markersize = 20, label = 'Before IREF Calibration')
    plt.plot(b_iref_stats.luminancevalues, 'gs', markersize = 20, label = 'After IREF Calibration')
    plt.legend()
    plt.title('blue LEDs luminance level before and after IREF calibration')
    plt.xlabel('LED index')
    plt.ylabel('Luminance level')
    plt.savefig(picture_directory + 'blue_before_and_after.png')
    print('blue info')
    print(led_calibrator.b_iref_values)
    print(b_raw_stats.rgbvalues)
    print(b_iref_stats.rgbvalues)
    ##color ratio scatter plot
    RunShellOnChirp(all_on_no_iref_filename)
    all_on_iref_img = GetPictureReliably()
    RunShellOnChirp(all_dark_no_iref_filename)
    all_on_iref_ds_img = cv.addWeighted(all_on_iref_img, 1.0, \
                                        all_dark_img, -1.0, 0.0)
    cv.imwrite(picture_directory + 'all_on_with_iref_cal.png', all_on_iref_ds_img)

    all_on_iref_stats = DotStats(all_on_iref_ds_img)
    all_on_iref_stats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
    all_on_iref_stats.AnalyzeDots()
    if printcheckinfo:
        print('check blue iref calibrated stats:')
    if not led_calibrator.CheckBrightnessRatio(all_on_iref_stats, \
        ratio_thres = ratio_thres_calibrated, \
        echomessages = printcheckinfo):
        quit()
    #plot color ratio scatter plot
    aftercal_x = np.zeros(12)
    aftercal_y = np.zeros(12)
    beforecal_x = np.zeros(12)
    beforecal_y = np.zeros(12)
    for i in range(12):
        beforecal_x[i] = w_stats.rgbvalues[i,0]/w_stats.rgbvalues[i,1]
        beforecal_y[i] = w_stats.rgbvalues[i,2]/w_stats.rgbvalues[i,1]
        aftercal_x[i] = all_on_iref_stats.rgbvalues[i,0]/all_on_iref_stats.rgbvalues[i,1]
        aftercal_y[i] = all_on_iref_stats.rgbvalues[i,2]/all_on_iref_stats.rgbvalues[i,1]
    plt.figure(figsize = (12,8), dpi = 100)
    plt.plot(beforecal_x, beforecal_y, 'ro', markersize = 8, label = 'Before IREF Calibration')
    plt.plot(aftercal_x, aftercal_y, 'gs', markersize = 8, label = 'After IREF Calibration')
    plt.legend()
    plt.title('color coordinates before and after IREF calibration')
    plt.xlabel('R/G')
    plt.ylabel('B/G')
    plt.savefig(picture_directory + 'colorscatter_iref.png')
    

    
#__de-init__
RunShellOnChirp(all_dark_filename)
ReleaseCamera()
