#-*- coding: UTF-8 -*-

import os
import datetime
import itertools
import numpy
import pp
import util
import dataLoader3
import classifier
import cluster
import splitter


# load and save data
def reload(stipfile, actions, dbname):     
    path1 = util.getPath(dbname + ".cpkl")
    if not os.path.exists(path1):
        print str(datetime.datetime.now())[:19] + " loading datasets ... "
        flags, inputSet, targetSet = dataLoader3.loadDataSet(stipfile, actions, path1)
    else:
        util.exPath([path1])
        flags, inputSet, targetSet = dataLoader3.cpklload(path1)

    return flags, inputSet, targetSet


#  split for old-version-splitter
'''*********************************************************'''
def split1(r, actions, stipfile, dbname):
    path2 = util.getPath(dbname + "_origin_r" + str(r) + ".cpkl")

    if os.path.exists(path2):
        print str(datetime.datetime.now())[:19] + " Files: " + path2 + " are already exist! "
        splitlist, xtrain, xtest, xtrainM, xtestM, ytrainM, ytestM, xrandMX = dataLoader3.cpklload(path2)
    else:
        print str(datetime.datetime.now())[:19] + " splitting datasets ..., round: " + str(r)
        flags, inputSet, targetSet = reload(stipfile, actions, dbname)
        '''*********************************************************'''
        splitlist, xtrain, xtest, xtrainM, xtestM, ytrainM, ytestM, xrandMX = splitter.splitDataSet(actions, flags, inputSet, targetSet, path2)

    return splitlist, xtrain, xtest, xtrainM, xtestM, ytrainM, ytestM, xrandMX


#  split for new-version-splitter
'''*********************************************************'''
def split2(r, actions, stipfile, dbname):
    path2 = util.getPath(dbname + "_origin_r" + str(r) + ".cpkl")

    if os.path.exists(path2):
        print str(datetime.datetime.now())[:19] + " Files: " + path2 + " are already exist! "
        splitlist, ctrain, ctest, ctrainM, ctestM, xtrainM, xtestM, ytrainM, ytestM, xrandMX = dataLoader3.cpklload(path2)
    else:
        print str(datetime.datetime.now())[:19] + " splitting datasets ..., round: " + str(r)
        flags, inputSet, targetSet = reload(stipfile, actions, dbname)
        '''*********************************************************'''
        splitlist, ctrain, ctest, ctrainM, ctestM, xtrainM, xtestM, ytrainM, ytestM, xrandMX = splitter.splitDataSet(actions, flags,inputSet, targetSet, path2)

    return splitlist, ctrain, ctest, ctrainM, ctestM, xtrainM, xtestM, ytrainM, ytestM, xrandMX


#  cluster, for old-version-splitter
'''*********************************************************'''
def cluster1(r, KList, actions, stipfile, dbname):
    path4 = util.getPath(dbname + "_ycobjs_r" + str(r) + ".cpkl")

    '''bitter of changing api frequently'''
    '''*********************************************************'''
    splitlist, xtrain, xtest, xtrainM, xtestM, ytrainM, ytestM, xrandMX = split1(r, actions, stipfile, dbname)

    if not os.path.exists(path4):
        print str(datetime.datetime.now())[:19] + " counting datasets ..., round: " + str(r)
        ctrain, ctest = splitter.count(xtrain, xtest)
        ycobjs = [ctrain, ctest, ytrainM, ytestM]
        dataLoader3.cpklsave(ycobjs, path4)
    else:
        util.exPath([path4])
    
    '''************************************************************************************************'''
    ctrain, ctest, ytrainM, ytestM = dataLoader3.cpklload(path4)            
    if numpy.shape(xtrainM)[0] > 100000:
        '''idx = idxrandom(numpy.shape(xtrainM)[0], 10000)'''
        idx = splitter.idxrandom(numpy.shape(xtrainM)[0], 100000)
        xrandMX2 = xtrainM[idx,:]
    else:
        xrandMX2 = xtrainM
        
    print str(datetime.datetime.now())[:19] + " The shape of xrandMX2 is : " + str(numpy.shape(xrandMX2))
    '''************************************************************************************************'''
    
    for k in KList:
        path3 = util.getPath(dbname + "_bow" + "_r" + str(r) + "_k" + str(k) + ".cpkl")
        
        if not os.path.exists(path3):
            cluster.kMeans(r, k, ctrain, ctest, xtrainM, xtestM, xrandMX2, path3)
        else:
            util.exPath([path3])
    '''bitter of changing api frequetly'''


#  cluster, for new-version-splitter
'''*********************************************************'''
def cluster2(r, KList, actions, stipfile, dbname):
    path4 = util.getPath(dbname + "_ycobjs_r" + str(r) + ".cpkl")

    '''bitter of changing api frequetly'''
    '''*********************************************************'''
    splitlist, ctrain, ctest, ctrainM, ctestM, xtrainM, xtestM, ytrainM, ytestM, xrandMX = split2(r, actions, stipfile, dbname)

    if not os.path.exists(path4):
        ycobjs = [ctrainM, ctestM, ytrainM, ytestM]
        dataLoader3.cpklsave(ycobjs, path4)
    else:
        util.exPath([path4])

    for k in KList:
        path3 = util.getPath(dbname + "_bow" + "_r" + str(r) + "_k" + str(k) + ".cpkl")

        if not os.path.exists(path3):
            cluster.kMeans(r, k, ctrain, ctest, xtrainM, xtestM, xrandMX, path3)
        else:
            util.exPath([path3])
    '''bitter of changing api frequetly'''
