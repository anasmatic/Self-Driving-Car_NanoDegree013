# Traffic Sign Recognition
---
**Build a Traffic Sign Recognition Project**

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/481/view) individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one. You can submit your writeup as markdown or pdf. You can use this template as a guide for writing the report. The submission includes the project code.

You're reading it! and here is a link to my [project code](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/Traffic_Sign_Classifier_try5.html)

### Data Set Summary & Exploration

#### 1. Provide a basic summary of the data set and identify where in your code the summary was done. In the code, the analysis should be done using python, numpy and/or pandas methods rather than hardcoding results manually.

The code for this step is contained in the second code cell of the IPython notebook.  

I used native python, numpy library to calculate and visualize summary statistics of the traffic
signs data set:

* The size of training set is 34799
* The size of validation set is 4410
* The size of test set is 12630
* The shape of a traffic sign image is (32, 32, 3)
* The number of unique classes/labels in the data set is 43

#### 2. Include an exploratory visualization of the dataset and identify where the code is in your code file.

The code for this step is contained in the 3rd, 4th,& 5th code cells of the IPython notebook, with help of pandas, numpy.

these are the 43 sign in our data set

![el data set](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/examples/all_signs.jpg)

Here is an exploratory visualization of the data set. It is a bar chart showing bad distribution of data, which may effect the quality of any algorithm

![bar chart](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/examples/distribution.jpg)

### Design and Test a Model Architecture

#### 1. Describe how, and identify where in your code, you preprocessed the image data. What tecniques were chosen and why did you choose these techniques? Consider including images showing the output of each preprocessing technique. Pre-processing refers to techniques such as converting to grayscale, normalization, etc.

The code for this step is contained in the 6th, 7th, & 8th code cell of the IPython notebook.

#### function preprocess_image_set :
this function pre-processes validation and test data, it also works with train data, but train data requires more works.

 - As a first step, I decided to convert the images to grayscale to reduce the amount of processing required  to train this data.
training 3 channels of data is not required and increase the training time.

 - then contrast the image, "Histogram Equalization" stretch out the intensity range, which improves the details of an image.
 - 
Here is an example of applying this proccess to traffic sign image.
![effects](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/examples/before-after.jpg)

As a last step, I normalized the image data because ... they everybody says it is important !
I come from a game development background, in games we normalize movement vectors, because we apply changes to it all the time, normalization grantees changes will effect the same way allover game objects.
I guess this will be the same for weights and images.


#### 2. Describe how, and identify where in your code, you set up training, validation and testing data. How much data was in each set? Explain what techniques were used to split the data into these sets. (OPTIONAL: As described in the "Stand Out Suggestions" part of the rubric, if you generated additional data for training, describe why you decided to generate additional data, how you generated the data, identify where in your code, and provide example images of the additional data)

#### function preprocess_train_set :

 - this function will do the same as the one above to all training data.
 - it also augment some images : 
	 - whenever a label has less than 500 sample, we make a 2 copies of it and save it back to the training data.
	 - this means if a label has only 200 sample, it will end up having 600 sample, which will improve its chances in training process
	 - the 2 copies will be augmented as following :
		 - random gamma
		 - random (+/-)20 degrees rotation.

the augmentation process has no effect on training/validation accuracy , actually it decreased it !
but it has a grat effect on testing :
in file [Traffic_Sign_Classifier_try4](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/Traffic_Sign_Classifier_try4.html) I didn't use this augmentation method, the Analyze Performance of the external images test was 50%
but after applying the Augmentation , it increased to 83%

####3. Describe, and identify where in your code, what your final model architecture looks like including model type, layers, layer sizes, connectivity, etc.) Consider including a diagram and/or table describing the final model.

cells from 9 to 12

I'm using [LeNet](http://yann.lecun.com/exdb/lenet/)  with the following layers:

| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:| 
| Input | 32x32x1 RGB image | 
| Convolution 5x5 | 1x1 stride, VALID padding, outputs 28x28x6 |
|RELU||
| Max pooling | 2x2 stride, outputs 14x14x6 |
| Convolution 5x5 | 1x1 stride, VALID padding, outputs 10x10x32|
|RELU||
| Max pooling | 2x2 stride,  outputs 5x5x32 |
| Fully connected|output 512|
|RELU||
| Fully connected|output 128|
|RELU||
| output| 43|


#### 4. Describe how, and identify where in your code, you trained your model. The discussion can include the type of optimizer, the batch size, number of epochs and any hyperparameters such as learning rate.
cells 13, 14 ,15

learning rate = 0.0005
cell 10 :
EPOCHS = 150 but 80 should be enough 
BATCH_SIZE = 128

using AdamOptimizer had good effect on accuracy, as it changes learning rate though epochs.

#### 5. Describe the approach taken for finding a solution. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.



My final model results were:

 - training set accuracy of 99%
 - validation set accuracy of 95% to 96%
 - test set accuracy of 93.5


If an iterative approach was chosen:
 

 - What was the first architecture that was tried and why was it chosen?
	 * I used default LeNet and tried to build something similar to inception V5
 - What were some problems with the initial architecture?
	 * I failed building Inception like structure
	 * default LeNet could not exceed .98 even after augmentation
 - How was the architecture adjusted and why was it adjusted?
	 - add more depth to weights and biases, after some trials.
	 - no need for batch_norm, it had bad effect on accuracy
	 - no need for dropout, has also bad effect
	 - add RELU after all conv layers and fully connected layers
	 - network was never over fitting ! it was always under fitting , and I really had no idea what I'm doing to make it come over it !
 - Which parameters were tuned? How were they adjusted and why?
	 - learning rate and epochs had great impact on results
	 - patch size had no impact on accuracy
 - What are some of the important design choices and why were they chosen?
	 - I tried everything and I was pulling my hair, then I decide to play with weight !
	 - I didn't know what I'm doing, and I still don't know how I made it work.
	 - also adding more epochs was good thing do

If a well known architecture was chosen:

 - What architecture was chosen?
	 - LeNet
 - Why did you believe it would be relevant to the traffic sign application?
	 - I don't know , please tell me.
 - How does the final model's accuracy on the training, validation and test set provide evidence that the model is working well?
	 - I think 99% training accuracy is great
	 - 95% to 96% validation accuracy with my lame skills is fine
	 - also 93% test accuracy with my lame skills was great !
 

###Test a Model on New Images

####1. Choose five German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.

Here are five German traffic signs that I found on the web:

![priority road](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/testphotos/Arterial.jpg) ![children crossing](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/testphotos/be-aware-of-children.jpg) ![dangerous curve to the left](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/testphotos/left_curve.jpg)
![dangerous curve to the right](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/testphotos/right_curve.jpg) ![children crossing](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/testphotos/traffic-signs-children-crossing.jpg) ![yield](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/CarND-Project2_Traffic-Sign-Classifier/testphotos/yeld.jpg)

all photos were chosen with letter rotation or skew
the yellow "children crossing" photo is cropped from edge and has stickers on it.

#### 2. Discuss the model's predictions on these new traffic signs and compare the results to predicting on the test set. Identify where in your code predictions were made. At a minimum, discuss what the predictions were, the accuracy on these new predictions, and compare the accuracy to the accuracy on the test set (OPTIONAL: Discuss the results in more detail as described in the "Stand Out Suggestions" part of the rubric).


Here are the results of the prediction:

|Image|Prediction| 
|:---------------------:|:---------------------------------------------:| 
| priority road|priority road| 
|children crossing|children crossing|
|dangerous curve to the left|dangerous curve to the left|
|dangerous curve to the right|dangerous curve to the right|
|children crossing| pedestrian|
|yield| yield|


The model was able to correctly guess 5 of the 6 traffic signs, which gives an accuracy of 83%. 

I think if we have more samples of "pedestrian" (has only 630 sample) , the network would have done better.

#### 3. Describe how certain the model is when predicting on each of the five new images by looking at the softmax probabilities for each prediction and identify where in your code softmax probabilities were outputted. Provide the top 5 softmax probabilities for each image along with the sign type of each probability. (OPTIONAL: as described in the "Stand Out Suggestions" part of the rubric, visualizations can also be provided such as bar charts)

soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| 100% | priority road| 
| 99% |children crossing|
| 94%	|dangerous curve to the left|
| 100%	 | dangerous curve to the right|
| 99%	| pedestrian (should be :children crossing)|
| 100%	| yield|

the second "children crossing" image was wrong prediction, the network was sure 100% it is not "children crossing" !
I think the network needs to be keen about small detains in the center of the image.

