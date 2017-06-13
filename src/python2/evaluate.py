import datetime
import numpy
import dataProcess


def calcErr(output, targetSet):
    assert numpy.shape(output) == numpy.shape(targetSet)
    errM = numpy.power(output - targetSet, 2)
    meanErr = numpy.mean(errM, axis = 0)

    return meanErr


def calcAcc(output, targetSet):
    assert numpy.shape(output)[0] == numpy.shape(targetSet)[0]
    outputIM = dataProcess.ftoi(output) 
    errCases = numpy.sum(outputIM != targetSet)/2
    totalCases = numpy.shape(outputIM)[0]
    trueCases = totalCases - errCases

    return float(trueCases)/totalCases


def calcConMat(output, target):
    m, n = numpy.shape(target)
    cMat = numpy.zeros((n, n))

    outputI = dataProcess.ftoi(output)
    os = numpy.nonzero(outputI != 0)[1]
    ts = numpy.nonzero(target != 0)[1]

    for o, t in zip(os, ts):
        cMat[o,t] += 1

    return cMat


# outline of LGEM calculating
def calcSTSM(trainX, trainY, W, U, V, Q):
    deltaX = dataProcess.genDeltaX(Q, trainX)
    H = numpy.shape(deltaX)[0]

    trainOut = dataProcess.feedforwardRBFNN(trainX, trainY, W, U, V)
    STSM = numpy.mat(numpy.zeros(numpy.shape(trainY)))
    for i in range(H):
        deltaOut = dataProcess.feedforwardRBFNN(trainX + deltaX[i,:], trainY, W, U, V)
        STSM = STSM + numpy.power((deltaOut - trainOut), 2)

    STSM = STSM/H
    meanSTSM = numpy.mean(STSM, axis = 0)

    return meanSTSM

if __name__ == '__main__':
    pass
else:
    print str(datetime.datetime.now())[:19] + " importing module evaluate ... "

# end