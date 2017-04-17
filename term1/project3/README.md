# **Behavioral Cloning** 

#### Writeup
 ---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/placeholder.png "Model Visualization"
[image2]: ./examples/placeholder.png "Grayscaling"
[image3]: ./examples/placeholder_small.png "Recovery Image"
[image4]: ./examples/placeholder_small.png "Recovery Image"
[image5]: ./examples/placeholder_small.png "Recovery Image"
[image6]: ./examples/placeholder_small.png "Normal Image"
[image7]: ./examples/placeholder_small.png "Flipped Image"

## Rubric Points
##### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report as README.md of github summarizing the results
* vid.mp4 file viewing the car takes 2 laps ccw & cw (@ 47s in video)

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
#or python drive.py model_udacitydata.h5
```
model is trained using my data (model.h5) , and Udacity data (model_udacitydata.h5)
udacity data is better with taking curves, but my data is better with recoveries

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed
(model.py lines 85 to 127)
I'm using the Nvidia CNN (end to end)

Model starts with normalize and mean center `Lambda layer`
then `Cropping2D layer`

Model consists of 5 `Conv2D layers` 
with `elu activation`to introduce nonlinearity 
 and `TruncatedNormal initializer` 
first 3 layers are 5x5 filter sizes, next 2 are 3x3
depths are in order : 24 , 36 , 48 , 64, 64
then `Flatten` layer
after that comes 2 Fully connected layers, with weights 500 then 100
both layers has `elu activation`
and `he_normal initializer` 

#### 2. Attempts to reduce overfitting in the model

I used 2x2`MaxPooling2D` after every `Conv2D` layer ,
also `Dropout` layers after `Dense` layers ,
in order to reduce overfitting 

The model was trained and validated on different data sets to ensure that the model was not overfitting (code line 10-16). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning
I tried to use different learning rates [ from 0.1 to  0.00001] , but the results was not as good as useing `Adam` optimizer, 
so the learning rate was not tuned manually.

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road ... 

For details about how I created the training data, see the next section. 

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to ...

My first step was to use a convolution neural network model similar to the LeNet , I thought this model might be good as start.

I split the data to training and validation , shuffle, but no augmentation.

first I used the model without activation, initializer, or any layers to stop overfitting : result was fine , but tha car driving was too bad (goes in circles).

Then I tried Nvidia CNN (end to end), because it is used to drive a real car using cameras as inputs.
also I started without activation, initializer, or any layers to stop overfitting : result was better , car was going forward to the lake ! 
but I noticed that validation loss is lower than training loss, which I don't know what it means, but it is not good !
![loss1](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/project3/examples/loss1.png)

Next I used small amount of my data and tried to come over the latter problem.
adding various activations , initializers, and overfitting layers, I was able to reach a higher validation loss than training loss
![loss2](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/project3/examples/loss2.png)


At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

Here is a visualization of the architecture 

_________________________________________________________________
| Layer (type)  | Output Shape    | Params |
|:-------------:|:---------------:|:------:|
| lambda_1 (Lambda)  | (None, 80, 160, 3)       | 0 |        
| cropping2d_1 (Cropping2D) | (None, 33, 158, 3) |  0 |         
|conv2d_1 (Conv2D) | (None, 33, 158, 24) | 1824|      
|max_pooling2d_1 (MaxPooling2) | (None, 16, 79, 24) | 0|
|conv2d_2 (Conv2D)   |(None, 16, 79, 36)        |21636|     
|max_pooling2d_2 (MaxPooling2)| (None, 8, 39, 36)|0|         
|conv2d_3 (Conv2D) | (None, 8, 39, 48) | 43248 |    
|max_pooling2d_3 (MaxPooling2)| (None, 4, 19, 48)|0 |        
|conv2d_4 (Conv2D)|(None, 4, 19, 64)| 27712  |   
|max_pooling2d_4 (MaxPooling2) | (None, 2, 9, 64)          0   |      
|conv2d_5 (Conv2D)|(None, 2, 9, 64)|36928    | 
|max_pooling2d_5 (MaxPooling2)|(None, 1, 4, 64) |0|     
|flatten_1 (Flatten)|(None, 256)|0|
|dense_1 (Dense)|(None, 500)|128500|    
|dropout_1 (Dropout)|(None, 500)|0|         |
|dense_2 (Dense)|(None, 100)|50100    | 
|dropout_2 (Dropout)|(None, 100)|0|
|dense_3 (Dense)|(None, 20)|2020      |
|dense_4 (Dense)|(None, 1)|21|        
 ===============================
Total params: 311,989
Trainable params: 311,989
Non-trainable params: 0
_________________________________________________________________

#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I recorded 1.5 laps on track CCW, then 1.5 CW. driving smoothly through curves
 Here is an example image of center lane driving:

![center](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/project3/examples/center.gif)

then recorded the vehicle recovering from the left side and right sides of the road back to center ,CCW and CW, so that the vehicle would learn to recover back to center if it was drifted to any side :

![recovery1](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/project3/examples/recovery1.gif)

![recovery2](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/project3/examples/recovery2.gif)


then I flipped images and angles in order to create more data

After the collection process, I had 6786 number of data points.

I finally randomly shuffled the data set and put 30% of the data into a validation set. 

then training data for 5 epochs, save the model, but validation loss was less than training loss
then train for another 3 epochs, after that the validation loss was higher than training loss.
The ideal number of epochs was 8 .
I used an adam optimizer so that manually training the learning rate wasn't necessary.
best patch size was 32, for speed and training results.

_________________________________________________________________

#### 4. Result Video
here you can see the car driving CCW smothly through curves, even tight ones

![vid1](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/project3/examples/vid1.gif)

and then I rotated the car to drive CW, I made it stop on the dirt road but facing the asphalt,
as you can see the car was abel to  get off the dirt and position is self on the track.

![vid2](https://github.com/anasmatic/Self-Driving-Car_NanoDegree013/blob/master/term1/project3/examples/vid2.gif)
