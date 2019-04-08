#execfile('usage.py')
import numpy as np
import cv2 as cv
import time
import matplotlib.pyplot as plt
from GoogleCode.LEDfuncs import DotStats

all_green_filename = './pictures/Quanta/4_25/6421A00024_All_Green.bmp'
all_red_filename = './pictures/Quanta/4_25/6421A00024_All_Red.bmp'
all_blue_filename = './pictures/Quanta/4_25/6421A00024_All_Blue.bmp'
all_white_filename = './pictures/Quanta/4_25/6421A00024_All_White.bmp'

image_all_green = cv.imread(all_green_filename)
image_all_red = cv.imread(all_red_filename)
image_all_blue = cv.imread(all_blue_filename)
image_all_white = cv.imread(all_white_filename)

expected_size = 1200
cv.imwrite('w.jpg', image_all_white)
w_stats = DotStats(image_all_white)
w_stats.DetectAnalyze(expected_size, True, True)
print(w_stats.dot_sizes)
print(w_stats.rgbvalues)
print(w_stats.coordinates)
cv.imwrite('w_notated.jpg', image_all_white)
##***
cv.imwrite('r.jpg', image_all_red)
r_stats = DotStats(image_all_red)
r_stats.DetectAnalyze(expected_size, True, True)
print(r_stats.dot_sizes)
print(r_stats.rgbvalues)
print(r_stats.coordinates)
cv.imwrite('r_notated.jpg', image_all_red)
##***
cv.imwrite('g.jpg', image_all_green)
g_stats = DotStats(image_all_green)
g_stats.DetectAnalyze(expected_size, True, True)
print(g_stats.dot_sizes)
print(g_stats.rgbvalues)
print(g_stats.coordinates)
cv.imwrite('g_notated.jpg', image_all_green)
##***
cv.imwrite('b.jpg', image_all_blue)
b_stats = DotStats(image_all_blue)
b_stats.DetectAnalyze(expected_size, True, True)
print(b_stats.dot_sizes)
print(b_stats.rgbvalues)
print(b_stats.coordinates)
cv.imwrite('b_notated.jpg', image_all_blue)
##***




"""Untitled event
cv.imshow('w1', image_all_green)
cv.waitKey(0)
cv.imshow('w1', image_all_green)
cv.waitKey(0)

numpoints = 100
percentilex = np.zeros(numpoints)
valuey = np.zeros(numpoints)
percentilexmin = 98.0
percentilexmax = 100.0
incrementx = (percentilexmax-percentilexmin)*1.0/(numpoints-1)

for i in range(numpoints):
    percentilex[i] = i*incrementx + percentilexmin
    print percentilex[i] 
    valuey[i] = np.percentile(image_all_green, percentilex[i])

plt.plot(percentilex, valuey )
plt.show()
"""
"""
image_notated = np.zeros(image_all_red.shape, dtype=np.uint8)
image_notated = 1*image_all_red
stat_engine2 = DotStats(image_notated, True, True)
cv.imwrite('image1.jpg', image_notated)
stat_engine1 = DotStats(image_all_red, False, False)
cv.imwrite( 'image2.jpg', image_all_red)
print stat_engine1.rgbvalues
"""
