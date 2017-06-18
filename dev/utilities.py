# -*- coding:utf-8 -*-

import numpy as np 


def sigmoid(weightedSum): 
    return 1.0/(1.0 + np.exp(weightedSum))


def sigmoid_prime(weightedSum):
    sp = np.multiply(sigmoid(weightedSum), (1 - sigmoid(weightedSum)))
    return sp
    # return np.multiply(sigmoid(weightedSum), (1 - sigmoid(weightedSum))) # warch out! Hadamard product!!!


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

