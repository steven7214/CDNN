#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from sklearn.model_selection import StratifiedKFold
import numpy
import os

numpy.random.seed(7)


#define 10-fold cross validation
kfold = StratifiedKFold(n_splits=10, shuffle=False, random_state=7)
valueList = []
tempList = []


#get normal data set
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Cancers2/Normal.csv')
    normalData = numpy.loadtxt(filename, delimiter=",")

fileNames = ['Breast', 'Colorectum', 'Liver', 'Lung', 'Ovary', 'Pancreas', 'UpperGI']
cancerData = [[],[],[],[],[],[],[]]
for j in range(7)

    #get cancer data set
    nameOfFile = 'Data/CancerSEEK/Cancers2/' + fileNames[j] + '.csv'
    filename = os.path.join(os.getcwd(), '..', nameOfFile)
    cancerData[j] = numpy.loadtxt(filename, delimiter=",")

    tempList = []
    for trainPositions, testPositions in kfold.split(cancerData[j][:, 0:40], cancerData[j][:, 40]):
        tempList.append(testPositions)
    valueList.append(tempList)

for trainPositions, testPositions in kfold.split(normalData[:, 0:40], normalData[:, 40]):
    tempList.append(testPositions)
valueList.append(tempList)

#create file to write in
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/CrossValidation/results.csv')
file = open(filename, 'w')

for x in range(7)
    falsePositive = 0
    totalAccuracy = 0
    wrong = 0
    total = 0
    for y in range(10)

        #split data
        normal = [normalData[:, 0:40][valueList[7][y]], normalData[:, 40][valueList[7][y]]]
        cancer = [cancerData[x][:, 0:40][valueList[x][y]], cancerData[x][:, 40][valueList[x][y]]]
        ends = [normalData[:, 41],[cancerData[x][:, 41],]
        train = [numpy.vstack((normal[0],cancer[0])), numpy.hstack((normal[1],cancer[1]))]
        test = [numpy.vstack((normal[0],cancer[0])), numpy.hstack((normal[1],cancer[1])),numpy.hstack((ends[0],ends[1]))]
	for z in range(6)
            r=7-z
            tempData = [cancerData[r][:, 0:40][valueList[r][y]], cancerData[r][:, 40][valueList[r][y]], cancerData[r][:, 41][valueList[r][y]]]
            test = [numpy.vstack((test[0],tempData[0])), numpy.hstack((test[1],tempData[1])),numpy.hstack((test[2],tempData[2]))]

        model = Sequential()
        model.add(Dense(30, input_dim=40, kernel_regularizer=regularizers.l2(0), activation='relu'))
        model.add(Dense(25, kernel_regularizer=regularizers.l2(0), activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        #class_weight makes false positives less desirable
        model.fit(train[0], train[1], class_weight={0: 1, 1: 1}, epochs=120, batch_size=32, verbose = 0)

        accuracy = model.evaluate(train[0], train[1], verbose = 0)
	totalAccuracy += accuracy[1]*100

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
        for count in range(len(rounded)):
            if types[count] == (x+1) and rounded[count] == 0:
                total += 1
                if rounded[count] == 0:
                    wrong += 1
            if real[count] == 0 and rounded[count] != 0:
                falsePositive += 1
            line = str(real[count]) + "," + str(rounded[count]) + "," + str(types[count])
            file.write(line + "\n")

    accuracy = ((total-wrong)/total)*100
    print(fileNames[x] + "\n")
    print("Average test accuracy: " + str(totalAccuracy/10) + "\n")
    print("Accuracy: " + str(accuracy) + "\n")
    print("False positives: " + str(falsePositive) + "\n\n\n")
    file.write("\n\n\n")
    
file.close()





























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

