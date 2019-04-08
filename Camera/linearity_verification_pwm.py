exec(open('./conveniencefuncs.py').read())
#*************************
#start here
expected_dot_size = 2700
ret = InitializeCamera()

            
def Mode10SetBrightness(brightnessvalue, waittime = 0.3):
    hexstring = "%02x" % brightnessvalue
    command_string = 'adb shell ' + 'i2cset -f -y 0 0x15 0x3F 0x' + hexstring + ' i'
    os.system(command_string)
    command_string = 'adb shell ' + 'i2cset -f -y 0 0x17 0x3F 0x' + hexstring + ' i'
    os.system(command_string)
    time.sleep(waittime)
    
if(ret==1):
    #Turn all LEDs to 100% duty cycle, perform auto-exposure
    RunShellOnChirp(all_on_filename)
    AutoExposure()
    all_on_img = GetPictureReliably()
    RunShellOnChirp(all_dark_filename)
    time.sleep(1)
    all_dark_img = GetPictureReliably()
    all_on_ds_img = cv.addWeighted(all_on_img, 1.0, all_dark_img, -1.0, 0.0)
    w_stats = DotStats(all_on_ds_img)
    w_stats.DetectAnalyze(expected_dot_size, False, False)
    print(w_stats.dot_sizes)
    print(w_stats.rgbvalues)
    print(w_stats.coordinates)
    cv.imwrite('w_original.jpg', all_on_ds_img)
    w_stats.MaskImage()
    cv.imwrite('w_masked.jpg', all_on_ds_img)
    w_stats.AddNotation()
    cv.imwrite('w_notated.jpg', all_on_ds_img)
    dot_coordinates = w_stats.coordinates
    dot_sizes = w_stats.dot_sizes
    num_dots = w_stats.num_dots
    #######################################
    #Begin sweep
    RunShellOnChirp(mode10_filename) #enter mode10
    yvalues = np.zeros(256)
    for i in range(256):
        Mode10SetBrightness(i)
        imgdata = GetPictureReliably()
        imgdata_ds = cv.addWeighted(imgdata, 1.0, all_dark_img, -1.0, 0.0)
        with DotStats(imgdata_ds) as dstats:
            dstats.LoadDotsInfo(dot_coordinates, dot_sizes, num_dots)
            dstats.AnalyzeDots()
            yvalues[i] = np.mean(dstats.rgbvalues)
        print('input: %03d, output %.1f' % (i, yvalues[i]))
    yvalues = yvalues/np.max(yvalues)
    xvalues = np.arange(256)
    yvalues_ideal = 1.0/255.0*xvalues
    plt.plot(xvalues,yvalues, 'b', label = 'Measured TF') 
    plt.plot(xvalues, yvalues_ideal, 'r--', label = 'Ideal TF')
    plt.legend( loc = 'upper left' )
    plt.title('LED transfer function')
    plt.xlabel('8 bit input in decimal')
    plt.ylabel('output normalized to 1.0')
    plt.show()
    PT_FreezeCapture()

    
"""    SaveBmpReliably('./ChirpLEDPictures/all_on.bmp')
    RunShellOnChirp(all_dark_filename)
    time.sleep(1)
    SaveBmpReliably('./ChirpLEDPictures/all_dark.bmp')
    
    dark_img = GetPictureReliably()
    RunShellOnChirp(four_dots_filename)

    #Verify linearity
    RunShellOnChirp(mode10_filename)
    yvalues = np.zeros(256)
    for i in range(256):
        hexstring = "%02x" % i
        command_string = 'adb shell ' + 'i2cset -f -y 0 0x15 0x3F 0x' + hexstring + ' i'
        os.system(command_string)
        command_string = 'adb shell ' + 'i2cset -f -y 0 0x17 0x3F 0x' + hexstring + ' i'
        os.system(command_string)
        yvalues[i] = GetMeanPixelValue()
        print('input value %d, max pixel value %03d' % (i, yvalues[i]))
    plt.plot(yvalues)
    plt.show()
"""
