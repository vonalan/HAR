#-*- coding: utf-8 -*- 

import numpy as np 
import scipy.spatial.distance as sciDist


def sigmoid(weightedSum): 
    return 1.0/(1.0 + numpy.exp(weightedSum))


def sigmoid_prime(weightedSum):
    sp = numpy.multiply(sigmoid(weightedSum), (1 - sigmoid(weightedSum)))
    return sp
    # return numpy.multiply(sigmoid(weightedSum), (1 - sigmoid(weightedSum))) # warch out! Hadamard product!!!


# !!! redefine feedforward function for RBFNN 
def run_rbfnn(trainX, trainY, W, U, V):
    D = np.power(sciDist.cdist(trainX, U), 2)
    Z = np.exp(D/np.transpose((-2 * np.power(V, 2)))) # how to implement element-wise operation?
    A = np.dot(Z, W)
    assert np.shape(A) == np.shape(trainY)
    return A 


# !!! redefine feedforward function for MLPNN 
def run_mlpnn(weights, biases, activation):
    for weight, bias in zip(weights, biases):
        activation = sigmoid(np.dot(weight, activation) + bias) # bias, bug!!!
    return activation


# outline of LGEM calculating
def calcSTSM(trainX, trainY, W, U, V, Q):
    deltaX = np.random.uniform(-Q, Q, (1000, np.shape(trainX)[1]))
    H = np.shape(deltaX)[0]

    trainOut = run_rbfnn(trainX, trainY, W, U, V)
    STSM = np.mat(np.zeros(np.shape(trainY)))
    for i in range(H):
        deltaOut = drun_rbfnn(trainX + deltaX[i,:], trainY, W, U, V)
        STSM = STSM + np.power((deltaOut - trainOut), 2)

    STSM = STSM/H
    meanSTSM = np.mean(STSM, axis = 0)

    return meanSTSM