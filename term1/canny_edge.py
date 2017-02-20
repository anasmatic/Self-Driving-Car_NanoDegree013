# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 18:29:15 2017

@author: Omnia
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

image = mpimg.imread("exit-ramp.jpg")
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
#plt.imshow(gray);

kernal_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernal_size,kernal_size),0)
#plt.imshow(blur_gray);

low_threshold = 50
high_threshold = low_threshold*3
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
#plt.imshow(edges, cmap='Greys_r');

# Next we'll create a masked edges image using cv2.fillPoly()
mask = np.zeros_like(edges)   
ignore_mask_color = 255   

# This time we are defining a four sided polygon to mask
imshape = image.shape
#vertices = np.array([[(0,imshape[0]),(0, 0), (imshape[1], 0), (imshape[1],imshape[0])]], dtype=np.int32)
vertices = np.array([[(0,imshape[0]),(465, 280), (495, 280), (imshape[1],imshape[0])]], dtype=np.int32)
cv2.fillPoly(mask, vertices, ignore_mask_color)
masked_edges = cv2.bitwise_and(edges, mask)           
plt.imshow(masked_edges)

# Define the Hough transform parameters
rho = 1
theta = 1*(np.pi/180)#63 also is good
print(theta)
threshold = 1
min_line_length = 8
max_line_gap = 5

#lines = cv2.HoughLinesP(edges,rho,theta,threshold,np.array([]),min_line_length,max_line_gap)
lines = cv2.HoughLinesP(masked_edges,rho,theta,threshold,np.array([]),min_line_length,max_line_gap)
#print(lines)
# Make a blank the same size as our image to draw on
line_image = np.copy(image)*0
                    
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
        
color_copy_of_edges = np.dstack((edges,edges,edges))

combo = cv2.addWeighted(color_copy_of_edges,.8,line_image,.5,0)
plt.imshow(combo)
        