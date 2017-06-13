#-*- coding: UTF-8 -*- 
                                                                        
import random
import datetime
import numpy
import split
import dataLoader3


def itov(n, actions):
    vec = [] 
    for i in xrange(len(actions)):
        vec.append(0) 
    vec[n-1] = 1


    return vec


def lstols(ytrain, actions):
    vecls = [] 
    for y in ytrain: 
        vec = itov(y, actions)
        vls = [vec]
        vecls.append(vls)
    return vecls


def lstomat(xtrain):
    xtrainM = numpy.mat(numpy.zeros((0, numpy.shape(xtrain[0])[1])))

    for x in xtrain:
        xtrainM= numpy.concatenate((xtrainM, x), axis = 0)
    
    return xtrainM

'''***************************************************'''
def countline(xtrain, xtest): 
    ctrain, ctest = [], []
    for x in xtrain: 
        ctrain.append(numpy.shape(x)[0])
    for x in xtest: 
        ctest.append(numpy.shape(x)[0])

    return ctrain, ctest
'''***************************************************'''

def idxrandom(total, num): 
    totalist = [i for i in xrange(total)]
    clip = random.sample(totalist, num)
    left = [i for i in totalist if i not in clip]
    
    return clip

'''*********************************************************'''
def splitDataSet(actions, flags, inputSet, targetSet, path, nsample = 100000): 
    addlist = split.mklist(actions)
    
    '''*********************************************************'''
    newtarget = []
    for j in xrange(len(targetSet)):
        if flags[j] == 'origin':
            newtarget.append(targetSet[j])
    '''*********************************************************'''
    
    total, vclist = split.vcount2(newtarget, actions)
    splitlist = split.split(vclist) # spliting: train/test = 2
    # splitlist = [([1,0], [2]), ([1,2], [0])]

    xtrain, ytrain, ctrain = [], [], []
    xtest, ytest, ctest = [], [], []
    for i in xrange(len(actions)): 
        for j in xrange(len(targetSet)):
            if flags[j] == 'origin': 
                x = inputSet[j] # mat
                y = targetSet[j] # ls
                if y == itov(i + 1, actions):
                    if addlist[i] in splitlist[i][0]: 
                        xtrain.append(x)
                        ytrain.append(y)
                        ctrain.append(numpy.shape(x)[0])
                    elif addlist[i] in splitlist[i][1]: 
                        xtest.append(x)
                        ytest.append(y)
                        ctest.append(numpy.shape(x)[0])
                    else: 
                        # raise Exception("idx is out of range! ")
                        pass 
                    addlist[i] += 1
                else: 
                    pass 
            else:
                pass 

    xtrainM = lstomat(xtrain)
    xtestM = lstomat(xtest)
    ytrainM = numpy.mat(ytrain)
    ytestM = numpy.mat(ytest)
    ctrainM = numpy.transpose(numpy.mat(ctrain))
    ctestM = numpy.transpose(numpy.mat(ctest))
    
    '''***************************************************'''
    if numpy.shape(xtrainM)[0] > nsample:
        '''idx = idxrandom(numpy.shape(xtrainM)[0], 10000)'''
        idx = idxrandom(numpy.shape(xtrainM)[0], nsample)
        xrandMX = xtrainM[idx,:]
    else:
        xrandMX = xtrainM
    '''***************************************************'''

    print len(xtrain), len(xtest), len(ytrain), len(ytest), len(ctrain), len(ctest)
    print numpy.shape(xtrainM), numpy.shape(xtestM), numpy.shape(xrandMX)
    
    data = [splitlist, ctrain, ctest, ctrainM, ctestM, xtrainM, xtestM, ytrainM, ytestM, xrandMX]
    dataLoader3.cpklsave(data, path)

    """ctrainM, ctestM are also need in AutoNorm procedure """
    return splitlist, ctrain, ctest, ctrainM, ctestM, xtrainM, xtestM, ytrainM, ytestM, xrandMX


if __name__ == '__main__':
    pass
else:
    print str(datetime.datetime.now())[:19] + " importing module splitter ... "


# end    
