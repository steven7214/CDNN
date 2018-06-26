#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from sklearn.model_selection import StratifiedKFold
import numpy
import os

numpy.random.seed(7)

#get testing data set
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Cancers/Testing.csv')
testingData = numpy.loadtxt(filename, delimiter=",")

#get cancers and normal data set
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Cancers/Normal.csv')
normalData = numpy.loadtxt(filename, delimiter=",")
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Cancers/Pancreas.csv')
cancerData = numpy.loadtxt(filename, delimiter=",")

#split data
test = [testingData[:, 0:40], testingData[:, 40], testingData[:, 41]]
normal = [normalData[:, 0:40], normalData[:, 40]]
cancer = [cancerData[:, 0:40], cancerData[:, 40]]
train = [numpy.vstack((normal[0],cancer[0])), numpy.hstack((normal[1],cancer[1]))]

#create file to write in
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/CrossValidation/results.csv')
file = open(filename, 'w')

model = Sequential()
model.add(Dense(30, input_dim=40, kernel_regularizer=regularizers.l2(0), activation='relu'))
model.add(Dense(25, kernel_regularizer=regularizers.l2(0), activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#class_weight makes false positives less desirable
model.fit(train[0], train[1], class_weight={0: 1, 1: 1}, epochs=120, batch_size=32, verbose = 0)

accuracy = model.evaluate(train[0], train[1], verbose = 0)
print("train: " + str(accuracy[1]*100))
accuracy = model.evaluate(test[0], test[1], verbose = 0)
print("test: " + str(accuracy[1]*100))

#calculate prediction
predictions = model.predict(test[0])
predictions = predictions.tolist()

#round predictions
rounded = []
for prediction in predictions:
    rounded.append(round(prediction[0]))

#add cancer types
types = test[2]
#add real cancer value
real = test[1]

#change to add cancer type
falsePositive = 0
for count in range(len(rounded)):
    if real[count] == 0 and rounded[count] != 0:
        falsePositive += 1
    line = str(real[count]) + "," + str(rounded[count]) + "," + str(types[count])
    file.write(line + "\n")
print("false positives: " + str(falsePositive)+ "\n")
file.close()
