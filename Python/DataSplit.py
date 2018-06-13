#!/usr/bin/env python3

import numpy
import random

def getData(filename, testPercentage, validationPercentage, validation):
    data = numpy.loadtxt(filename, delimiter=",")
    testDataLength = int(testPercentage*len(data))
    validationDataLength = int(validationPercentage*len(data))
    testData = []

    for i in range(testDataLength):
        num = random.randint(0, len(data)-1)
        testData.append(data[num])
        data = numpy.delete(data, num, 0)

    validationData = []
    if (validation == True):
        for i in range(validationDataLength):
            num = random.randint(0, len(data)-1)
            validationData.append(data[num])
            data = numpy.delete(data, num, 0)

    validationData = numpy.asarray(validationData)
    testData = numpy.asarray(testData)
    return data, validationData, testData
