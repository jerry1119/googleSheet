# Copyright 2016 Google Inc. All Rights Reserved. 
"""
Classes Chirp LED detection and calibration
"""
__author__ = ('levonyoung@google.com (Levon Young)')
"""
#TODO: add return values that indicates pass/fail of each operation
#TODO: add graceful exit mechanisms
#TODO: add logging or error info dumping functions in failure cases
#TODO: Change detection/analysis sequence options and add more customization
function in DotStats to allow consistent dot location between colors
"""
import numpy as np
import cv2 as cv
import time
import sys
import os
const_subimg_half_size_ratio = 0.5
const_circle_mask_ratio = 0.35
const_mask_threshold_ratio = 0.3333

class DotStats(object):
    """
    DotStats
    Machine-vision class
    This class performs the following functions:
    * detect LED dots
    * sort LED dots according to location
    * analyze LED dots stats (R,G,B) values
    All tasks are performed at init
    This class does NOT perform any judgements or calibration tasks
    It merely detects and reports the LED Dots' stats
    """
    def __init__(self, imageinput):
        """
        Image input MUST be present during construction
        """
        self._dot_information_ready = False
        self.img = imageinput
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        pass
        
    def DetectAnalyze(self, expected_dot_area_size = 5000, addnotation = True, maskimage = True):
        """
        This funciton call all the key member functions
        It is written as a convenience feature
        """
        self.DetectDots(expected_dot_area_size)
        self.AnalyzeDots()
        if maskimage:
            self.MaskImage()
        if addnotation:
            self.AddNotation()        

    def DetectDots(self, expected_dot_area_size):
        """
        This function detects and sorts the dots
        """
        #convert into grey image
        #grey_img is the average of three channels
        #max and min pixel values are calculated
        #after gaussian blur
        #max/min pixel level is subtracted from all pixels
        #masking threshold is calculated from max/min values
        grey_img = cv.addWeighted(self.img[:,:,0], 0.33, 
                                    self.img[:,:,1], 0.34, 0)
        grey_img = cv.addWeighted(self.img[:,:,2], 0.33,
                                    grey_img, 1.0, 0)
        grey_img_blurred = cv.GaussianBlur(grey_img, (11,11), 0)
        max_pixel_level = np.max(grey_img_blurred)
        min_pixel_level = np.min(grey_img_blurred)
        #determine low brightness threshold
        #TODO validate if this method is robust on the production line
        self.min_threshold = min_pixel_level \
            + const_mask_threshold_ratio*(max_pixel_level - min_pixel_level)
        #convert grey_img into mask image
        mask_img = cv.inRange(grey_img, self.min_threshold, 255)
        #construct blob detector parameters
        self.bdparams = cv.SimpleBlobDetector_Params() 
        self.bdparams.filterByColor = False #disable color filtering,
        self.bdparams.filterByCircularity = False #disable circularity filtering
        self.bdparams.filterByConvexity = False #disable convexity filtering
        self.bdparams.filterByInertia = False #disable inertia filtering
        self.bdparams.filterByArea = True #enable filter by Area
        #set Area filter parameters
        self.bdparams.minArea = expected_dot_area_size/4
        self.bdparams.maxArea = expected_dot_area_size*4
        self.bdparams.minThreshold = self.min_threshold
        self.bdparams.maxThreshold = 255
        self.bdver = (cv.__version__).split('.')
        #instantiate blob detector
        #***********************************************
        if int(self.bdver[0]) < 3:
            self.blob_detector = cv.SimpleBlobDetector(self.bdparams)
        else:
            self.blob_detector = cv.SimpleBlobDetector_create(self.bdparams)
        #******************************************
        #detect the dots
        ###################################################
        ###################################################
        self.raw_keypoints = self.blob_detector.detect(mask_img)
        ###################################################
        ###################################################
        #some times the dot detector will detect an invalid dot with
        #nan type coordinates, those need to be filtered.
        #also the dots detected need to be sorted
        #according to geometrical locations
        #in the following section, result from dot detector is translated into
        #ordinary numpy array. 
        #coordinates are recorded into self.raw_coordinates array
        #sizes are recorded into self.raw_dot_sizes array
        #-1 is treated as invalid number, use "-1" as "invalid" mark
        self.raw_num_dots = len(self.raw_keypoints) #number of dots detected
        self.num_dots = self.raw_num_dots #number of valid dots
        self.raw_dot_sizes = np.zeros(self.raw_num_dots) #unsorted
        self.raw_coordinates = np.zeros((self.raw_num_dots, 2)) #unsorted
        self.raw_dot_valid = np.zeros(self.raw_num_dots)
        for i in range(self.raw_num_dots):
            currentkp = self.raw_keypoints[i]
            currentpoint = currentkp.pt
            currentsize = currentkp.size
            currentx = currentpoint[0]
            currenty = currentpoint[1]
            if np.isnan(currentx) \
                or np.isnan(currenty) \
                or np.isnan(currentsize):
                self.raw_coordinates[i, 0] = -1.0
                self.raw_coordinates[i, 1] = -1.0
                self.raw_dot_sizes[i] = -1.0
                self.raw_dot_valid[i] = -1.0
                self.num_dots = self.num_dots -1 #one less valid dot
            else:
                self.raw_coordinates[i,0] = currentx
                self.raw_coordinates[i,1] = currenty
                self.raw_dot_sizes[i] = currentsize
                self.raw_dot_valid[i] = 1.0
        #put valid dots into self.coordinates and self.dot_sizes
        self.dot_sizes = np.zeros(self.num_dots)
        self.coordinates = np.zeros((self.num_dots, 2))
        valid_i = 0
        for i in range(self.raw_num_dots):
            if valid_i > self.num_dots:
                break
            if self.raw_dot_valid[i] > 0:
                self.coordinates[valid_i,:] = self.raw_coordinates[i,:]
                self.dot_sizes[valid_i] = self.raw_dot_sizes[i]
                valid_i = valid_i +1
        # at this point, the following members are populated:
        # self.num_dots
        # self.coordinates
        # self.dot_sizes
        # Next step is to Sort Dots
        self.SortDots()

    def SortDots(self):
        #TODO Add error handling mechanism for cases of zero Zenith vector
        # and Zero current vectors
        # The task of this funciton is to sort the valid dots
        # according to geometrical locations
        # Sorting criteria:
        # Dots are sorted in a clock-wise fashion
        # The dot at the zenith will be the last dot
        if not hasattr(self, "num_dots"):
            return #don't do anything if DetectDots was not done
        if self.num_dots < 2:
            return #don't do anything if less than 2 dots are present
        # First, pick the center location as the "origin"
        led_x_max = np.max(self.coordinates[:,0])
        led_x_min = np.min(self.coordinates[:,0])
        led_y_max = np.max(self.coordinates[:,1])
        led_y_min = np.min(self.coordinates[:,1])
        center_x = 0.5*(led_x_max+led_x_min)
        center_y = 0.5*(led_y_max+led_y_min)
        self.center_point = (center_x, center_y)
        # Find the Zenith dot (LED #12 if all LEDs are functional)
        # and caluclate zenith vector (vector from center to zenith dot)
        # note Y axis is pointing downward in numpy array
        zenith_index = np.argmin(self.coordinates[:,1])
        zenith_x = self.coordinates[zenith_index,0]
        zenith_y = self.coordinates[zenith_index,1]
        zenith_vector = ((zenith_x - center_x), (center_y - zenith_y))
        zenith_vector = np.array(zenith_vector)
        zenith_unit_vector = zenith_vector/np.linalg.norm(zenith_vector)
        east_unit_vector = (zenith_unit_vector[1], -1.0*zenith_unit_vector[0])
        east_unit_vector = np.array(east_unit_vector)      
        # Calculate the angle of each valid dot, compared to Zenith dot
        self.angles = np.zeros(self.num_dots)
        for i in range(self.num_dots):
            current_x = self.coordinates[i,0]
            current_y = self.coordinates[i,1]
            current_vector = ((current_x - center_x),(center_y - current_y))
            current_vector = np.array(current_vector)
            current_unit_vector = current_vector/np.linalg.norm(current_vector)
            if i == zenith_index:
                self.angles[i] = 2*np.pi
            else:
                cosval1 = np.dot(zenith_unit_vector, current_unit_vector)
                cosval1 = np.clip(cosval1, -1.0, 1.0)
                cosval2 = np.dot(east_unit_vector, current_unit_vector)
                if cosval2 > 0.0:
                    self.angles[i] = np.arccos(cosval1)
                else:
                    self.angles[i] = 2*np.pi - np.arccos(cosval1)
        # Sort dots according to angles
        sortindex = np.argsort(self.angles)
        self.angles = self.angles[sortindex]
        self.coordinates = self.coordinates[sortindex]
        self.dot_sizes = self.dot_sizes[sortindex]
        self._dot_information_ready = True #mark self as "ready"
        
    def IsReady(self):
        return self._dot_information_ready
            
    def AnalyzeDots(self):
        #TODO: check if the masks will fall out of range, if so, throw error info
        #this means the lens is zoomed in too much and 
        #needs to be zoomed out to have more iamge margin
        # The task of this function is to extract average RGB values for each dot
        if self.IsReady():
            subimgmasksizes = self.GetSubImgMaskSize()
            subimg_half_size = subimgmasksizes[0]
            subimg_size = subimgmasksizes[1]
            circle_mask_size = subimgmasksizes[2]
            subimg_center = (subimg_half_size, subimg_half_size)
            circle_mask = np.zeros((subimg_size, subimg_size, 3), np.uint8)
            cv.circle(circle_mask, 
                    subimg_center, 
                    circle_mask_size, #size of the mask circle
                    [255,255,255], #0xFFFFFF
                    thickness = -1)
            circle_area = np.pi*circle_mask_size**2
            self.rgbvalues = np.zeros((self.num_dots, 3))
            self.luminancevalues = np.zeros(self.num_dots)
            for i in range(self.num_dots):
                current_x = np.int(np.round(self.coordinates[i,0]))
                current_y = np.int(np.round(self.coordinates[i,1]))
                current_point = (current_x, current_y)
                current_size = np.int(np.round(self.dot_sizes[i]))
                #crop the sub image containing the dot
                xl = current_x - subimg_half_size
                xr = current_x + subimg_half_size
                yu = current_y - subimg_half_size
                yd = current_y + subimg_half_size
                subimage = self.img[yu:(yd+1), xl:(xr+1)] 
                #note x and y are reversed
                #mask the sub image
                subimage = cv.bitwise_and(subimage, circle_mask)
                #calculate and store RGB values
                cr = np.sum(subimage[:,:,2])/circle_area
                cg = np.sum(subimage[:,:,1])/circle_area
                cb = np.sum(subimage[:,:,0])/circle_area
                self.rgbvalues[i,:] = [ cr, cg, cb]
                self.luminancevalues[i] = cr + cg + cb

    def LoadDotsInfo(self, coordinates, dot_sizes, num_dots, need_to_sort = False):
        """
        Load a given set of dot information. 
        Args:
        coordinates: coordinates of LED dots
        dot_sizes : dot sizes of LED dots
        num_dots: number of dots
        need_to_sort : if True, input argument values are not sorted, 
        need to call self.SortDots()
        """
        self.coordinates = np.array(coordinates)
        self.dot_sizes = np.array(dot_sizes)
        self.num_dots = np.int(num_dots)
        if need_to_sort:
            self.SortDots()
        self._dot_information_ready = True
        
    def GetSubImgMaskSize(self):
        """
        Centralized support function for managing sub image size, 
        sub image half size and mask size
        sub image size is used in multiple places, centralize the algorithm
        for determining subimage size here to ensure consistency in 
        sub-image sizing among different functions
        return value: np array:
        subimg_half_size, subimg_size, circle_mask_size
        """
        if self.IsReady():
            #*****************************************************
            #*****************************************************
            #Two key parameters that may need adjustments for different platforms:
            #subimg_size : size of the square sub-img
            #circle_mask_size : size of the circle-shaped mask
            #*****************************************************
            #*****************************************************
            max_dot_size = np.max(self.dot_sizes) 
            min_dot_size = np.min(self.dot_sizes)  
            subimg_half_size = np.int(
                np.round(max_dot_size*const_subimg_half_size_ratio))
            #sub image size
            subimg_size = subimg_half_size*2+1 
            #size of the mask circle
            circle_mask_size = np.int(
                np.floor(min_dot_size*const_circle_mask_ratio))
            return np.array([subimg_half_size, subimg_size, circle_mask_size])
        else:
            return np.array([0,0,0])
            
    def AddNotation(self):
        """
        Add notation to the image.
        """
        if self.IsReady():
            subimgmasksizes = self.GetSubImgMaskSize()
            subimg_half_size = subimgmasksizes[0]
            subimg_size = subimgmasksizes[1]
            circle_mask_size = subimgmasksizes[2]
            subimg_center = (subimg_half_size, subimg_half_size)
            text_font = cv.FONT_HERSHEY_COMPLEX
            notation_color = [255,255,255]
            for i in range(self.num_dots):
                current_x = np.int(np.round(self.coordinates[i,0]))
                current_y = np.int(np.round(self.coordinates[i,1]))
                current_point = (current_x, current_y)
                pt1 = (current_x - subimg_half_size , current_y - subimg_half_size)
                pt2 = (current_x + subimg_half_size , current_y + subimg_half_size)
                cv.rectangle(self.img, pt1, pt2, color = notation_color, thickness = 2)
                cv.circle(self.img, current_point, 
                    circle_mask_size, notation_color, thickness = 1)
                cv.putText(self.img, str(i+1), current_point, text_font, 0.6, notation_color)        
        
    def MaskImage(self):
        """
        Mask the image, for monitoring and debugging purposes
        After masking, the areas used for dots' rgb calculation are kept
        while the immediate-surrounding areas will be masked to be 
        pure dark (0,0,0)
        """
        if self.IsReady():
            subimgmasksizes = self.GetSubImgMaskSize()
            subimg_half_size = subimgmasksizes[0]
            subimg_size = subimgmasksizes[1]
            circle_mask_size = subimgmasksizes[2]
            subimg_center = (subimg_half_size, subimg_half_size)
            circle_mask = np.zeros((subimg_size, subimg_size, 3), np.uint8)
            cv.circle(circle_mask, 
                    subimg_center, 
                    circle_mask_size, #size of the mask circle
                    [255,255,255], #0xFFFFFF
                    thickness = -1)
            for i in range(self.num_dots):
                current_x = np.int(np.round(self.coordinates[i,0]))
                current_y = np.int(np.round(self.coordinates[i,1]))
                current_point = (current_x, current_y)
                current_size = np.int(np.round(self.dot_sizes[i]))
                #crop the sub image containing the dot
                xl = current_x - subimg_half_size
                xr = current_x + subimg_half_size
                yu = current_y - subimg_half_size
                yd = current_y + subimg_half_size
                subimage = self.img[yu:(yd+1), xl:(xr+1)] #note x and y are reversed
                #mask the sub image
                subimage = cv.bitwise_and(subimage, circle_mask)
                #copy the masked sub image back to the image
                self.img[yu:(yd+1), xl:(xr+1)] = subimage
                
    def GetMeanRGB(self):
        """
        Return the average rgb values of the analyzed dots. 
        """
        rvalue = np.mean(self.rgbvalues[:,0])
        gvalue = np.mean(self.rgbvalues[:,1])
        bvalue = np.mean(self.rgbvalues[:,2])
        return np.array([rvalue,gvalue,bvalue])
        
    def GetBrightnessVariation(self):
        """
        Return the std/mean of brightness values
        Brightness values defined as r+g+b, equal weighting for now
        #TODO add different weighting to r,g,b according to spectrometer measurement
        """
        brightness_vals = np.zeros(self.num_dots)
        brightness_vals = self.rgbvalues[:,0] + self.rgbvalues[:,1] + self.rgbvalues[:,2]
        brightness_mean = np.mean(brightness_vals)
        brightness_var = np.std(brightness_vals)
        return brightness_var/brightness_mean
        
    def GetBrightnessRatio(self):
        """
        Get min/max ratio, it is duplicate function, leave it for now
        #TODO, merge with the one in led calibrator class
        """
        brightness_vals = np.zeros(self.num_dots)
        brightness_vals = self.rgbvalues[:,0] + self.rgbvalues[:,1] + self.rgbvalues[:,2]
        brightness_min = np.min(brightness_vals)
        brightness_max = np.max(brightness_vals)
        return brightness_min/brightness_max

"""Colorimetry master class
""" 
class ColorConverter(object):
    """class for color converter"""

    
    def GetsRGBPrimaries(self):
        return self._srgb_primaries_xyz

    def __init__(self):
        self._srgb_primaries_xyz = np.array([ 
        [0.412315151515, 0.2126000000, 0.019327272727],
        [0.357600000000, 0.7152000000, 0.119200000000],
        [0.180500000000, 0.0722000000, 0.950633333333],
        ]) #_srgb_primaries_xyz is 3x3 matrix,
        # each row is XYZ coordinates of R,G,B primaries
        self._xyz2srgb_matrix = np.linalg.inv(self._srgb_primaries_xyz.transpose())

    def NormalizeColorSpace(self, primaries, furtherdim = 1.0):
        """normalized a color space,
        It will be normalized so that Sum(Y) = 1.0
        note that the input itself will be changed"""
        sumy = primaries[0,1]+primaries[1,1]+primaries[2,1]
        primaries = primaries/sumy*furtherdim
        return primaries
        
    def sRGBdegamma(self, code, fullscale = 255.0):
        """
        Note that input and output are using the same fullscale
        e.g. if input is 0-255.0, then output is also 0-255.0
        """
        sRGBs = 1.0*code/fullscale #scaled value for sRGB
        sRGBlins = 0.0 #scaled linear value for sRGB
        if sRGBs <= 0.04045:
            sRGBlins = sRGBs/12.92
        else:
            sRGBlins = ((sRGBs+0.055)/1.055)**2.4
        lincode = sRGBlins*fullscale
        return lincode
        
    def sRGBgamma(self, slin, fullscale = 255.0):
        """ add gamma to a scaled, linear input, range (0-1)"""
        slininput = np.clip(slin, 0.0, 1.0) #clip input to 0-1
        sRGBs = 0.0 #scaled sRGB value
        if slininput <= 0.0031308:
            sRGBs = 12.92*slininput
        else:
            sRGBs = 1.055*slininput**(1.0/2.4) - 0.055
        sRGBcode = sRGBs*fullscale
        return sRGBcode
        
    def sRGB2XYZ(self, rcode, gcode, bcode, fullscale = 255.0):
        """ inputs: code representation of sRGB value
        outputs: scaled XYZ values, at full RGB, Y = 1.0"""
        rlincode = self.sRGBdegamma(rcode, fullscale)
        glincode = self.sRGBdegamma(gcode, fullscale)
        blincode = self.sRGBdegamma(bcode, fullscale)
        rgbslin = 1.0/fullscale*np.array([
            rlincode,
            glincode,
            blincode,
            ])
        xyz = np.dot( (self._srgb_primaries_xyz.transpose()) , rgbslin)
        return xyz
        
    def sRGBHex2XYZ(self, sRGB_Hex_String):
        """convert from hex string sRGB to XYZ values
        Note that in Hex format, 8bit/channel is assumed
        """
        rcode = int(sRGB_Hex_String[0:2],16)
        gcode = int(sRGB_Hex_String[2:4],16)
        bcode = int(sRGB_Hex_String[4:6],16)
        return self.sRGB2XYZ(rcode,gcode,bcode,255.0)
        
    def XYZ2sRGBlin(self, xval, yval, zval):
        """ inputs: scaled XYZ values, scaled to Y = 1.0 at full scale
        outputs: RGB linear values code in sRGB color space"""
        xyzmatrix = np.matrix([
            xval,
            yval,
            zval])
        xyzmatrix = xyzmatrix.transpose()
        sRGBslinvals = np.dot( self._xyz2srgb_matrix, xyzmatrix)
        return sRGBslinvals
    
    def XYZ2sRGBcode(self, xval, yval, zval, fullscale = 255.0):
        """ inputs: scaled XYZ values, scaled to Y = 1.0 at full scale
        outputs: RGB code"""
        sRGBslinvals = self.XYZ2sRGBlin(xval,yval,zval)
        sRGBcode = np.array([
            0.0,
            0.0,
            0.0])
        sRGBcode[0] = self.sRGBgamma(np.double(sRGBslinvals[0]), fullscale)
        sRGBcode[1] = self.sRGBgamma(np.double(sRGBslinvals[1]), fullscale)
        sRGBcode[2] = self.sRGBgamma(np.double(sRGBslinvals[2]), fullscale)
        return sRGBcode
        
    def XYZ2Arb(self, xval, yval, zval, arb_cs):
        """ inputs: scaled xyz values, scaled to Y = 1.0 at full scale. 
        arb_cs: arbitrary color space, specified as the color primaries. 
        The format is an np array or matrix, consistent with the format of
        _srgb_primaries_xyz:
        dimensions: 3x3
        Line 1, 3 numbers: X,Y,Z of the R primary
        Line 2, 3 numbers: X,Y,Z of the G primary 
        Line 3, 3 numbers: X,Y,Z of the B primary
        The primaries' coordinates should be arranged so that sum of Y of 
        the primaries should = 1.00
        return value: RGB values in the new colorspace
        Note that the RGB values are linear, scaled to 1.0"""
        #normalize the arbitrary color space so that sum(Y) = 1.00
        #sumy = arb_cs[0,1] + arb_cs[1,1] + arb_cs[2,1]
        #arb_cs_n = arb_cs * (1/sumy) #normalized arbitrary color space
        arb_cs_n = arb_cs
        #calculate the color conversion matrix
        convmatrix = np.linalg.inv(arb_cs_n.transpose())
        #calculate the rgb value and return
        xyzvalues = np.array([
            xval,
            yval,
            zval])
        xyzvalues = xyzvalues.transpose()
        rgbval = np.dot(convmatrix, xyzvalues)
        return rgbval
        
    def sRGB2Arb(self, rcode, gcode, bcode, arb_cs, fullscale = 255.0):
        """ function to convert sRGB value into linear Arbitrary color space
        inputs: rcode, gcode and bcode: RGB code in sRGB colorspace, with gamma
        arb_cs: arbitrary color space, specified as the color primaries. 
        The format is an np array or matrix, consistent with the format of
        _srgb_primaries_xyz:
        dimensions: 3x3
        Line 1, 3 numbers: X,Y,Z of the R primary
        Line 2, 3 numbers: X,Y,Z of the G primary 
        Line 3, 3 numbers: X,Y,Z of the B primary
        The primaries' coordinates should be arranged so that sum of Y of 
        the primaries should = 1.00 
        output is scaled to 0.0-1.0 when the primaries are scaled"""
        #convert from sRGB to XYZ
        xyzval = self.sRGB2XYZ(rcode, gcode, bcode, fullscale)
        #convert from XYZ to Arbitrary color space
        return self.XYZ2Arb(xyzval[0], xyzval[1], xyzval[2], arb_cs)
        
    def sRGBHex2Arb(self, srgb_hex_string, arb_cs, fullscale = 255.0, degamma = True):
        """function to convert sRGB value in hex string to arbitrary colorspace
        it is simply a call to sRGB2Arb function, preceded by the hex to int conversion
        """
        if fullscale > 255.0:
            print("ColorConverter::sRGBHex2Arb  fullscale not correct, defaulting to 255.0")
            fullscale = 255.0
        rcode = int(srgb_hex_string[0:2],16)
        gcode = int(srgb_hex_string[2:4],16)
        bcode = int(srgb_hex_string[4:6],16)
        #print "ColorConverter::sRGBHex2Arb input %s output %03d %03d %03d" % (srgb_hex_string, rcode, gcode, bcode)
        #return self.sRGB2Arb(rcode, gcode, bcode, arb_cs, fullscale)
        #rewrite, to emulate production line algorithm
        #Generate the conversion matrix (note that in the demo code, the matrix is generated for every conversion
        #this is inefficient but sufficient for demo / production line purposes, makes the code more straightforward. 
        #To generate the conversion matrix, invert of LED color space is mutiplied with sRGB coordinates, see doc for details
        conversionmatrix = np.dot(np.linalg.inv(arb_cs.transpose()), self._srgb_primaries_xyz.transpose())
        if debugmessage:
            print("ColorConverter::sRGBHex2Arb conversionmatrix before scaling")
            print(conversionmatrix)
        #regulate the conversion matrix to prevent overflow
        linemaxx = np.zeros(3)
        for yi in range(3):
            for xi in range(3):
                if conversionmatrix[yi,xi] > 0.0:
                    linemaxx[yi] = linemaxx[yi] + conversionmatrix[yi,xi]
        scalingfactor = np.max(linemaxx)
        conversionmatrix = conversionmatrix/scalingfactor
        if debugmessage:
            print("linemaxx")
            print(linemaxx)
            print("scalingfactor : %.3f" % scalingfactor)
            print("conversionmatrix after scaling")
            print(conversionmatrix)
        #Step 1: De-gamma, convert non linear value to linear value
        if degamma:
            rlincode = self.sRGBdegamma(rcode, fullscale)
            glincode = self.sRGBdegamma(gcode, fullscale)
            blincode = self.sRGBdegamma(bcode, fullscale)
        else:
            rlincode = rcode
            glincode = gcode
            blincode = bcode
        #Step 2: multiply by the conversion matrix. 
        srgb_lin = np.array([
            rlincode,
            glincode,
            blincode])
        srgb_lin = srgb_lin.transpose()
        rgbout = np.dot(conversionmatrix, srgb_lin)
        #step 3: output range clip, print out warning and debug message when clipping happens
        """<0 clip is not considerred to be an algorithm defect, it is simply color space boundary mismatch
        which doesn't affect functionality much. >255 clip is considered to be an algorithm defect, since it shouldn't happen"""
        if (np.max(rgbout)) > fullscale or (np.min(rgbout) < 0.0):
            print("ColorConverter::sRGBHex2Arb output out of range")
            print("conversion matrix:")
            print(conversionmatrix)
            print("input %sH  %03d %03d %03d" % (srgb_hex_string, rcode, gcode, bcode))
            print("output: %03d %03d %03d" % (rgbout[0], rgbout[1], rgbout[2]))
            rgbout = np.clip(rgbout, 0.0, fullscale)
        if debugmessage:
            print("input %sH  %03d %03d %03d" % (srgb_hex_string, rcode, gcode, bcode))
            print("output is: %03d %03d %03d" % (rgbout[0], rgbout[1], rgbout[2]))
        return rgbout
  
    def XYZ2xy(self, XYZ):
        Xval = XYZ[0]
        Yval = XYZ[1]
        Zval = XYZ[2]
        x = Xval/(Xval+Yval+Zval)
        y = Yval/(Xval+Yval+Zval)
        return (x,y) #return a tuple here

class ChirpLEDCalibrator(object):
    """
    Chirp LED Calibrator
    
    """
    def __init__( self ):
        self.cc = ColorConverter()
        self.NumLEDs = 12
        #I2C address look up tables
        #colorindex 0: red, 1: green, 2: blue
        self.dev_addresses = [
        # R   ,  G   ,  B  
        '0x17','0x17','0x17', #LED 1, index 0
        '0x17','0x17','0x17', #LED 2, index 1
        '0x15','0x15','0x15', #LED 3, index 2
        '0x15','0x15','0x15', #LED 4, index 3
        '0x15','0x15','0x15', #LED 5, index 4
        '0x15','0x15','0x15', #LED 6, index 5
        '0x15','0x15','0x15', #LED 7, index 6
        '0x15','0x15','0x15', #LED 8, index 7
        '0x17','0x17','0x17', #LED 9, index 8
        '0x17','0x17','0x17', #LED 10, index 9
        '0x17','0x17','0x17', #LED 11, index 10
        '0x17','0x17','0x17', #LED 12, index 11
        ]
        self.pwm_addresses = [
        # R   ,  G   ,  B   
        '0x0E','0x0F','0x0D', #LED1, index 0
        '0x0A','0x0B','0x0C', #LED2, index 1
        '0x19','0x1A','0x1B', #LED3, index 2
        '0x18','0x17','0x16', #LED4, index 3
        '0x13','0x14','0x15', #LED5, index 4
        '0x10','0x11','0x12', #LED6, index 5
        '0x0D','0x0E','0x0F', #LED7, index 6
        '0x0A','0x0B','0x0C', #LED8, index 7
        '0x12','0x10','0x11', #LED9, index 8
        '0x13','0x15','0x14', #LED10, index 9
        '0x1A','0x1B','0x19', #LED11, index 10
        '0x17','0x18','0x16', #LED12, index 11
        ]
        self.iref_addresses = [
        # R   ,  G   ,  B
        '0x26','0x27','0x25', #LED1, index 0
        '0x22','0x23','0x24', #LED2, index 1
        '0x31','0x32','0x33', #LED3, index 2
        '0x30','0x2F','0x2E', #LED4, index 3
        '0x2B','0x2C','0x2D', #LED5, index 4
        '0x28','0x29','0x2A', #LED6, index 5
        '0x25','0x26','0x27', #LED7, index 6
        '0x22','0x23','0x24', #LED8, index 7
        '0x2A','0x28','0x29', #LED9, index 8
        '0x2B','0x2D','0x2C', #LED10, index 9
        '0x32','0x33','0x31', #LED11, index 10
        '0x2F','0x30','0x2E', #LED12, index 11
        ]
        #IREF non-linearity compensation table
        iref_lut_filename = './GoogleCode/iref_agg.txt' 
        iref_lut = np.genfromtxt(iref_lut_filename, delimiter = ' ')
        self.led_iref_in = iref_lut[:,0]/255.0
        self.led_iref_out = iref_lut[:,1]/255.0
        self.gc_step1_filename = 'gc_step1_iref_cal.txt'
        self.gc_step2_filename = 'gc_step2_led_coord.txt'
        self.gc_step3_filename = 'gc_step3_srgb_coord.txt'
        self.camera_cal_ini_filename = 'camera_cal.ini'
        self.box_calibration_filename = 'camera_cal.ini'
        self.all_on_filename = './GoogleCode/all_on.sh'
        self.all_on_no_iref_filename = './GoogleCode/all_on_no_iref.sh'
        self.all_green_filename = './GoogleCode/all_green.sh'
        self.all_green_no_iref_filename = './GoogleCode/all_green_no_iref.sh'
        self.all_blue_filename = './GoogleCode/all_blue.sh'
        self.all_blue_no_iref_filename = './GoogleCode/all_blue_no_iref.sh'
        self.all_red_filename = './GoogleCode/all_red.sh'
        self.all_red_no_iref_filename = './GoogleCode/all_red_no_iref.sh'
        self.all_dark_filename = './GoogleCode/all_dark.sh'
        self.all_dark_no_iref_filename = './GoogleCode/all_dark_no_iref.sh'
        self.four_dots_filename = './GoogleCode/four_dots.sh'
        self.mode10_filename = './GoogleCode/mode10.sh'
        self.mode10_no_iref_filename = './GoogleCode/mode10_no_iref.sh'
        self.mode10r_filename = './GoogleCode/mode10r.sh'
        self.mode10g_filename = './GoogleCode/mode10g.sh'
        self.mode10b_filename = './GoogleCode/mode10b.sh'
        self.mode11_filename = './GoogleCode/mode11.sh'
        self.expected_dot_size = 1100
        self.raw_ratio_thres = 0.5
        self.iref_cal_ratio_thres = 0.9
        self.final_cal_ratio_thres = 0.9
        self.cdis_thres = 0.05
        self.final_cal_filename = 'ledcal.ini'
        
    def SetGlobalDimming(self, gdval):
        """
        Set global dimming value for all LEDs
        Only works in mode 11
        """
        gdval = np.int(np.clip(gdval, 0.0, 255.0))
        gdhex = '%02x' % gdval
        cmdstr = 'adb shell i2cset -f -y 0 0x17 0x08 0x' \
                 + gdhex + ' i'
        os.system(cmdstr)
        cmdstr = 'adb shell i2cset -f -y 0 0x15 0x08 0x' \
                 + gdhex + ' i'
        os.system(cmdstr)
        
    def SetGlobalIREF(self, giref):
        """
        Set global Iref values
        """
        giref = np.int(np.clip(giref, 0.0, 255.0))
        girefhex = '%02x' % giref
        cmdstr = 'adb shell i2cset -f -y 0 0x17 0x40 0x' \
                 + girefhex + ' i'
        os.system(cmdstr)
        cmdstr = 'adb shell i2cset -f -y 0 0x15 0x40 0x' \
                 + girefhex + ' i'
        os.system(cmdstr)        
        
        
    def SetLEDPWMValue(self, LEDindex, colorindex, PWMvalue):
        #Sets the PWM value for specified LED
        #LEDindex is from 0 to 11 
        #PWM is from 0 to 255
        #colorindex: 0:red, 1:green, 2:blue
        PWMvalue = np.int(np.clip(PWMvalue, 0.0, 255.0))
        PWMhex = '%02x' % PWMvalue
        cmdstr = 'adb shell i2cset -f -y 0 '\
            + self.dev_addresses[LEDindex*3 + colorindex] + ' '\
            + self.pwm_addresses[LEDindex*3 + colorindex] + ' '\
            + '0x' + PWMhex + ' i'
        os.system(cmdstr)

    def SetLEDIrefValue(self, LEDindex, colorindex, IrefValue):
        #Sets the IREF value for specified LED
        #LEDindex is from 0 to 11 
        #IrefValue is from 0 to 255
        #colorindex: 0:red, 1:green, 2:blue
        IrefValue = np.int(np.clip(IrefValue, 0.0, 255.0))
        Irefhex = '%02x' % IrefValue
        cmdstr = 'adb shell i2cset -f -y 0 '\
            + self.dev_addresses[LEDindex*3 + colorindex] + ' '\
            + self.iref_addresses[LEDindex*3 + colorindex] + ' '\
            + '0x' + Irefhex + ' i'
        os.system(cmdstr)

    def IsSameLocation( p1, p2, dth = 12.0):
        #determine if two dots are the same
        #p1 p2 are the two points
        #dth is threshold distance
        x1 = p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        d12 = ((x2-x1)**2.0 + (y2-y1)**2.0)**0.5
        if d12 <= dth:
            return True
        else:
            return False
            
    def CheckNumLEDs(self, dstats, echomessages = True):
        #Check the all on image (right after auto exposure)
        #make sure there are self.NumLEDs dots
        if dstats.num_dots != self.NumLEDs:
            if echomessages:
                print('LED # dots check failed, %d LEDs detected' \
                    % dstats.num_dots)
            return False
        else:
            if echomessages:
                print('LED # dots check pass')
            return True
            
    def CheckBrightnessRatio(self, \
        dstats, \
        ratio_thres = 0.5, \
        echomessages = True):
        #check brightness variation between LEDs
        #if brightness variation is too high, then consider it to be yield loss
        lin_brightness = dstats.rgbvalues[:,0] \
            + dstats.rgbvalues[:,1] + dstats.rgbvalues[:,2]  
        brightness_ratio = np.min(lin_brightness)/np.max(lin_brightness)
        if echomessages:
            print('brightness ratio min/max is %.3f' % brightness_ratio)
        if brightness_ratio < ratio_thres:
            if echomessages:
                print('brightness ratio check fail')
            return False
        else:
            if echomessages:
                print('brightness rtaio check pass')
            return True
    
    def CheckBrightness(self, dstats, brightness_thres):
        #check minimum brightness of individual LEDs
        #Be careful when using this, since it is a function of auto-exposure
        lin_brightness = dstats.rgbvalues[:,0] \
            + dstats.rgbvalues[:,1] + dstats.rgbvalues[:,2]  
        if np.min(lin_brightness)<brightness_thres:
            return False
        else:
            return True           
            
    def CheckFourDots(self, four_dot_stats):
        #check the four dots image to make sure there are 4 dots
        if four_dot_stats.num_dots != 4:
            return False
            
    def CheckAlignment(self, all_on_stats, four_dot_stats):
        #check alignment
        #all_on_stats is the stat engine for all on image
        #four_dot_stats is the stat engine for four dot image
        ret = True
        for i in range(4):
            p1 = all_on_stats.coordinates[3*i+2,:]
            p2 = four_dots_stats.coordinates[i, :]
            if not IsSameLocation(p1,p2):
                ret = False
        return ret
        
    def _IrefValueMap(self, linear_ratio):
        #map the IREF values to compensate for non_linearity
        #this is a function that is only used internally to this class
        mapped_ratio = np.interp( linear_ratio, \
                                  self.led_iref_out, \
                                  self.led_iref_in )
        return mapped_ratio
        
    def CalculateIrefValuesSingleColor(self, dstats):
        #Calculate the iref register values needed to compensate for 
        #brightness variation in a single color channel
        #Input: dstats: DotStats engine instance of the given color channel
        #output: iref register values, np.int data type, range 0-255
        current_ratio = 0.0
        iref_values = np.zeros(self.NumLEDs)
        lin_brightness = dstats.rgbvalues[:,0] \
            + dstats.rgbvalues[:,1] + dstats.rgbvalues[:,2]
        min_brightness = np.min(lin_brightness)
        for i in range(self.NumLEDs):
            current_ratio = min_brightness/lin_brightness[i]
            current_ratio = self._IrefValueMap(current_ratio)
            iref_values[i] = current_ratio*255.0
            iref_values[i] = np.int(np.clip(iref_values[i], 0.0, 255.0))
        return iref_values
        
    def CalculateIrefValues(self, r_stats, g_stats, b_stats):
        """
        Calculate and store Iref Values as members
        input: 
        r_stats, g_stats, b_stats:
        DotStats instances for r,g,b at 100% duty cycel and 0xFF Iref settings
        output: 
        no explicit return values
        self.r_iref_values, self.g_iref_values, self.b_iref_values are calibrated 
        Iref register values for r,g,b
        """
        self.r_iref_values = self.CalculateIrefValuesSingleColor(r_stats)
        self.g_iref_values = self.CalculateIrefValuesSingleColor(g_stats)
        self.b_iref_values = self.CalculateIrefValuesSingleColor(b_stats)
        
    def WriteIrefRegisters(self):
        """
        Write the calibrated Iref register values (calculated in 
        CalculateIrefValues function) to the Chirp unit
        input:
        No explicit input
        output:
        No explicit return values
        """
        if hasattr(self, 'r_iref_values') \
          and hasattr(self, 'g_iref_values') \
          and hasattr(self, 'b_iref_values'):
            for i in range(self.NumLEDs):
                self.SetLEDIrefValue(i, 0, self.r_iref_values[i])
                self.SetLEDIrefValue(i, 1, self.g_iref_values[i])
                self.SetLEDIrefValue(i, 2, self.b_iref_values[i])
                
    def WritePushIrefCalibrationFile(self, local_directory):
        """
        Write and push Iref Calibration file, 
        ONLY for Golden Chirps
        Do NOT use this function during normal production process 
        Input:
        filename: string containing the file name, do not include './'
        """
        with open(self.gc_step1_filename, 'w') as f:
            for i in range(self.NumLEDs):
                f.write('%d %d %d\n' % \
                    (self.r_iref_values[i], self.g_iref_values[i], self.b_iref_values[i]))
        cmdstring = 'adb push ' + self.gc_step1_filename + ' /factory_setting/'
        os.system(cmdstring)
        cmdstring = 'move ' + self.gc_step1_filename + ' ' + local_directory
        os.system(cmdstring)
        
    def PullReadIrefCalibrationFile(self):
        """
        Pull and read the Iref calibration file
        ONLY for Golden Chirps
        Do NOT use this function at during normal production process
        If step 1 file already exist, it'll get deleted... 
        so don't save any files under the running dir. 
        """
        if os.path.isfile(self.gc_step1_filename):
            cmdstring = 'del ' + self.gc_step1_filename
            os.system(cmdstring)  
        cmdstring = 'adb pull /factory_setting/' + self.gc_step1_filename
        os.system(cmdstring)
        self.r_iref_values = np.zeros(self.NumLEDs)
        self.g_iref_values = np.zeros(self.NumLEDs)
        self.b_iref_values = np.zeros(self.NumLEDs)
        with open(self.gc_step1_filename, 'r') as f:
            for i in range(self.NumLEDs):
                linestring = f.readline()
                strlist = str.split(linestring, ' ')
                self.r_iref_values[i] = int(strlist[0])
                self.g_iref_values[i] = int(strlist[1])
                self.b_iref_values[i] = int(strlist[2])
        cmdstring = 'del ' + self.gc_step1_filename
        os.system(cmdstring)
        self.WriteIrefRegisters()
        
    def LoadCCMfromCoords(self):
        """
        Load CCMs from LED coordinates
        This function is only used during Golden Chirp fabrication
        Load Iref calibration file
        Load LED coordinates, calculate and load global CCM
        Ready for sRGB color rendering (global)
        
        """
        self.PullReadIrefCalibrationFile()
        if os.path.isfile(self.gc_step2_filename):
            cmdstring = 'del ' + self.gc_step2_filename
            os.system(cmdstring)            
        cmdstring = 'adb pull /factory_setting/' + self.gc_step2_filename
        os.system(cmdstring)
        self.led_coordinates = np.zeros((3,3))
        with open(self.gc_step2_filename, 'r') as f:
            for i in range(3):
                linestring = f.readline()
                strlist = str.split(linestring, ' ')
                self.led_coordinates[i,0] = float(strlist[0])
                self.led_coordinates[i,1] = float(strlist[1])
                self.led_coordinates[i,2] = float(strlist[2])
        cmdstring = 'del ' + self.gc_step2_filename
        os.system(cmdstring)
        self.led_coordinates = self.cc.NormalizeColorSpace(self.led_coordinates)
        self.ccms = np.zeros((self.NumLEDs, 3,3))
        singleccm = np.dot( np.linalg.inv(self.led_coordinates.transpose()), \
                            self.cc.GetsRGBPrimaries().transpose())
        for i in range(self.NumLEDs):
            self.ccms[i,:,:] = singleccm
        self.NormalizeCCMs()
        
    def WriteBoxCalFile(self, r_stats, g_stats, b_stats, cam_sn_str):
        with open(self.box_calibration_filename, 'w') as f:
            f.write('!!! DO NOT EDIT !!!\n')
            f.write('Box calibration file\n')
            f.write(cam_sn_str + '\n')
            r_rgb = r_stats.GetMeanRGB()
            g_rgb = g_stats.GetMeanRGB()
            b_rgb = b_stats.GetMeanRGB()
            f.write('%.5e %.5e %.5e\n' % (r_rgb[0], r_rgb[1], r_rgb[2]))
            f.write('%.5e %.5e %.5e\n' % (g_rgb[0], g_rgb[1], g_rgb[2]))
            f.write('%.5e %.5e %.5e\n' % (b_rgb[0], b_rgb[1], b_rgb[2]))
            
            
    def NormalizeCCMs(self):
        row_positive_sums = np.zeros((self.NumLEDs, 3))
        for iled in range(self.NumLEDs):
            for i1 in range(3): 
                for i2 in range(3):
                    if self.ccms[iled,i1,i2] > 0 :
                        row_positive_sums[iled, i1] = \
                            row_positive_sums[iled, i1] \
                            + self.ccms[iled, i1, i2]
        scaling_factor = np.max(row_positive_sums)
        self.ccms = self.ccms/scaling_factor

    def DispCalibratedUniform(self, rgbvals, gdval = 255.0):
        """
        Display calibrated color
        Same color on all LEDs
        rgbvals: r,g,b values specified in 8bit int
        """
        for i in range(self.NumLEDs):
            self.DispCalibratedSingle(i, rgbvals)
        self.SetGlobalDimming(gdval)

    def DispCalibratedSingle(self, ledi, rgbvals, echomessages = True):
        """
        Display calibrated color for a single LED
        rgb vals: r,g,b values specified in 8 bit int
        We should use the function in cc, but it was implemented in a different
        way... so we explictly write down the sRGB to LED color space conversion
        within this function. And this is the only function where that 
        conversion happens during LED calibration and verification, including
        GoldenChirp cal, Box cal and DUT cal. 
        """
        srgblin = np.zeros(3)
        #Step 1: degamma
        srgblin[0] = self.cc.sRGBdegamma(rgbvals[0], 255)
        srgblin[1] = self.cc.sRGBdegamma(rgbvals[1], 255)
        srgblin[2] = self.cc.sRGBdegamma(rgbvals[2], 255)
        #Step 2: CCM multiplication
        ledrgb = np.dot(self.ccms[ledi,:,:], srgblin.transpose())
        #Step 3: render the color
        self.SetLEDPWMValue(ledi, 0, ledrgb[0])
        self.SetLEDPWMValue(ledi, 1, ledrgb[1])
        self.SetLEDPWMValue(ledi, 2, ledrgb[2])
        if echomessages:
            print('led #%02d: %03d %03d %03d' % (ledi, ledrgb[0], ledrgb[1], ledrgb[2]))

    def DispRawUniform(self, rgbvals, gdval = 255.0):
        """
        Display non-calibrated color
        same color on all LEDs
        """
        for i in range(self.NumLEDs):
            self.DispRawSingle(i, rgbvals)
        self.SetGlobalDimming(gdval)
    
    def DispRawSingle(self, ledi, rgbvals, echomessages = True):
        self.SetLEDPWMValue(ledi, 0, rgbvals[0])
        self.SetLEDPWMValue(ledi, 1, rgbvals[1])
        self.SetLEDPWMValue(ledi, 2, rgbvals[2])
        if echomessages:
            print('led #%02d: %03d %03d %03d' % (ledi, rgbvals[0], rgbvals[1], rgbvals[2]))
        
    def WriteCalibrationFile(self, file_dir):
        """
        Write and push calibration file
        file_dir is the place where you want a copy of the ledcal.ini
        """
        with open('./'+self.final_cal_filename, 'w') as f:
            for i in range(self.NumLEDs):
                for ir in range(3):
                    f.write('%.5f %.5f %.5f\n' % (self.ccms[i, ir, 0], self.ccms[i, ir, 1], self.ccms[i, ir, 2] ))
            f.write('\n')
            for i in range(self.NumLEDs):
                f.write('%d %d %d\n' % \
                    (self.r_iref_values[i], \
                     self.g_iref_values[i], \
                     self.b_iref_values[i]))
        cmdstring = 'adb push ' + self.final_cal_filename + ' /factory_setting/'
        os.system(cmdstring)
        cmdstring = 'move ' + self.final_cal_filename + ' ' + file_dir
        os.system(cmdstring)
        
                    
    def RunShellOnChirp(self, shellscript_filename, wait_time = 0.3, echocommands = False):
        with open(shellscript_filename) as f:
            for line in f:
                command_string = 'adb shell ' + line
                if echocommands:
                    print(command_string)
                os.system(command_string)
        time.sleep(wait_time)
        
    def CheckCameraSerialNumber(self, camSN, verbose = True):
        """
        check if the camera serial number camSN matches what is saved on file
        During this function, the sRGB CValues are also loaded
        If successful, return True
        If not, return False
        """
        camera_cal_filename = './' + self.camera_cal_ini_filename
        f = open(camera_cal_filename, 'r')
        linebuf = f.readline()
        linebuf = f.readline()
        ini_camera_sn_str = f.readline()
        ini_camera_sn_int = int(ini_camera_sn_str)
        f.close()
        self.ReadsRGBCVals()
        if verbose:
            print('serial on file: %d \n serial of cam: %d' % (ini_camera_sn_int, camSN))
        if ini_camera_sn_int == camSN:
            return True
        else:
            return False
            
    def ReadsRGBCVals(self):
        """
        read and store the sRGB C values
        """
        camera_cal_filename = './' + self.camera_cal_ini_filename
        f = open(camera_cal_filename, 'r')
        linebuf = f.readline()
        linebuf = f.readline()
        linebuf = f.readline()
        self.srgb_cvals = np.zeros((3,3))
        for i in range(3):
            linebuf = f.readline()
            strlist = str.split(linebuf, ' ')
            for ic in range(3):
                self.srgb_cvals[i,ic] = float(strlist[ic])
        f.close()
        
    def ChirpCalStep1(self, 
                      all_on_img, \
                      all_dark_img, \
                      all_red_img, \
                      all_green_img, \
                      all_blue_img, \
                      verbose):
        """
        Chirp calibration step 1. 
        return True if successful, 
        return False if unsuccessful
        """
        #Dark img subtraction
        self.all_dark_img = all_dark_img
        self.all_on_img = all_on_img
        self.all_red_img = all_red_img
        self.all_green_img = all_green_img
        self.all_blue_img = all_blue_img
        self.all_on_ds_img = cv.addWeighted(all_on_img, 1.0, all_dark_img, -1.0, 0.0)
        self.all_red_ds_img = cv.addWeighted(all_red_img, 1.0, all_dark_img, -1.0, 0.0)
        self.all_green_ds_img = cv.addWeighted(all_green_img, 1.0, all_dark_img, -1.0, 0.0)
        self.all_blue_ds_img = cv.addWeighted(all_blue_img, 1.0, all_dark_img, -1.0, 0.0)
        self.w_stats = DotStats(self.all_on_ds_img)
        self.w_stats.DetectAnalyze(self.expected_dot_size, False, False)
        if verbose:
            print('Dots information')
            print(self.w_stats.dot_sizes)
            print(self.w_stats.rgbvalues)
            print(self.w_stats.coordinates)
        if not self.CheckNumLEDs(self.w_stats, echomessages = verbose):
            if verbose:
                print('check num LED failed')
            return False
        if not self.CheckBrightnessRatio(self.w_stats, \
                                         ratio_thres = self.raw_ratio_thres,\
                                         echomessages = verbose):
            if verbose:
                print('brightness ratio failed, faulty unit')
            return False
        #Record dots information
        self.dot_coordinates = self.w_stats.coordinates
        self.dot_sizes = self.w_stats.dot_sizes
        self.num_dots = self.w_stats.num_dots
        #Check Reds
        self.red_raw_stats = DotStats(self.all_red_ds_img)
        self.red_raw_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.red_raw_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.red_raw_stats, \
                                         ratio_thres = self.raw_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('Red color raw ratio check failed!')
            return False
        #Check greens
        self.green_raw_stats = DotStats(self.all_green_ds_img)
        self.green_raw_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.green_raw_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.green_raw_stats, \
                                         ratio_thres = self.raw_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('green color raw ratio check failed!')
            return False
        #Check blues
        self.blue_raw_stats = DotStats(self.all_blue_ds_img)
        self.blue_raw_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.blue_raw_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.blue_raw_stats, \
                                         ratio_thres = self.raw_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('blue color raw ratio check failed!')
            return False
        #Calibrate IREF values
        self.CalculateIrefValues(self.red_raw_stats, \
                                 self.green_raw_stats, \
                                 self.blue_raw_stats)
        self.WriteIrefRegisters()
        return True
        
    def ChirpCalStep2(self, 
                      all_red_irefcal_img, \
                      all_green_irefcal_img, \
                      all_blue_irefcal_img, \
                      verbose ):
        """
        Step 2 of Chirp calibration. 
        Veify the iref cal results, then
        Calculate the CCMs
        If successful, return True
        if not, return False
        Note that calibration file will NOT be written at this step
        Rather, the calibration file will be written in the verification step
        """
        #dark subtraction
        self.all_red_irefcal_img = all_red_irefcal_img
        self.all_green_irefcal_img = all_green_irefcal_img
        self.all_blue_irefcal_img = all_blue_irefcal_img
        self.all_red_irefcal_ds_img = cv.addWeighted(self.all_red_irefcal_img, \
                                                     1.0, \
                                                     self.all_dark_img,\
                                                     -1.0,\
                                                     0.0)
        self.all_green_irefcal_ds_img = cv.addWeighted(self.all_green_irefcal_img, \
                                                     1.0, \
                                                     self.all_dark_img,\
                                                     -1.0,\
                                                     0.0)
        self.all_blue_irefcal_ds_img = cv.addWeighted(self.all_blue_irefcal_img, \
                                                     1.0, \
                                                     self.all_dark_img,\
                                                     -1.0,\
                                                     0.0)
        #Red color check
        self.red_iref_stats = DotStats(self.all_red_irefcal_ds_img)
        self.red_iref_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.red_iref_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.red_iref_stats, \
                                         ratio_thres = self.iref_cal_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('red color iref cal check failed! quit')
            return False
        #green color check
        self.green_iref_stats = DotStats(self.all_green_irefcal_ds_img)
        self.green_iref_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.green_iref_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.green_iref_stats, \
                                         ratio_thres = self.iref_cal_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('green color iref cal check failed! quit')
            return False
        #blue color check
        self.blue_iref_stats = DotStats(self.all_blue_irefcal_ds_img)
        self.blue_iref_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.blue_iref_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.blue_iref_stats, \
                                         ratio_thres = self.iref_cal_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('blue color iref cal check failed! quit')
            return False        
        #Calculate CCMs
        self.ccms = np.zeros((self.NumLEDs, 3,3))
        LED_cvals = np.zeros((3,3))
        for i in range(self.NumLEDs):
            LED_cvals[0,:] = self.red_iref_stats.rgbvalues[i,:]
            LED_cvals[1,:] = self.green_iref_stats.rgbvalues[i,:]
            LED_cvals[2,:] = self.blue_iref_stats.rgbvalues[i,:]
            currentccm = np.dot( np.linalg.inv(LED_cvals.transpose()), \
                                 self.srgb_cvals.transpose())
            self.ccms[i,:,:] = currentccm
        self.NormalizeCCMs()
        return True
        
    def CalculateColorDistance(self, rgb1, rgb2):
        """
        calculate rgb color distances
        x = r/(r+g+b), y = g/(r+g+b)
        """
        x1 = rgb1[0]/np.sum(rgb1)
        x2 = rgb2[0]/np.sum(rgb2)
        y1 = rgb1[1]/np.sum(rgb1)
        y2 = rgb2[1]/np.sum(rgb2)
        cdis = ((x2-x1)**2.0 + (y2-y1)**2.0)**0.5
        return cdis
        
    def VerifyChirpCalibration(self, \
                               srgb_red_img, \
                               srgb_green_img, \
                               srgb_blue_img, \
                               file_dir, \
                               verbose):
        """
        Verify Chirp LED calibration
        """
        #dark level subtraction
        self.srgb_red_ds_img = cv.addWeighted(srgb_red_img, 1.0 , \
                                              self.all_dark_img, -1.0, 0.0)
        self.srgb_green_ds_img = cv.addWeighted(srgb_green_img, 1.0 , \
                                              self.all_dark_img, -1.0, 0.0)
        self.srgb_blue_ds_img = cv.addWeighted(srgb_blue_img, 1.0 , \
                                              self.all_dark_img, -1.0, 0.0)
        #Check brightness ratios
        #Red check
        self.srgb_red_stats = DotStats(self.srgb_red_ds_img)
        self.srgb_red_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.srgb_red_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.srgb_red_stats, \
                                         ratio_thres = self.final_cal_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('red color final cal check failed! quit')
            return False
        #green check
        self.srgb_green_stats = DotStats(self.srgb_green_ds_img)
        self.srgb_green_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.srgb_green_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.srgb_green_stats, \
                                         ratio_thres = self.final_cal_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('green color final cal check failed! quit')
            return False        
        #blue check
        self.srgb_blue_stats = DotStats(self.srgb_blue_ds_img)
        self.srgb_blue_stats.LoadDotsInfo(self.dot_coordinates, self.dot_sizes, self.num_dots)
        self.srgb_blue_stats.AnalyzeDots()
        if not self.CheckBrightnessRatio(self.srgb_blue_stats, \
                                         ratio_thres = self.final_cal_ratio_thres, \
                                         echomessages = verbose):
            if verbose:
                print('blue color final cal check failed! quit')
            return False
  
        #Check color distance
        red_dis = self.CalculateColorDistance(self.srgb_red_stats.GetMeanRGB(), \
                                              self.srgb_cvals[0,:])
        green_dis = self.CalculateColorDistance(self.srgb_green_stats.GetMeanRGB(), \
                                                self.srgb_cvals[1,:])
        blue_dis = self.CalculateColorDistance(self.srgb_blue_stats.GetMeanRGB(), \
                                               self.srgb_cvals[2,:])
        red_dis_old = self.CalculateColorDistance(self.srgb_red_stats.GetMeanRGB(), \
                                                  self.red_raw_stats.GetMeanRGB())
        green_dis_old = self.CalculateColorDistance(self.srgb_green_stats.GetMeanRGB(), \
                                                  self.green_raw_stats.GetMeanRGB())
        blue_dis_old = self.CalculateColorDistance(self.srgb_blue_stats.GetMeanRGB(), \
                                                  self.blue_raw_stats.GetMeanRGB())
        if verbose:
            print('Error reduction summary:')
            print('red color error:')
            print('before: %.8f' % red_dis_old)
            print(' after: %.8f' % red_dis)
            if red_dis > 0:
                print('color error reduction ratio: %.2fX' % (red_dis_old/red_dis))
            print('green color error:')
            print('before: %.8f' % green_dis_old)
            print(' after: %.8f' % green_dis)
            if green_dis > 0:
                print('color error reduction ratio: %.2fX' % (green_dis_old/green_dis))
            print('blue color error:')
            print('before: %.8f' % blue_dis_old)
            print(' after: %.8f' % blue_dis)
            if blue_dis > 0:
                print('color error reduction ratio: %.2fX' % (blue_dis_old/blue_dis))
        if green_dis > self.cdis_thres or \
           red_dis > self.cdis_thres or \
           blue_dis > self.cdis_thres:
            return False
        else:
            self.WriteCalibrationFile(file_dir)
            return True
