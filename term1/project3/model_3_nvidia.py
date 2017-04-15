# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:50:23 2017

@author: Omnia
"""

import csv
import cv2
import numpy as np
import time
_time = time.time()

lines = []
with open("data/driving_log.csv") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)
print("lines",len(lines))#passed

print("_time ",(time.time() - _time))
_time = time.time()

images = []
measures = []
for line in lines:
    for i in range(3):
        source_path = line[i]
        filename = source_path.split('\\')[-1]
        current_path = "data\\IMG\\"+filename
        image = cv2.imread(current_path)
        #image = cv2.imread(source_path)
        images.append(image)
        images.append(cv2.flip(image,1))
        measure = float(line[i+3])
        measures.append(measure)
        measures.append(measure*-1.0)
print("measures",len(measures))#passed
print("measures ex:",measures[len(measures)-1])#passed
print("images",len(images))#passed

print("_time ",(time.time() - _time))
_time = time.time()
print("converting to train array")

X_train = np.array(images)
y_train = np.array(measures)

print("_time ",(time.time() - _time))
_time = time.time()

#checkpoint :
X_train_test = X_train
y_train_test = y_train
print("\nmodel...")
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, MaxPooling2D, Conv2D, Cropping2D

#model :
model = Sequential()
#normalize and mean center
model.add(Lambda(lambda x: (x/255.0) - 0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((75,25), (0,0)), input_shape=(160,320,3)))
#LeNet
model.add(Conv2D(24,(5,5), subsample=(2,2), activation='relu'))
model.add(Conv2D(36,(5,5), subsample=(2,2), activation='relu'))
model.add(Conv2D(48,(5,5), subsample=(2,2), activation='relu'))
model.add(Conv2D(64,(3,3), subsample=(2,2), activation='relu'))
model.add(Conv2D(64,(3,3), subsample=(2,2), activation='relu'))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

print("_time ",(time.time() - _time))
_time = time.time()
print("\ntraining")
#train
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
hist = model.fit(X_train_test, y_train_test, validation_split=0.2, shuffle=True, epochs=10, verbose=1)
print(hist.history)


print("_time ",(time.time() - _time))
_time = time.time()
print("saving to 'model_3.h5'")
model.save('model_3.h5')