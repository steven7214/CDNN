#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import numpy
import os

numpy.random.seed(7)

#update/Parameters
update = [5, 0.0005]

#define 10-fold cross validation
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
valueList = []
tempList = []


#get normal data set
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Cancers2/Normal.csv')
normalData = numpy.loadtxt(filename, delimiter=",")

fileNames = ['Breast', 'Colorectum', 'Liver', 'Lung', 'Ovary', 'Pancreas', 'UpperGI']
cancerData = [[],[],[],[],[],[],[]]
for j in range(7):
    #get cancer data set
    nameOfFile = 'Data/CancerSEEK/Cancers2/' + fileNames[j] + '.csv'
    filename = os.path.join(os.getcwd(), '..', nameOfFile)
    cancerData[j] = numpy.loadtxt(filename, delimiter=",")

    tempList = []
    for trainPositions, testPositions in kfold.split(cancerData[j][:, 0:40], cancerData[j][:, 40]):
        tempList.append(testPositions)
    valueList.append(tempList)
tempList = []
for trainPositions, testPositions in kfold.split(normalData[:, 0:40], normalData[:, 40]):
    tempList.append(testPositions)
valueList.append(tempList)

#create file to write in
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/CrossValidation/results.csv')
file = open(filename, 'w')
for x in range(7):
    parameters = [[15, 0], [15, 0]]
    falsePositive = 0
    totalAccuracy = 0
    num = 0
    wrong = 0
    total = 0
    previousAccuracy = 0
    optimizeIndex = [0, 0]
    optimizeAccuracy = 0
    go = True
    while go:
        for y in range(10):
            test = []
            train = []
            for z in range(10):
                normal = [normalData[:, 0:40][valueList[7][z]], normalData[:, 40][valueList[7][z]], normalData[:, 41][valueList[7][z]]]
                cancer = [cancerData[x][:, 0:40][valueList[x][z]], cancerData[x][:, 40][valueList[x][z]], cancerData[x][:, 41][valueList[x][z]]]
                if not z == y:
                    if not len(train) == 2:
                        train = [cancer[0], cancer[1]]
                    else:
                        train = [numpy.vstack((train[0],cancer[0])), numpy.hstack((train[1],cancer[1]))]
                    train = [numpy.vstack((train[0],normal[0])), numpy.hstack((train[1],normal[1]))]
                else:
                    test = [cancer[0],cancer[1],cancer[2]]
                    test = [numpy.vstack((test[0],normal[0])), numpy.hstack((test[1],normal[1])), numpy.hstack((test[2],normal[2]))]
            for s in range(7):
                other = [cancerData[s][:, 0:40][valueList[s][y]], cancerData[s][:, 40][valueList[s][y]], cancerData[s][:, 41][valueList[s][y]]]
                if not s == x:
                    test = [numpy.vstack((test[0],other[0])), numpy.hstack((test[1],other[1])), numpy.hstack((test[2],other[2]))]

            model = Sequential()
            model.add(Dense(parameters[0][0], input_dim=40, kernel_regularizer=regularizers.l2(parameters[0][1]), activation='relu'))
            model.add(Dense(parameters[1][0], kernel_regularizer=regularizers.l2(parameters[1][1]), activation='relu'))
            model.add(Dense(1, activation='sigmoid'))

            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            #class_weight makes false positives less desirable
            model.fit(train[0], train[1], class_weight={0: 1, 1: 1}, epochs=120, batch_size=32, verbose = 0)

            accuracy = model.evaluate(train[0], train[1], verbose = 0)

            num += 1
            totalAccuracy += accuracy[1]*100
            print("train: " + str(accuracy[1]*100))

            #calculate prediction
            predictions = model.predict(test[0])

            y_pred_keras = predictions.ravel()
            fpr, tpr, thresholds = roc_curve(test[1], y_pred_keras)
            aucKeras = auc(fpr, tpr)
            print("auc score: " + str(aucKeras))
            predictions = predictions.tolist()

            #set metric to auc score
            accuracy = aucKeras*100

            #round predictions
            rounded = []
            for prediction in predictions:
                if prediction[0] > 0.5:
                    rounded.append(1)
                else:
                    rounded.append(0)

            #add cancer types
            types = test[2]
            #add real cancer value
            real = test[1]

            #change to add cancer type
            for count in range(len(rounded)):
                #print(types[count])
                if types[count] == (x+1):
                    total += 1
                    if rounded[count] == 0:
                        wrong += 1
                if real[count] == 0 and rounded[count] != 0:
                    falsePositive += 1
                line = str(real[count]) + "," + str(rounded[count]) + "," + str(types[count])
                file.write(line + "\n")

            #accuracy = ((total-wrong)/total)*100 #this sets metric to number right rather than auc

            if accuracy >= previousAccuracy:
                previousAccuracy = accuracy
                parameters[optimizeIndex[0]][optimizeIndex[1]] += update[optimizeIndex[1]]
            else:
                parameters[optimizeIndex[0]][optimizeIndex[1]] -= update[optimizeIndex[1]]
                accuracy = previousAccuracy
                previousAccuracy = 0
                if optimizeIndex[1] == 1:
                    optimizeIndex[1] = 0
                    optimizeIndex[0] += 1
                else:
                    optimizeIndex[1] += 1
                if optimizeIndex[0] >= 2:
                    print("finished")
                    print(parameters)
                    #if there is improvement within the three, update and keep going
                    if accuracy - optimizeAccuracy > 0.1:
                        optimizeAccuracy = accuracy
                        optimizeIndex[0] = 0
                    #otherwise, break out of all loops
                    else:
                        print("optimized")
                        go = False
                        break

    print(fileNames[x] + "\n")
    print("Average train accuracy: " + str(totalAccuracy/num) + "\n")
    print("Accuracy: " + str(optimizeAccuracy) + "\n")
    print("False positives: " + str(falsePositive) + "\n\n\n")
    file.write("\n\n\n")
file.close()
