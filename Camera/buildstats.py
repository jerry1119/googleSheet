exec(open('./conveniencefuncs.py').read())
foldername= 'd:\\P3_images\\'
listofdirs = next(os.walk(foldername))[1]
num_dirs = len(listofdirs)
led_ratios = np.zeros(num_dirs)
for i in range(num_dirs):
    current_dir = listofdirs[i]
    print(current_dir)
    all_dark_filename = foldername + current_dir + '\\' + current_dir + '_All_Dark.bmp'
    all_white_filename = foldername + current_dir + '\\' + current_dir + '_All_White.bmp'
    all_dark_img = cv.imread(all_dark_filename)
    all_white_img = cv.imread(all_white_filename)
    all_white_ds_img = cv.addWeighted(all_white_img, 1.0, all_dark_img, -1.0, 0.0)
    w_stats = DotStats(all_white_ds_img)
    w_stats.DetectAnalyze(expected_dot_size, False, False)
    if w_stats.num_dots == 12:
        led_ratios[i] = w_stats.GetBrightnessRatio()
    else:
        led_ratios[i] = -1.0
        print('Failure: # of Dots:' + str(w_stats.num_dots))
print(led_ratios)
print('max:')
print(np.max(led_ratios))
print('min:')
print(np.min(np.abs(led_ratios)))

