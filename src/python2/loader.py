#-*- coding: UTF-8 -*-

import numpy
import cPickle
import datetime
import utilities


def merge(prefix, num):
    labels = []
    attrs = []
    for i in xrange(num):
        fn = prefix + '_' + str(i + 1) + '.cpk'
        path = utilities.getPath(fn)
        object = loadObject(path)
        lbs, ats = object[2], object[3]
        labels += lbs
        attrs += ats
    labelsM = numpy.mat(labels)
    attrsM = numpy.mat(attrs)
    obj = [labelsM, attrsM]
    path = utilities.getPath(prefix + '.cpk')
    saveObjects([obj], [path])


def head(fn1, fn2, num):
    rf = open(fn1, 'r')
    wf = open(fn2, 'w')
    count = 1
    for lineFile in rf.readlines():
        wf.write(lineFile)
        
        if (count > 10):
            break 
        count += 1
    wf.close()
    rf.close()


def visualize(filename):
    info = []
    attribute = []

    rf = open(filename, 'r')
    count = 1
    for lineFile in rf.readlines():
        strLine = lineFile.strip().split()

        strLine0 = strLine[0]
        curLine0 = strLine0.strip().split(',')
        curLine = [curLine0[-1]] + strLine[1:]

        cate = curLine0[0][:6]
        idx = int(curLine0[0][6:])
        label = int(curLine0[1])
        curInfo = [cate, idx, label]

        try:
            map(float, curLine)
        except Exception:
            print str(datetime.datetime.now())[:19] + " ValueError: could not convert string to float: ", curLine
        else:
            fltLine = map(float, curLine)
            arrLine = numpy.array(fltLine)
            attr = arrLine.reshape((15, 4, 101, 101, 1))
            attribute.append(fltLine)
            info.append(curInfo)
            print count
        count += 1


def load(fn1, s1, s2, post, size):
    names = []
    index = []
    labels = []
    attrs = []

    with open(fn1, 'r') as rf:
        for lineFile in rf.readlines():
            strLine = lineFile.strip().split(',')
            info, label, attr = strLine[0], strLine[1], strLine[2]

            sname, sidx = info[:s1], info[s2:]
            curattr = attr.strip().split()

            try:
                map(float, curattr)
            except Exception:
                print utilities.fetchTime() + " ValueError: could not convert string to float: ", curattr
            else:
                vname = sname + post
                names.append(vname)

                idx = int(sidx)
                # curinfo = [idx]
                index.append(idx)

                fltlabel = float(label)
                # vfltlabel = [fltlabel]
                labels.append(fltlabel)

                fltattr = map(float, curattr)
                attrs.append(fltattr)
                # print count
                ''''''
                if(idx%size == 0):
                    dataset = [names, index, labels, attrs]
                    # for item in dataset:
                      #   print utilities.fetchTime() + ' ', len(item), len(item[0])
                    ''''''
                    iter = idx/size
                    fn2 = utilities.getPath(vname + '_' + str(iter) + '.cpk')
                    saveObjects([dataset], [fn2])

                    names =[]
                    index = []
                    labels = []
                    attrs = []

    assert (len(names) or len(index) or len(labels) or len(attrs)) == 0


def saveMatrix(matrixName, matrixFile):
    numpy.save(matrixFile, matrixName)
    print str(datetime.datetime.now())[:19] + " " + matrixFile+ " is saved! shape: " + str(numpy.shape(matrixName))


def saveMatrices(matrixNames, matrixFiles): 
    for matrixName, matrixFile in zip(matrixNames, matrixFiles):
        numpy.save(matrixFile, matrixName)
        print str(datetime.datetime.now())[:19] + " " + matrixFile+ " is saved! shape: " + str(numpy.shape(matrixName))

        
def loadMatrix(matrixFile): 
    matrix = numpy.load(matrixFile)
    print str(datetime.datetime.now())[:19] + " " + matrixFile+ " is loaded! shape: " + str(numpy.shape(matrixName))
    return matrix 


def loadMatrices(matrixFiles): 
    matrices = [] 
    for matrixFile in matrixFiles: 
        matrix = numpy.load(matrixFile)
        matrices.append(matrix)
        print str(datetime.datetime.now())[:19] + " " + matrixFile+ " is loaded! shape: " + str(numpy.shape(matrixName))
    return matrices


def saveObject(objectName, objectFile):     
    with open(objectFile, "wb") as File:
        cPickle.dump(objectName, File)
    
    print str(datetime.datetime.now())[:19] + " " + objectFile + " is saved! "


def saveObjects(objectNames, objectFiles): 
    for objectName, objectFile in zip(objectNames, objectFiles): 
        with open(objectFile, "wb") as File:
            cPickle.dump(objectName, File)
        
        print str(datetime.datetime.now())[:19] + " " + objectFile + " is saved! "


def loadObject(filename):
    object = []
    with open(filename, 'r') as rf:
        names, index, labels, attrs = cPickle.load(rf)
        object += [names, index, labelst, attrs]
        print str(datetime.datetime.now())[:19] + " " + filename + " is loaded! "
    return object

    
def loadObjects(filenames):
    objects = []
    for fn in filenames:
        with open(fn, 'r') as rf:
            names, index, labels, attrs = cPickle.load(rf)
            obj = [names, index, labels, attrs]
            objects.append(obj)
            print str(datetime.datetime.now())[:19] + " " + filename + " is loaded! "
    return objects


if __name__ == '__main__':
    fn1 = utilities.getPath('testA.txt')
    fn2 = utilities.getPath('samples_testA.txt')
    load(fn2, 2)
else: 
    print str(datetime.datetime.now())[:19] + ' importing module loader ... '


# end
