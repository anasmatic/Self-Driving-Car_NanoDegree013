# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:08:25 2017

@author: Omnia
"""
import sys
import numpy as np
#np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

PATH = "test.jpg"
image = mpimg.imread(PATH)
print('This image is: ',type(image), 
         'with dimensions:', image.shape)
#I don't know why !
ysize = image.shape[0]
xsize = image.shape[1]
### region masking
region_select = np.copy(image)
left_bottom = [100,539]
right_bottom = [810,539]
apex = [480,300]

fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

# Find the region inside the lines
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*fit_left[0] + fit_left[1])) & \
                    (YY > (XX*fit_right[0] + fit_right[1])) & \
                    (YY < (XX*fit_bottom[0] + fit_bottom[1]))

#region_select[region_thresholds] = [255, 0, 0]
#sys.exit();
### color selection
#make copy
color_select = np.copy(image)
#find the wight
#print("line 539: ",color_select[539,750:800,:])
#

#define white !!!
red_threshold = 200#230
green_threshold = 200#240
blue_threshold = 200#230
rgb_threshold = [red_threshold, green_threshold, blue_threshold]

# all data won't apply to this comparison, even the black points !
color_thresholds = (image[:,:,0] < rgb_threshold[0]) \
            | (image[:,:,1] < rgb_threshold[1]) \
            | (image[:,:,2] < rgb_threshold[2])            
#applying comparison to array
color_select[color_thresholds] = [0,0,0]


# Color pixels red which are inside the region of interest
region_select[~color_thresholds & region_thresholds] = [255, 0, 0]

# Display the image
plt.imshow(color_select)
plt.imshow(region_select)
#plt.show()