# Advanced Lane Finding Project
#### Writeup
 ---
**The goals / steps of this project are the following:** 

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

---

## [Rubric Points](https://review.udacity.com/#!/rubrics/571/view) 

**Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  **

### Camera Calibration

#### **1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.**

The code for this step is contained in the cell 1 to cell 4 of the IPython notebook located in "./Project4.ipynb"

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![camera calibration](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/001_corners.png)

### **Pipeline (single images)**

#### **1.  distortion-corrected image.**

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![undistort test image](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/002_undistort.png)

#### **2. create a thresholded binary image using color transforms, gradients or other methods .**
That was a long round , and has been revisited many times
I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at cells 5 to 8).  
an example of my output for this step at cell 9

After testing various colors spaces , I decided that LAB space is the best for detecting yellow and light colors ( this choice was solid after encountering shadow and lighting problems ), so I used that for sobel of X
mixing channel L and B.

![sobel L+ B of LAB](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/003_sobel LAB.png)

after that I make color transform using channel S of HLS color space
and mix that with Sobel of L+B of LAB :
![S of HLS and Sobel of L+B of LAB](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/004_lab-hsl.png)
using low threshold and high kernel with Sobel , and high threshold for color transform ,  the final result looks great:
![S of HLS and Sobel of L+B of LAB](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/005_mix.png)


#### **3. perspective transform **

function `warper()` in cell 10 , I use dynamic horizon ( top limit ) of 36% of the photo , lowering this horizon value will make harsh curves detectable

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![warp img](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/006_warp.png)


#### **4. identify lane-line pixels and fit their positions with a polynomial**

cell 15 , using function **`slidingwindowsearch`** in external file **lanesearch.py** , I was able to detect lanes with least confusion !
this function would take a histogram of white points in image, then define the peak : where the most white points are.
dividing the pic into 2 half , the peak at the left will define left lane, and same for right side.
window search is defining a small window at the very bottom , this window will follow while pixels around the peak x axis , then the window will move up (on y axis) trying to find the rest of the lane
at the end we use 2nd order polynomial to draw a line/curvy line that defines each lane. 

![curved lane detected](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/007_curved_lane.png)


#### **5. calculate the radius of curvature of the lane and the position of the vehicle with respect to center.**

cell 16, using function `find_curvature`& `position_to_center` in external file **curvatureandcenter.py** .
`find_curvature` converts pixels to meters using this scale :
in y dimension, there is 30/720  meters per pixel 
in x dimension, there is 3.7/700 meters per pixel 
the higher the result is, the less curvy is the road.

`position_to_center`finds the midpoint of lanes with respect to center of camera, less than 0 means the car is near to right lane than left lane.

`translate_position_to_center` converts the position to human readable instructions "position ##m to left/right"

#### **6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.**

cell 18 , function `drawlane_unwarpimage` unwarps a plotted image of the curve (results the green triangle like shape below) , and combine it with the original un-distorted photo :

![combine plotted curve with original image](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/008_mix result.png)

then write curvatuer and position data to image ( function `write_curv_pos`)

![final result](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/009_final.png)


### **the pipeline function :**
##### **- Revisit code- smoothing and skipping.**
pipe line function `find_lane_main_pipeline`at cell 20 , is where all instructions above are mixed.
it expects color image as input, and will return the same color with lane detected and drawn over the image.

**skipping :**
function `skipslidingwindowsearch` from file `lanesearch.py` is used often in the main pipeline function.
we need `slidingwindowsearch` from same file to draw the first lane.
then `skipslidingwindowsearch` would detect lanes in the next frames until it fails.
when `skipslidingwindowsearch` fails, function `slidingwindowsearch`is back in business to detect the lane that `skipslidingwindowsearch` failed to detect.

while `slidingwindowsearch` searches as explained in point 4 , function `skipslidingwindowsearch` traces the detected lanes from last frame, and searches around these lanes, with a margin 38 pixels to left or right .

To get better results, I run simple sanity check after each window search ( cell 20 ) , if lane width is so small, so we would use data from last detected image.

**Smoothing:**
using function `smothing_fit` from cell 19 after the sanity check,
this function keeps tracking fit-lines , it needs 10 frames to calculate the average of them, and that average will be will define how the current frame will look like.


---

### Pipeline (video)
link to final video output.

Here's a [link to my video result](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/project_video_result.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I had to do many trials to make this project work :
**first :** detecting lanes in the lighter asphalt material  had been a problem (check : project_video_result (01).mp4 )
so I had to tweak thresholds values, that could fix the lane expansion to the wall problem !

**second :** but last fix was good only for lighter lanes at second 20, but second 39 was a disaster (check : project_video_result (02).mp4 )
more teaks to gradient threshold and transform color parameters were done to fix that.

**third :** shadows at second 41 caused a major problem (check : project_video_result (03).mp4 ) , at this point I was using HLS color space for both gradient and color transform, but that was not helping in shadows.
so after trying all color spaces , LAB results was promising , but I have to mix gradients from 2 channels of LAB to get the best result.
![sobel L+ B of LAB](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/010_desc_1.png)
results were better (check : project_video_result_45marg.mp4 )

**fourth :** I noticed that lanes are pulled to the black car coming from the left, what fix that was tweaking gradient to lower values, using higher Sobol kernel, and higher color transform thresholds.
Also using lower `skipslidingwindowsearch` margin limited the search to be accurately following the lanes, and ignoring the car
 adding smoothing  function had a great effect overall the video , and especially the current problem.

I can't use the same pipeline function with challenge video (check challenge_video_result.mp4) , bad result caused by asphalt colors.
when removing smoothing and `skipslidingwindowsearch` ,  and using higher thresholds I got slightly less catastrophic result (check challenge_video_result (01).mp4)

that was fun , but extremely time consuming .
