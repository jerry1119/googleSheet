#Golden Chirp Step 1: Calibrate Iref Values, write Iref value file into Chirp
#Golden Chirp Step 2: Measure LED primaries color coordinates with spectrometer
#Golden Chirp Step 3: verify transformed sRGB coordinates
#Note that Golden Chirps actually have a little residue color un-uniformity
#which is intentional
#This file is Step 3:
#Calculate the universal CCM and load CCM. 
#Then display sRGB primaries one by one again, to take measurements
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
led_cal = ChirpLEDCalibrator()
#Initialize Golden Chirp
led_cal.RunShellOnChirp(led_cal.mode11_filename)#Mode 11
led_cal.LoadCCMfromCoords()

###Red
led_cal.DispCalibratedUniform([255,0,0])
print('sRGB Red, please measure color coordinates')
red_xval = float(input('X value of Red LED?\n'))
red_yval = float(input('Y value of Red LED?\n'))
red_zval = float(input('Z value of Red LED?\n'))
###Green
led_cal.DispCalibratedUniform([0, 255, 0])
print('sRGB Green, please measure color coordinates')
green_xval = float(input('X value of Green LED?\n'))
green_yval = float(input('Y value of Green LED?\n'))
green_zval = float(input('Z value of Green LED?\n'))
###Blue
led_cal.DispCalibratedUniform([0, 0, 255])
print('sRGB blue, please measure color coordinates')
blue_xval = float(input('X value of Blue LED?\n'))
blue_yval = float(input('Y value of Blue LED?\n'))
blue_zval = float(input('Z value of Blue LED?\n'))
#write to file
step3_filepath = picture_directory + led_cal.gc_step3_filename
print('Golden Chirp Step 3 file being written to: ' + step3_filepath)
with open(step3_filepath, 'w') as f:
    f.write( 'Golden Chirp step 3 file\n')
    f.write( 'Each line is XYZ of corrected sRGB primary coordinates\n')
    f.write( 'This file is intended for human consumption only\n' )
    f.write( '%.5e %.5e %.5e\n' % (red_xval, red_yval, red_zval))
    f.write( '%.5e %.5e %.5e\n' % (green_xval, green_yval, green_zval))
    f.write( '%.5e %.5e %.5e\n' % (blue_xval, blue_yval, blue_zval))
    f.write( 'measu R xy: %.3f %.3f\n' % (red_xval/(red_xval+red_yval+red_zval), \
                                  red_yval/(red_xval+red_yval+red_zval)) )
    f.write( 'ideal R xy: %.3f %.3f\n' % (0.64, 0.33))
    f.write( 'measu G xy: %.3f %.3f\n' % (green_xval/(green_xval+green_yval+green_zval), \
                                  green_yval/(green_xval+green_yval+green_zval)) )
    f.write( 'ideal G xy: %.3f %.3f\n' % (0.3, 0.6))
    f.write( 'measu B xy: %.3f %.3f\n' % (blue_xval/(blue_xval+blue_yval+blue_zval), \
                                  blue_yval/(blue_xval+blue_yval+blue_zval)) )
    f.write( 'ideal B xy: %.3f %.3f\n' % (0.15, 0.06)) 
    f.write( 'rg ratio measu %.3f\n' % (red_yval/green_yval))
    f.write( 'rg ratio ideal %.3f\n' % (0.297))  
    f.write( 'bg ratio measu %.3f\n' % (blue_yval/green_yval))
    f.write( 'bg ratio ideal %.3f\n' % (0.101))
#Turn off LEDs
RunShellOnChirp(all_dark_filename)


