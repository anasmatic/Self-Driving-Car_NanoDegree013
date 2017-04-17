# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 22:48:03 2017

@author: Anas
"""
#from test3-nvidia-2mousedata.ipynb

import csv
import cv2
import numpy as np
import sklearn
import time

#load the data I recorded
lines = []
with open("mydata/driving_log.csv") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)
#ignore header
lines = lines[1:]

#slpit data , to :training and validation
from sklearn.model_selection import train_test_split
train_samples, validation_samples = train_test_split(lines, test_size=0.3)

from sklearn.utils import shuffle
_time = time.time()

# to train data on fly and save disk , we use generators
def generator(samples, batch_size=32):
    #correction value will be used for side camera images
    correction = 0.2
    num_samples = len(samples)
    while True: # Loop forever so the generator never terminates
        shuffle(samples)
        #loop over this batch
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            for batch_sample in batch_samples:
                for i in range(3):
                    #get path
                    source_path = batch_sample[i]
                    source_path = source_path.replace(" ", "")#fix a typo in Udacity data
                    filename = source_path.split('\\')[-1]#get file name
                    current_path = "mydata/IMG/"+filename #append generic path to file name
                    image = cv2.imread(current_path)
                    #resize image 50% run training faster
                    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
                    #convert to RGB
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    images.append(image)
                    #add steering angle
                    measure = float(batch_sample[3])
                    if(i == 1):#left cam, add correction value to steering
                        measure = float(batch_sample[3]) + correction
                    elif(i == 2):#right cam, subtract correction value to steering
                        measure = float(batch_sample[3]) - correction
                    
                    angles.append(measure)
                    
                    #flip same data, and add it to the array
                    images.append(cv2.flip(image,1))
                    angles.append(measure*-1.0)
                    
            # trim image to only see section with road
            X_train = np.array(images)
            y_train = np.array(angles)
            #shuffle data
            train_shuffled = sklearn.utils.shuffle(X_train, y_train)
            #return tuple as required
            yield(train_shuffled[0] , train_shuffled[1])


#save batch_size , we will use it later in fit function
BATCH_SIZE =32
#save refrance to train and validation
train_generator = generator(train_samples, batch_size=BATCH_SIZE)
validation_generator = generator(validation_samples, batch_size=BATCH_SIZE)

##############################################################################
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, MaxPooling2D, Conv2D, Cropping2D, Dropout
from keras.initializers import TruncatedNormal

#the model
ch, row, col = 3, 160*.5, 320*.5  # resized image format
#model :
model = Sequential()
#normalize and mean center
model.add(Lambda(lambda x: (x/255.0) - 0.5, input_shape=(row,col,ch)))# output(None, 80, 160, 3)
model.add(Cropping2D(cropping=((35,12), (1,1)), input_shape=(row,col,ch)))# output (None, 33, 158, 3) 
#NVidia model
initializer=TruncatedNormal(mean=0.0, stddev=0.01, seed=None) # save the initializer
model.add(Conv2D(24,(5,5), input_shape=(33, 158, 3), activation='elu', padding='same', kernel_initializer=initializer))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(36,(5, 5), activation='elu', padding='same', kernel_initializer=initializer))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(48,(5,5), activation='elu', padding='same',kernel_initializer=initializer))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64,(3,3), activation='elu', padding='same',kernel_initializer=initializer))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64,(3,3), activation='elu', padding='same',kernel_initializer=initializer))
model.add(MaxPooling2D((2, 2)))

model.add(Flatten())

model.add(Dense(500, activation='elu', kernel_initializer='he_normal'))
model.add(Dropout(.5))

model.add(Dense(100, activation='elu', kernel_initializer='he_normal'))
model.add(Dropout(.25))

model.add(Dense(20, activation='elu', kernel_initializer='he_normal'))
model.add(Dense(1))

#model.summary()

##############################################################################
#train the model
from keras.optimizers import Adam
EPOCHS = 8
#use adam optimizer
model.compile(loss='mse', optimizer=Adam())
hist = model.fit_generator(train_generator, steps_per_epoch=len(train_samples)/BATCH_SIZE, validation_data=validation_generator, validation_steps=len(validation_samples)/BATCH_SIZE, epochs=EPOCHS)

#save model
model.save('model.h5')