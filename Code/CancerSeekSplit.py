#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.ensemble import RandomForestClassifier
#import matplotlib.pyplot as plt
import numpy
import os

numpy.random.seed(7)

#get complete data set
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv')
totalData = numpy.loadtxt(filename, delimiter=",")

#randomly split data into train, validation, test
#trainData, validationData, testData = getData(filename, 0.1, 0.2, False)

'''filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Training Data.csv' )
trainData = numpy.loadtxt(filename, delimiter=",")
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Test Data.csv')
testData = numpy.loadtxt(filename, delimiter=",")'''

#split data
total = [totalData[:, 0:40], totalData[:, 40], totalData[:, 41]]
#define 10-fold cross validation
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)


previousAccuracy = [0, -500]
parameters = [0.0004, 150]
threshold = 0.96
update = [0.0001, 20]
optimizeIndex = 0
go = True
switch = False
num = 0

while go:
    average = [0, 0]
    falsePositive = 0
    for train, test in kfold.split(total[0], total[1]):
        model = Sequential()
        model.add(Dense(30, input_dim=40, kernel_regularizer=regularizers.l2(0), activation='relu'))
        model.add(Dense(25, kernel_regularizer=regularizers.l2(parameters[0]), activation='relu'))
        #model.add(Dense(25, kernel_regularizer=regularizers.l2(0.0005), activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        #class_weight makes false positives less desirable
        model.fit(total[0][train], total[1][train], class_weight={0: 1, 1: 1}, epochs=parameters[1], batch_size=32, verbose = 0)

        '''accuracy = model.evaluate(total[0][train], total[1][train], verbose = 0)
        print("train: " + str(accuracy[1]*100))
        accuracy = model.evaluate(total[0][test], total[1][test], verbose = 0)
        print("total: " + str(accuracy[1]*100))'''


        #calculate prediction
        predictions = model.predict(total[0][test])
        y_pred_keras = predictions.ravel()
        fpr, tpr, thresholds = roc_curve(total[1][test], y_pred_keras)
        predictions = predictions.tolist()

        #round predictions
        rounded = []
        for prediction in predictions:
            if prediction[0] > threshold:
                rounded.append(1)
            else:
                rounded.append(0)

        #add cancer types
        types = total[2][test]

        #add real cancer value
        real = total[1][test]

        #change to add cancer type
        accuracy = 0
        for count in range(len(rounded)):
            if real[count] == 0 and rounded[count] != 0:
                falsePositive += 1
            elif real[count] == rounded[count]:
                accuracy += 1
            line = str(real[count]) + "," + str(rounded[count]) + "," + str(types[count])
        accuracy /= len(rounded)
        print("accuracy " + str(accuracy))
        accuracy = auc(fpr, tpr)
        #print("real accuracy: " + str(accuracy) + "\n")
        average[0] += accuracy

    average[1] = -1*falsePositive #store accuracy average and number of false positives (negative for comparison)
    if falsePositive > 10 and threshold < 0.99: #if false positives is bad use that as metric
        if num == 0:
            previousAccuracy[1] = -500
            switch = True
        else:
            switch = False
        num = 1
    else:
        if num == 1:
            print("reset cut")
            switch = True
            #previousAccuracy[0] = 0
        else:
            switch = False
        num = 0

    average[0] /= 10

    if average[num] > previousAccuracy[num] or num == 1: #solved problem by making false positive negative
        previousAccuracy[0] = average[0]
        previousAccuracy[1] = average[1]
        if num == 1: #increases thresholds for false positives
            if threshold >= 0.99:
                print("maximum threshold " + str(threshold))
            else:
                threshold += 0.01
                print("cut " + str(threshold))
        else:
            parameters[optimizeIndex] += update[optimizeIndex]
    else:
        if parameters[optimizeIndex] > 0 and switch == False:
            parameters[optimizeIndex] -= update[optimizeIndex]
        if num != 1:
            optimizeIndex += 1
        if optimizeIndex >= 2:
            if falsePositive < 10:
                go = False
                break
            optimizeIndex = 0
        if num != 1:
            parameters[optimizeIndex] += update[optimizeIndex]

    print(average)
    #print(falsePositive)
    print(parameters)
    print()

print("final")
print(parameters)
