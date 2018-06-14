#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from sklearn.model_selection import StratifiedKFold
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

num = 1
average = 0
for train, test in kfold.split(total[0], total[1]):
    model = Sequential()
    model.add(Dense(45, input_dim=40, kernel_regularizer=regularizers.l2(0), activation='relu'))
    model.add(Dense(55, kernel_regularizer=regularizers.l2(0), activation='relu'))
    model.add(Dense(45, kernel_regularizer=regularizers.l2(0), activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #class_weight makes false positives less desirable
    model.fit(total[0][train], total[1][train], class_weight={0: 1, 1: 0.1}, epochs=100, batch_size=32, verbose = 0)

    '''accuracy = model.evaluate(train[0], train[1], verbose = 0)
    print("train: " + str(accuracy[1]*100))'''
    accuracy = model.evaluate(total[0][test], total[1][test], verbose = 0)
    print("total: " + str(accuracy[1]*100) + "\n")

    #calculate prediction
    predictions = model.predict(total[0][test])
    predictions = predictions.tolist()
    #round predictions
    rounded = []
    for prediction in predictions:
        rounded.append(round(prediction[0]))

    #add cancer types
    types = total[2][test]

    #add real cancer value
    real = total[1][test]

    #create file to write in
    filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/CrossValidation/results ' + str(num) + '.csv')
    file = open(filename, 'w')
    #change to add cancer type
    for count in range(len(rounded)):
        line = str(real[count]) + "," + str(rounded[count]) + "," + str(types[count])
        file.write(line + "\n")
    file.close()
    num += 1
    average += accuracy[1]*100
print(average/10)
