#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.ensemble import RandomForestClassifier
from DataSplit import getData
import numpy
import os

numpy.random.seed(7)

#get complete data set
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv')
totalData = numpy.loadtxt(filename, delimiter=",")

#randomly split data into train, validation, test
trainData, validationData, testData = getData(filename, 0.1, 0.2, True)

#set number of false positives allowed
num = 1

#split data
train = [trainData[:, 0:40], trainData[:, 40]]
validation = [validationData[:, 0:40], validationData[:, 40]]
test = [testData[:, 0:40], testData[:, 40]]

model = Sequential()
threshold = 0.80
falsePositive = 10
while falsePositive > num:
    threshold += 0.01
    if threshold == 1:
        print("this the best it gon do")
        break
    average = 0
    falsePositive = 0
    model = Sequential()
    model.add(Dense(30, input_dim=40, kernel_regularizer=regularizers.l2(0), activation='relu'))
    model.add(Dense(25, kernel_regularizer=regularizers.l2(0), activation='relu'))
    #model.add(Dense(25, kernel_regularizer=regularizers.l2(0.0005), activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #class_weight makes false positives less desirable
    model.fit(train[0], train[1], class_weight={0: 10, 1: 1}, epochs=120, batch_size=32, verbose = 0)

    accuracy = model.evaluate(train[0], train[1], verbose = 0)
    print("train: " + str(accuracy[1]*100))
    accuracy = model.evaluate(validation[0], validation[1], verbose = 0)
    print("validation: " + str(accuracy[1]*100))


    #calculate prediction
    predictions = model.predict(validation[0])
    predictions = predictions.tolist()

    #round predictions
    rounded = []
    for prediction in predictions:
        if prediction[0] > threshold:
            rounded.append(1)
        else:
            rounded.append(0)

    #get real cancer value
    real = validation[1]

    accuracy = 0
    for count in range(len(rounded)):
        if real[count] == 0 and rounded[count] != 0:
            falsePositive += 1
        elif real[count] == rounded[count]:
            accuracy += 1
    print("accuracy?: " + str(accuracy/len(rounded)))
    print("false positives: " + str(falsePositive))

print(threshold)
print()

#do the same but with testing data

#calculate prediction
predictions = model.predict(test[0])
predictions = predictions.tolist()

#round predictions
rounded = []
for prediction in predictions:
    if prediction[0] > threshold:
        rounded.append(1)
    else:
        rounded.append(0)

#get real cancer value
real = test[1]

accuracy = 0
falsePositive = 0
for count in range(len(rounded)):
    if real[count] == 0 and rounded[count] != 0:
        falsePositive += 1
    elif real[count] == rounded[count]:
        accuracy += 1
print("real accuracy: " + str(accuracy/len(rounded)))
print("false positives: " + str(falsePositive))
