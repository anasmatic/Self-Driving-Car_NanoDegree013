##Vehicle Detection Project##

The goals / steps of this project are the following:

* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images and train a classifier Linear SVM classifier
* Optionally, you can also apply a color transform and append binned color features, as well as histograms of color, to your HOG feature vector. 
* Note: for those first two steps don't forget to normalize your features and randomize a selection for training and testing.
* Implement a sliding-window technique and use your trained classifier to search for vehicles in images.
* Run your pipeline on a video stream (start with the test_video.mp4 and later implement on full project_video.mp4) and create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles.
* Estimate a bounding box for vehicles detected.

---
###Histogram of Oriented Gradients (HOG)

####1. Explain how (and identify where in your code) you extracted HOG features from the training images.

The code for this step is contained in the first code cell of the IPython notebook

I started by reading in all the `vehicle` and `non-vehicle` images.  Here is an example of one of each of the `vehicle` and `non-vehicle` classes:

![alt text][image1]

I manually split the data, making most of test (vehicles) come from 'KITTI_extracted' folder

I then explored different color spaces and different `skimage.hog()` parameters (`orientations`, `pixels_per_cell`, and `cells_per_block`).  I grabbed random images from each of the two classes and displayed them to get a feel for what the `skimage.hog()` output looks like.

Here is an example using the `YCrCb` color space and HOG parameters of `orientations=9`, `pixels_per_cell=(8, 8)` and `cells_per_block=(2, 2)`:
![HOG using YCrCb](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/hog_ycrcb.png)


Here is an example using the `HSV` color space and HOG parameters of `orientations=8`, `pixels_per_cell=(8, 8)` and `cells_per_block=(2, 2)`:
![HOG using HSV](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/hog_hsv.png)

####2. Explain how you settled on your final choice of HOG parameters.

I was not able to decide , until I trained a classifier..
when I Trained data , I got great results using both HSV & YCrCb.
but when I used HSV to detect cars in test images, it was NOT able to detect light color cars, unlike YCrCb.

####3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

I trained a linear SVM using 'rbf' kernel , and C=10.0
those parameters was determined after using GridSearchCV  .

    best_params_ {'kernel': 'rbf', 'C': 10}

training was done after extracting Color features ( spatial bins , and histogram), combined with HOG features

###Sliding Window Search

####1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?

first I used 64*64 window search over the lower third of images,
but cars very near camera or very far to camera were NOT detected,
so I planned to use multi scale -actually multi sizes - windows

every size would go over 2 lines, 
windows will maintain same y point, however size will make covered area vary

![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/slide_01.png)
![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/slide_02.png)
![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/slide_03.png)
![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/slide_04.png)


---

### Video Implementation

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)
Here's a [link to my video result](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/project_video_res.png)

and another [link ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/project_video_res.png) before applying smoothing

####2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

I created a "Heatmap' , that counts how many positive detections were detected , then apply threshold to this heatmap, that will detect false positives.
I then used `scipy.ndimage.measurements.label()` to identify individual blobs in the heatmap.  
I then assumed each blob corresponded to a vehicle.  I constructed bounding boxes to cover the area of each blob detected.  

#### Here are examples of heatmaps and final bounding boxes:

![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/heat.png)
![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/heat01.png)
![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/heat02.png)
![ ](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project5_Vehicle-Detection/output_images/heat_empty.png)


---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

**HOG**
I was not able to see the difference between colorspaces I thought they are promising (HSV & YCrCb) until I trained my SVM classifier , and saw the result on test images.
If I'm able to predict a good color space from its HOG visualization, that will save time.
 
**Search Windows**:

 - it needs performance improvement, because every frame is taking 10 seconds to be processed , this improvement my include using proper usage of scaling than it is now in the code, and/or using less rows and columns.
 - skip searching where a car is already detected, and focusing on road center or/and sides , ignoring some frames as long as I'm able to predict a detected car position 

**More data**:
may be using udacity "aicrowd" data will improve the detection accuracy, that I noticed the system now cant detect a car by its side.

**Smothing**:
I know my current algorithm of smoothing is lame, but I really hadn't any plans in mind while building it, but I'll work on it until it can track a car even when it is overlapping with another.


