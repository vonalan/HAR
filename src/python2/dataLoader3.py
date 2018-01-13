#-*- coding: UTF-8 -*-

import numpy
import cPickle
import datetime
import itertools 


def appendRC(): 
    pass


def itov(n, actions):
    vec = []
    for i in xrange(len(actions)):
        vec.append(0)
    vec[n - 1] = 1

    return vec


def loadDataSet(fileName, actions, path):
    inputSet = [] 
    targetSet = []
    flags = [] 
    
    inputTemp = []
    cate = []
    flag = "null"
    with open(fileName, 'r') as fn: 
        for lineFile in fn.readlines(): 
            curLine = lineFile.strip().split()
            if len(curLine) != 0:
                try:
                    map(float, curLine)
                except Exception:
                    print str(datetime.datetime.now())[:19] + " ValueError: could not convert string to float: ", curLine
                    for i in xrange(len(actions)):
                        if actions[i] in lineFile: # ucf-Diving-Side-001-2538-5_70133_h
                            # # ucf
                            # if 'jpeg' in lineFile: # ucf-Diving-Side-001-jpeg_o
                            #     flag = 'jpeg'
                            #     # print flag
                            # elif 'jpeg' not in lineFile: # ucf-Diving-Side-001-2538-5_70133_h
                            #     flag = 'origin'
                            #     # print flag
                            # else:
                            #     pass

                            # kth
                            lineFile = curLine
                            if lineFile[-1][-1] == 'h':
                                flag = 'hflip'
                            elif lineFile[-1][-1] == 'o':
                                flag = 'origin'
                            else:
                                pass
                            cate = i + 1
                        else: # the first line: # point-type y-norm x-norm t-norm y x t sigma2 tau2 dscr-hog(72) dscr-hof(90)
                            pass 
                else:
                    fltLine = map(float, curLine)
                    inputTemp.append(fltLine[9:])
            else:
                inputM = numpy.mat(inputTemp)
                inputSet.append(inputM)
                inputTemp = []
                cateL = itov(cate, actions)
                targetSet.append(cateL) # !!! itov()
                flags.append(flag)
                
    '''ugly code ugly code '''
    inputM = numpy.mat(inputTemp)
    inputSet.append(inputM)
    # inputTemp = []
    cateL = itov(cate, actions)
    targetSet.append(cateL)  # !!! itov()
    flags.append(flag)


    assert len(targetSet) == len(flags), len(targetSet) == len(flags)
    print len(targetSet), len(flags)
    print len(inputSet), numpy.shape(inputSet[0])

    # save object
    ucfdata = [flags, inputSet, targetSet]
    cpklsave(ucfdata, path)

    return flags, inputSet, targetSet


def cpklload(path):
    with open(path, 'rb') as fs:
        objs = cPickle.load(fs)

    return objs


def cpklsave(objs, path):
    with open(path, 'wb') as fs:
        cPickle.dump(objs, fs)

    print str(datetime.datetime.now())[:19] + " " + path + " is saved! "


def saveMatrix(matrixNames, matrixFiles):
    for matrixName, matrixFile in zip(matrixNames, matrixFiles):
        numpy.save(matrixFile, matrixName)
        print str(datetime.datetime.now())[:19] + " " + matrixFile+ " is saved! shape: " + str(numpy.shape(matrixName))


def saveObjects(objectNames, objectFiles): 
    for objectName, objectFile in zip(objectNames, objectFiles): 
        with open(objectFile, "wb") as File: 
            cPickle.dump(objectName, File)
        
        print str(datetime.datetime.now())[:19] + " " + objectFile + " is saved! "


if __name__ == '__main__':
    actions = ['walk-simple', 'walk-complex']
    filename = 'walk-samples-stip.txt'
    filename2 = 'fucking.txt'
    gzPath1 = "../data/pwd/ucf.cpkl.gz"
    loadDataSet(filename, actions, gzPath1)
    # flags, IDX, countLine, inputSet, targetSet = gzload(gzPath1)
else: 
    print str(datetime.datetime.now())[:19] + ' importing module dataLoader3 ... '


# end
