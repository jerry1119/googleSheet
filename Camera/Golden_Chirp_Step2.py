#Golden Chirp Step 2:
#Read and load IREF values, then display the intrinsic LED R, G, B coordinates 
#one by one
exec(open('./conveniencefuncs.py').read())
#*************************
#start here
picture_directory = '.\\pictures\\Golden_Chirps\\'
snstring = GetChirpSerialNumber()
print('device serial number: ' + snstring)
picture_directory = picture_directory + snstring + '\\'
if not os.path.isdir(picture_directory):
    os.system('mkdir ' + picture_directory)
printcheckinfo = True
#Turn all LEDs to 100% duty cycle, perform auto-exposure
RunShellOnChirp(all_on_filename)
led_cal = ChirpLEDCalibrator()
led_cal.PullReadIrefCalibrationFile()
###Red
led_cal.RunShellOnChirp(led_cal.all_red_no_iref_filename)
print('LED Red, please measure color coordinates')
red_xval = float(input('X value of Red LED?\n'))
red_yval = float(input('Y value of Red LED?\n'))
red_zval = float(input('Z value of Red LED?\n'))
###Green
led_cal.RunShellOnChirp(led_cal.all_green_no_iref_filename)
print('LED Green, please measure color coordinates')
green_xval = float(input('X value of Green LED?\n'))
green_yval = float(input('Y value of Green LED?\n'))
green_zval = float(input('Z value of Green LED?\n'))
###Blue
led_cal.RunShellOnChirp(led_cal.all_blue_no_iref_filename)
print('LED blue, please measure color coordinates')
blue_xval = float(input('X value of Blue LED?\n'))
blue_yval = float(input('Y value of Blue LED?\n'))
blue_zval = float(input('Z value of Blue LED?\n'))
#write to file

step2_filepath = picture_directory + led_cal.gc_step2_filename
print('Golden Chirp step 2 file being written to: ' + step2_filepath)
with open(step2_filepath, 'w') as f:
    f.write( '%.5e %.5e %.5e\n' % (red_xval, red_yval, red_zval))
    f.write( '%.5e %.5e %.5e\n' % (green_xval, green_yval, green_zval))
    f.write( '%.5e %.5e %.5e\n' % (blue_xval, blue_yval, blue_zval))
#push file to device
os.system('adb push ' + step2_filepath + ' /factory_setting/')
#Turn off LEDs
RunShellOnChirp(all_dark_filename)

