#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
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
total = [totalData[:, 0:40], totalData[:, 41]]
total[1] = np_utils.to_categorical(total[1])
print(total[1])
#create file to write in
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/CrossValidation/results.csv')
file = open(filename, 'w')

average = 0
falsePositive = 0
model = Sequential()
model.add(Dense(30, input_dim=40, kernel_regularizer=regularizers.l2(0), activation='relu'))
model.add(Dense(25, kernel_regularizer=regularizers.l2(0), activation='relu'))
#model.add(Dense(25, kernel_regularizer=regularizers.l2(0.0005), activation='relu'))
model.add(Dense(8, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#class_weight makes false positives less desirable
estimator = KerasClassifier(model, epochs=120, batch_size=32, verbose=0)
kfold = KFold(n_splits=10, shuffle=True, random_state = 7)
model.fit(total[0], total[1], epochs=120, batch_size=32, verbose = 0)
accuracy = model.evaluate(total[0], total[1], verbose = 0)
print(accuracy[1]*100)
