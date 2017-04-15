# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:50:23 2017

@author: Omnia
"""

import csv
import cv2
import numpy as np

lines = []
with open("data/driving_log.csv") as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)
#print("lines",lines)#passed
images = []
measures = []
for line in lines:
    source_path = line[0]
    filename = source_path.split('\\')[-1]
    current_path = "data\\IMG\\"+filename
    #print(current_path)
    image = cv2.imread(current_path)
    #image = cv2.imread(source_path)
    images.append(image)
    measure = float(line[3])
    measures.append(measure)
"""
print("loading test image..")    
#passed using : image = cv2.imread(source_path)
#passed using : image = cv2.imread(current_path)
cv2.imshow("check",images[0])
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
X_train = np.array(images)
y_train = np.array(measures)

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda

model = Sequential()
#normalize and mean center
model.add(Lambda(lambda x: (x/255.0 -0.5), input_shape=(160,320,3)))
model.add(Flatten())
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')
model.fit(X_train, y_train, validation_split=0.2, shuffle=True, epochs=4)

model.save('model.h5')