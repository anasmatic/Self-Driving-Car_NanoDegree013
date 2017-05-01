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

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the cell 1 to cell 4 of the IPython notebook located in "./Project4.ipynb"

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![camera calibration](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/001_corners.png)

### Pipeline (single images)

#### 1.  distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![undistort test image](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/002_undistort.png)

#### 2. create a thresholded binary image using color transforms, gradients or other methods .
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


#### 3. perspective transform 

function `warper()` in cell 10 , I use dynamic horizon ( top limit ) of 36% of the photo , lowering this horizon value will make harsh curves detectable

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![warp img](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/006_warp.png)


#### 4. identify lane-line pixels and fit their positions with a polynomial

cell 15 , using function **`slidingwindowsearch`** in external file **lanesearch.py** , I was able to detect lanes with least confusion !
this function would take a histogram of white points in image, then define the peak : where the most white points are.
dividing the pic into 2 half , the peak at the left will define left lane, and same for right side.
window search is defining a small window at the very bottom , this window will follow while pixels around the peak x axis , then the window will move up (on y axis) trying to find the rest of the lane
at the end we use 2nd order polynomial to draw a line/curvy line that defines each lane. 

![curved lane detected](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project4_Advanced-Lane-Lines/examples/007_curved_lane.png)


#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  

