#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras import regularizers
import numpy
import os
from DataSplit import getData

numpy.random.seed(7)

averageRun = 0
for i in range(5):
    #randomly split data into train, validation, test
    filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv')
    trainData, validationData, testData = getData(filename, 0.1, 0.2)

    '''filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Training Data.csv' )
    trainData = numpy.loadtxt(filename, delimiter=",")
    filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Validation Data.csv')
    validationData = numpy.loadtxt(filename, delimiter=",")
    filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Test Data.csv')
    testData = numpy.loadtxt(filename, delimiter=",")'''


    #split data
    train = [trainData[:, 0:39], trainData[:, 39]]
    validation = [validationData[:, 0:39], validationData[:, 39]]
    test = [testData[:, 0:39], testData[:, 39]]

    # Parameters: node number, epochs, regulizer
    update = [5, 10, 0.0005]

    #array to store layer parameters
    layers = []

    optimizeIndex = 0
    totalAccuracy = 0
    accuracy = 0
    temp = 0
    num = 1
    while totalAccuracy==0 or accuracy-totalAccuracy > 0.1: #loop by adding layers when there's improvement
        layers.append([20, 100, 0]) #try 45 as node start as well
        if num == 5:
            print("over fit")
            break
        #print(num)
        #print(str(optimizeIndex) + " " + str(layers[len(layers)-1][optimizeIndex]))
        totalAccuracy = accuracy
        accuracy = 0
        while optimizeIndex <= 2:
            temp = 0
            #build model
            model = Sequential()
            #model.add(Dropout(0.2, input_shape=(39,)))
            for count in range(len(layers)):
                model.add(Dense(layers[count][0], input_dim=39, kernel_regularizer=regularizers.l2(layers[count][2]), activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            #compile model
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            #fit model
            model.fit(train[0], train[1], epochs=layers[len(layers)-1][1], batch_size=32, verbose = 0)
            #evaluate model
            scores = model.evaluate(validation[0], validation[1], verbose = 0)
            temp = scores[1]*100
            #print("%s: %.2f%%\n" % (model.metrics_names[1], temp))
            #print("weights: " + str(model.layers[0].get_weights()))

            if accuracy == 0 or temp-accuracy>=0:
                accuracy = temp
                layers[len(layers)-1][optimizeIndex] += update[optimizeIndex]
            else:
                layers[len(layers)-1][optimizeIndex] -= update[optimizeIndex]
                optimizeIndex += 1
                accuracy = 0
                #print parameters
            '''    for count in range(len(layers[len(layers)-1])):
                    print(str(count) + " " + str(layers[len(layers)-1][count]) + "\n")'''


            if optimizeIndex == 3:
                model.layers.pop()
                model.layers.pop()
                model.add(Dense(layers[len(layers)-1][0], input_dim=39, kernel_regularizer=regularizers.l2(layers[len(layers)-1][2]), activation='relu'))
                model.add(Dense(1, activation='sigmoid'))
                model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
                model.fit(train[0], train[1], epochs=layers[len(layers)-1][1], batch_size=32, verbose = 0)
                accuracy = model.evaluate(validation[0], validation[1], verbose = 0)

        accuracy = accuracy[1]*100
        #print("this is bill " + str(accuracy))
        optimizeIndex = 0
        num += 1

    layers = layers[:-1]
    model = Sequential()
    for list in layers:
        model.add(Dense(list[0], input_dim=39, kernel_regularizer=regularizers.l2(list[2]), activation='relu'))
        print(str(list[0]) + " " + str(list[1]) + " " + str(list[2]))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(train[0], train[1], epochs=layers[len(layers)-1][1], batch_size=32, verbose = 0)

    accuracy = model.evaluate(train[0], train[1], verbose = 0)
    print(len(model.layers)-1)
    print("train: " + str(accuracy[1]*100))
    accuracy = model.evaluate(validation[0], validation[1], verbose = 0)
    print("validation: " + str(accuracy[1]*100))
    accuracy = model.evaluate(test[0], test[1], verbose = 0)
    print("test: " + str(accuracy[1]*100) + "\n")
    averageRun += accuracy[1]*100

print(averageRun/5)

#calculate prediction
predictions = model.predict(test[0])
#round predictions
rounded = [round(test[0]) for test in predictions]
#print(rounded)
