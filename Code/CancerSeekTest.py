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

regularizer = [0, 0.0005, 150]
node = 5

previousAccuracy = 0
while True:
    average = 0
    falsePositive = 0
    for train, test in kfold.split(total[0], total[1]):
        model = Sequential()
        model.add(Dense(30, input_dim=40, kernel_regularizer=regularizers.l2(regularizer[0]), activation='relu'))
        model.add(Dense(25, kernel_regularizer=regularizers.l2(regularizer[1]), activation='relu'))
        model.add(Dense(node, kernel_regularizer=regularizers.l2(0.002), activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        #class_weight makes false positives less desirable
        model.fit(total[0][train], total[1][train], class_weight={0: 1, 1: 1}, epochs=regularizer[2], batch_size=32, verbose = 0)

        #calculate prediction
        predictions = model.predict(total[0][test])
        predictions = predictions.tolist()
        #round predictions
        rounded = []
        for prediction in predictions:
            if prediction[0] > 0.98:
                rounded.append(1)
            else:
                rounded.append(0)

        #add cancer types
        types = total[2][test]

        #add real cancer value
        real = total[1][test]


        #change to add cancer type
        bill = 0
        accuracy = 0
        for count in range(len(rounded)):
            if real[count] == 0 and rounded[count] != 0:
                bill += 1
            elif real[count] == rounded[count]:
                accuracy += 1
        accuracy /= len(rounded)
        average += accuracy
        falsePositive += bill
    if accuracy < previousAccuracy:
        break
    previousAccuracy = accuracy
    node += 5

    print()
    print(average/10)
    print(falsePositive)

print("layer")
print(node-5)
