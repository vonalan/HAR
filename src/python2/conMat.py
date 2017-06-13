#-*- coding: UTF-8 -*- 
# generating confused matrix! 

import numpy 
import dataProcess
from sklearn.metrics import confusion_matrix

def ConMat(output, target):
    assert numpy.shape(output) == numpy.shape(target) 
    
    m, n = numpy.shape(target) 
    cMat = numpy.zeros((n, n))
    
    outputI = dataProcess.ftoi(output)
    for i in xrange(m):
        o = numpy.nonzero(outputI[i,:] != 0)[1]
        t = numpy.nonzero(target[i,:] != 0)[1]
        cMat[o,t] += 1

    print cMat
    return cMat

def ConMat2(output, target):
    m, n = numpy.shape(target)
    cMat = numpy.zeros((n, n))

    outputI = dataProcess.ftoi(output)
    os = numpy.nonzero(outputI != 0)[1]
    ts = numpy.nonzero(target != 0)[1]

    for o, t in zip(os, ts):
        cMat[o,t] += 1

    print cMat
    return cMat

def metrics(cm, threshold = 0.65):
    trace = numpy.trace(cm)
    total = numpy.sum(cm)
    acc = trace/total

    sumR = numpy.sum(cm, axis = 1)
    sumC = numpy.sum(cm, axis = 0)
    
    TP = numpy.diag(cm)
    FP = sumC - TP
    FN = sumR - TP
    TN = trace - TP

    TPR = TP/sumC
    idxcx = numpy.nonzero(TPR >= threshold)[0]
    idxsx = numpy.argsort(TPR) # ascend

    idxc = [i for i in idxsx if i not in idxcx]
    
    cms = cm - 0
    for i in xrange(len(cms)): 
        cms[i,i] = -1
    print cms

    idxr = numpy.argmax(cms, axis = 0)[idxc]

    pairs = []
    for r, c in zip(idxr, idxc):
        p = (r,c)
        pairs.append(p)

    print pairs
    return pairs
    

if __name__ == '__main__': 
    a = numpy.mat([[1, 0, 0, 0],[0, 0, 1, 0],[0, 1, 0, 0],[0, 0, 0, 1],[1, 0, 0, 0],[0, 0, 1, 0]])
    b = numpy.mat([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 0, 1],[0, 0, 1, 0],[1, 0, 0, 0],[0, 1, 0, 0]])
    cmat2 = ConMat2(a, b)

    cmat2[1,1] = 1
    cmat2[3,3] = 1
    print cmat2

    hi = metrics(cmat2)
    
# end 
