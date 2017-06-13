import gzip 
import cPickle 
import numpy as np 
from datetime import datetime as dt 


def loadFileNames(fileList): 
    fileNames = []
    fl = open(fileList)
    for lineList in fl.readlines(): 
        curLine = lineList.strip().lstrip().rstrip()
        fileNames.append(curLine)
    return fileNames



def loadDataSet(fileNames):
    inputSet = []
    targetSet = []
    countLine = []
    for idx, filename in enumerate(fileNames):
        indicator = False
        count = 0
        flag = False
        fn = open(filename)
        for lineFile in fn.readlines(): 
            curLine = lineFile.strip().split(' ')
            fltLine = []
            try: 
                fltLine = map(float, curLine)
            except Exception:
                print str(dt.now())[:19] + " ValueError: could not convert string to float: ", curLine
                if flag:
                    target = np.zeros(6)
                    target[idx] = 1
                    targetSet.append(target)
                    print str(dt.now())[:19] + " LABEL: " + str(idx)
                    flag = not flag
                else:
                    if indicator:
                        acount = [count]
                        countLine.append(acount)
                        count = 0
                    else:
                        indicator = not indicator
                    print str(dt.now())[:19] + " NO LABEL! "
                    flag = not flag
            else:
                fltLine = map(float, curLine)
                inputSet.append(fltLine[9:])
                count = count + 1
        acount = [count]
        countLine.append(acount)
    return np.mat(inputSet), np.mat(targetSet), np.mat(countLine)



def saveMatrix(matrixNames, matrixFiles, k = 0):
    for matrixName, matrixFile in zip(matrixNames, matrixFiles):
        if k:
            matrixFile = matrixFile + str(k) + ".npy"
            np.save(matrixFile, matrixName)
            print str(dt.now())[:19] + " " + matrixFile + " is saved! shape: " + str(np.shape(matrixName))
        else:
            matrixFile = matrixFile + ".npy"
            np.save(matrixFile, matrixName)
            print str(dt.now())[:19] + " " + matrixFile+ " is saved! shape: " + str(np.shape(matrixName))



'''
def loadMatrix(matrixNames, matrixFiles):
    for matrixName, matrixFile in zip(matrixNames, matrixFiles):
        matrixFile = matrixFile + ".npy"
        matrixName = load(matrixFile)
'''


'''new''' 
def saveObject(objectNames, objectFiles, k = 0): 
    for objectName, objectFile in zip(objectNames, objectFiles): 
        objectFile = objectFile + ".cpkl.gz" 
        with gzip.open(objectFile, "wb") as File: 
            dmp = cPickle.dumps(objectName) 
            File.write(dmp) 
        print str(dt.now())[:19] + " " + objectFile + " is saved! " 


'''
def loadObject(objectName, objectFiles): 
    for objectName, objectFile in zip(objectNames, objectFiles): 
        with gzip.open(objectFile, "rb") as File: 
            objectName = cPickle.load(objsFile) 
        print str(dt.now())[:19] + " " + objectFile + " is saved! " 
''' 
'''new'''


# end
