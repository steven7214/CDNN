#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
import numpy
import os
from DataSplit import getData

numpy.random.seed(7)

#get complete data set
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv')
totalData = numpy.loadtxt(filename, delimiter=",")

#randomly split data into train, validation, test
#trainData, validationData, testData = getData(filename, 0.1, 0.2, False)

filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Training Data.csv' )
trainData = numpy.loadtxt(filename, delimiter=",")
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Test Data.csv')
testData = numpy.loadtxt(filename, delimiter=",")

#split data
train = [trainData[:, 0:39], trainData[:, 39]]
test = [testData[:, 0:39], testData[:, 39]]
total = [totalData[:, 0:39], totalData[:, 39]]

model = Sequential()
model.add(Dense(35, input_dim=39, kernel_regularizer=regularizers.l2(0.0002), activation='relu'))
model.add(Dense(20, kernel_regularizer=regularizers.l2(0), activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#class_weight makes false positives less desirable
model.fit(train[0], train[1], class_weight={0: 1, 1: 0.5}, epochs=150, batch_size=32, verbose = 0)

accuracy = model.evaluate(train[0], train[1], verbose = 0)
print("train: " + str(accuracy[1]*100))
accuracy = model.evaluate(total[0], total[1], verbose = 0)
print("total: " + str(accuracy[1]*100) + "\n")

#calculate prediction
predictions = model.predict(total[0])
#round predictions
rounded = [round(total[0]) for total in predictions]
output = total[0].tolist()
for count in range(len(rounded)):
    output[count].append(rounded[count])
#create file to write in
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/results.csv')
file = open(filename, 'w')
for list in output:
    line = ""
    for i in range(len(list)-1):
        line += str(list[i]) + ","
    line += str(list[len(list)-1])
    file.write(line + "\n")
file.close()
