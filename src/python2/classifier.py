import os
import datetime
import itertools 
import pp
import util
import numpy 
import dataLoader3
import RBFNetwork 
import dataProcess


def classify(ratio, r, numCenter, alpha, Q, K, lenPara, trainY, testY, countLineTrain, countLineTest, dbname):
    results = numpy.mat(numpy.zeros((0, lenPara)))
    # objs = []

    path5 = util.getPath2(dbname + "_bow" + "_r" + str(r) + "_k" + str(K) + ".cpkl")
    # bowTrain, bowTest, centroids = dataLoader3.cpklload(path5)

    if os.path.exists(path5):
        print "\n" + str(datetime.datetime.now())[:19] + " Sequence learning for {r = " + str(r) + ", numCenter = " + str(numCenter) + ", alpha = " + str(alpha) + ", Q = " + str(Q) + ", K = " + str(K) + "} ... "
        bowTrain, bowTest, centroids = dataLoader3.cpklload(path5)

        # normalize dataset
        trainX = dataProcess.autoNorm(bowTrain, countLineTrain)
        testX = dataProcess.autoNorm(bowTest, countLineTest)

        # define the architecture of Neural Network
        indim = numpy.shape(trainX)[1]
        outdim = numpy.shape(trainY)[1]
        RBFClassifier = RBFNetwork.RBFNN(indim, numCenter, outdim, alpha, Q)

        # classifier training and testing
        RBFClassifier.train(trainX, trainY)
        trainOut = RBFClassifier.test(trainX)
        testOut = RBFClassifier.test(testX)
        print str(datetime.datetime.now())[:19] + " The classifier testing is done! the shapes of {outputTrain, outputTest} are: " + str(numpy.shape(trainOut)) + ", " + str(numpy.shape(testOut))

        '''bug bug bug'''
        results1, cmtrain, cmtest = RBFClassifier.evaluateAll(trainX, trainY, trainOut, testX, testY, testOut)
        results2 = [ratio, r, numCenter, alpha, Q, K]
        results3 = numpy.mat(results2 + results1)
        results = numpy.concatenate((results, results3), axis=0)
        # obj = [RBFClassifier, cmtrain, cmtest]
        # objs.append(obj)
        '''bug bug bug'''

        # The epoch is done!
        print str(datetime.datetime.now())[:19] + " Sequence learning for {r = " + str(r) + ", numCenter = " + str(numCenter) + ", alpha = " + str(alpha) + ", Q = " + str(Q) + ", K = " + str(K) + "} is done! " 

    else:
        print str(datetime.datetime.now())[:19] + " Files: " + path5 + " do not exist! "

    # print results, len(objs)
    return results

    
def classifyCM(ratio, r, numCenter, alpha, Q, K, lenPara, trainY, testY, countLineTrain, countLineTest, dbname):
    results = numpy.mat(numpy.zeros((0, lenPara)))
    objs = []

    path5 = util.getPath2(dbname + "_bow" + "_r" + str(r) + "_k" + str(K) + ".cpkl")
    # bowTrain, bowTest, centroids = dataLoader3.cpklload(path5)

    if os.path.exists(path5):
        print "\n" + str(datetime.datetime.now())[:19] + " Sequence learning for {r = " + str(r) + ", numCenter = " + str(numCenter) + ", alpha = " + str(alpha) + ", Q = " + str(Q) + ", K = " + str(K) + "} ... "
        bowTrain, bowTest, centroids = dataLoader3.cpklload(path5)

        # normalize dataset
        trainX = dataProcess.autoNorm(bowTrain, countLineTrain)
        testX = dataProcess.autoNorm(bowTest, countLineTest)

        # define the architecture of Neural Network
        indim = numpy.shape(trainX)[1]
        outdim = numpy.shape(trainY)[1]
        RBFClassifier = RBFNetwork.RBFNN(indim, numCenter, outdim, alpha, Q)

        # classifier training and testing
        RBFClassifier.train(trainX, trainY)
        trainOut = RBFClassifier.test(trainX)
        testOut = RBFClassifier.test(testX)
        print str(datetime.datetime.now())[:19] + " The classifier testing is done! the shapes of {outputTrain, outputTest} are: " + str(numpy.shape(trainOut)) + ", " + str(numpy.shape(testOut))

        '''bug bug bug'''
        results1, cmtrain, cmtest = RBFClassifier.evaluateAll(trainX, trainY, trainOut, testX, testY, testOut)
        results2 = [ratio, r, numCenter, alpha, Q, K]
        results3 = numpy.mat(results2 + results1)
        results = numpy.concatenate((results, results3), axis=0)
        
        '''***************************************************'''
        obj = [trainOut, testOut, cmtrain, cmtest]
        objs.append(obj)
        '''***************************************************'''
        '''bug bug bug'''

        # The epoch is done!
        print str(datetime.datetime.now())[:19] + " Sequence learning for {r = " + str(r) + ", numCenter = " + str(numCenter) + ", alpha = " + str(alpha) + ", Q = " + str(Q) + ", K = " + str(K) + "} is done! " 

    else:
        print str(datetime.datetime.now())[:19] + " Files: " + path5 + " do not exist! "

    # print results, len(objs)
    return (results, objs)


def seqLearn(cate, ratio, r, numCenterList, alphaList, QList, KList, lenPara, dbname, iter = 'ZZZ', mode = 'ZZZ'):
    # setting and starting ppservers ...  

    ppservers = ()
    ncpus = 2
    job_server = pp.Server(ncpus, ppservers = ppservers) 
    print str(datetime.datetime.now())[:19] + " Starting python parallel with", job_server.get_ncpus(), "workers. "

    paraPerm = list(itertools.product(numCenterList, alphaList, QList, KList))

    path4 = util.getPath2(dbname + "_ycobjs_r" + str(r) + ".cpkl")
    if os.path.exists(path4):
        fnResults = util.getPath2(dbname + "_results_r" + str(r) + "_" + iter + "_" + mode + ".npy")
        # fnRBFobjs = util.getPath2(dbname + "_results_r" + str(r) + "_" + iter + ".cpkl")

        if not os.path.exists(fnResults):
            ctrainM, ctestM, ytrainM, ytestM = dataLoader3.cpklload(path4)
            # ctrainM, ctestM = numpy.mat(ctrain).T, numpy.mat(ctest).T

            results = numpy.mat(numpy.zeros((0,lenPara)))
            objsRBF = []
            jobs = [job_server.submit(classify, (ratio, r, para[0], para[1], para[2], para[3], lenPara, ytrainM, ytestM, ctrainM, ctestM, dbname), (), ("numpy","dataProcess", "RBFNetwork", "dataLoader3", "datetime", "util")) for para in paraPerm]
            for job in jobs:
                # cnm = job()
                # result, obj = cnm[0], cnm[1]
                result = job()
                results =numpy.concatenate((results, result), axis = 0)
                # objsRBF = objsRBF + obj
                # results = numpy.concatenate((results, job()[0]), axis = 0)
                # objsRBF = objsRBF + job()[1]

            print "\n"
            if not numpy.shape(results)[0] == 0: 
                dataLoader3.saveMatrix([results], [fnResults])
                # dataLoader3.saveObjects([objsRBF], [fnRBFobjs])
            else: 
                util.infoErr([fnResults])
        else:
            util.exPath([fnResults])
    else:
        util.noPath([path4])
        
        
def seqLearnCM(cate, ratio, r, numCenterList, alphaList, QList, KList, lenPara, dbname, iter = 'ZZZ', mode = 'ZZZ'):
    # setting and starting ppservers ...  

    ppservers = ()
    ncpus = 2
    job_server = pp.Server(ncpus, ppservers = ppservers) 
    print str(datetime.datetime.now())[:19] + " Starting python parallel with", job_server.get_ncpus(), "workers. "

    paraPerm = list(itertools.product(numCenterList, alphaList, QList, KList))

    path4 = util.getPath2(dbname + "_ycobjs_r" + str(r) + ".cpkl")
    if os.path.exists(path4):
        fnResults = util.getPath2(dbname + "_results_r" + str(r) + "_" + iter + "_" + mode + ".npy")
        fnRBFobjs = util.getPath2(dbname + "_results_r" + str(r) + "_" + iter + "_" + mode + ".cpkl")

        if not os.path.exists(fnResults):
            ctrainM, ctestM, ytrainM, ytestM = dataLoader3.cpklload(path4)
            # ctrainM, ctestM = numpy.mat(ctrain).T, numpy.mat(ctest).T

            results = numpy.mat(numpy.zeros((0,lenPara)))
            objsRBF = []
            jobs = [job_server.submit(classifyCM, (ratio, r, para[0], para[1], para[2], para[3], lenPara, ytrainM, ytestM, ctrainM, ctestM, dbname), (), ("numpy","dataProcess", "RBFNetwork", "dataLoader3", "datetime", "util")) for para in paraPerm]
            for job in jobs:
                cnm = job()
                result, objs = cnm[0], cnm[1]
                results =numpy.concatenate((results, result), axis = 0)
                objsRBF = objsRBF + objs

            print "\n"
            if not (numpy.shape(results)[0] == 0 or len(objsRBF) == 0): 
                dataLoader3.saveMatrix([results], [fnResults])
                dataLoader3.saveObjects([objsRBF], [fnRBFobjs])
            else: 
                util.infoErr([fnResults, fnRBFobjs])
        else:
            util.exPath([fnResults, fnRBFobjs])
    else:
        util.noPath([path4])


def seqLearnTest(cate, ratio, r, numCenterList, alphaList, QList, KList, lenPara, dbname, iter = 'ZZZ', mode = 'ZZZ'): 
    paraPerm = list(itertools.product(numCenterList, alphaList, QList, KList))

    path4 = util.getPath2(dbname + "_ycobjs_r" + str(r) + ".cpkl")
    if os.path.exists(path4):
        fnResults = util.getPath2(dbname + "_results_r" + str(r) + "_" + iter + "_" + mode + ".npy")
        # fnRBFobjs = util.getPath2(dbname + "_results_r" + str(r) + "_" + iter + ".cpkl")

        if not os.path.exists(fnResults):
            ctrainM, ctestM, ytrainM, ytestM = dataLoader3.cpklload(path4)
            # ctrainM, ctestM = numpy.mat(ctrain).T, numpy.mat(ctest).T

            results = numpy.mat(numpy.zeros((0,lenPara)))
            objsRBF = []
            for para in paraPerm: 
                result = classify(ratio, r, para[0], para[1], para[2], para[3], lenPara, ytrainM, ytestM, ctrainM, ctestM, dbname)
                # cnm = job()
                # result, obj = cnm[0], cnm[1]
                results =numpy.concatenate((results, result), axis = 0)
                # objsRBF = objsRBF + obj
                # results = numpy.concatenate((results, job()[0]), axis = 0)
                # objsRBF = objsRBF + job()[1]

            print "\n"
            if not numpy.shape(results)[0] == 0: 
                dataLoader3.saveMatrix([results], [fnResults])
                # dataLoader3.saveObjects([objsRBF], [fnRBFobjs])
            else: 
                util.infoErr([fnResults])
        else:
            util.exPath([fnResults])
    else:
        util.noPath([path4])


if __name__ == '__main__':
    pass
else:
    print str(datetime.datetime.now())[:19] + " importing module classifier ... "


# end
