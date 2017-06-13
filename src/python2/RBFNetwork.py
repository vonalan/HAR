import datetime
import numpy
import dataProcess
import evaluate



class RBFNN:
    # initialize the archietecture for Neural Network
    def __init__(self, indim, numCenter, outdim, alpha, Q):
        # self.ration = ration 
        # self.nRound = nRound 
        self.indim = indim # K
        self.numCenter = numCenter # M 
        self.outdim = outdim # category 
        self.U = numpy.mat([numpy.random.uniform(-1, 1, indim) for j in xrange(numCenter)])
        self.V = numpy.mat([[0.25] for j in xrange(numCenter)])
        self.W = numpy.mat(numpy.random.random([self.numCenter, self.outdim]))
        '''new'''
        self.alpha = alpha 
        self.Q = Q
        # self.trainx = trainx ##############################################
        # self.testx = testx ################################################
        # self.trainy = trainy ##############################################
        # self.testy = testy ################################################
        # self.trainout = trainout 
        # self.testout = testout 
        # self.confusedmatrix = confusedmatrix ##############################
        '''new'''


    # calculate activations
    def activCalc(self, trainX):
        Z = numpy.power(dataProcess.cDist(trainX, self.U), 2)
        A = numpy.exp(Z/numpy.transpose((-2 * numpy.power(self.V, 2)))) # how to implement element-wise operation?
        assert numpy.shape(A) == (numpy.shape(trainX)[0], self.numCenter)
        return A


    # calculate the parameters of hidden neurons in Network
    def centersCalc(self, trainX, trainY):
        self.U, self.V = dataProcess.innerCluster(trainX, trainY, self.numCenter, self.alpha)
        '''bug bug bug bug'''
        '''alpha'''
        '''bug bug bug bug'''
        assert numpy.shape(self.U) == (self.numCenter, numpy.shape(trainX)[1])
        # print str(datetime.datetime.now())[:19] + " The U calculation is done! The shape of the U is: ", numpy.shape(self.U)
        # self.V = numpy.tile(numpy.mean(dataProcess.pDist(trainX)) * alpha, (self.numCenter, 1))
        assert numpy.shape(self.V) == (self.numCenter, 1)
        # print str(datetime.datetime.now())[:19] + " The V calculation is done! The shape of the V is: ", numpy.shape(self.V)


    # classifier training
    def train(self, trainX, trainY):
        self.centersCalc(trainX, trainY)
        H = self.activCalc(trainX)
        self.W = numpy.dot(numpy.linalg.pinv(H), trainY)
        assert numpy.shape(self.W) == (self.numCenter, numpy.shape(trainY)[1])
        # print str(datetime.datetime.now())[:19] + " The W calculation is done! The shape of the W is: ", numpy.shape(self.W)
        print str(datetime.datetime.now())[:19] + " The classifier training is done! the shapes of {U, V, W} are: "+ str(numpy.shape(self.U)) + ", " + str(numpy.shape(self.V)) + ", " + str(numpy.shape(self.W))


    # classifier testing
    def test(self, trainX):
        H = self.activCalc(trainX)
        output = numpy.dot(H, self.W)
        assert numpy.shape(output) == (numpy.shape(trainX)[0], self.outdim)
        # if numpy.shape(trainX)[0] == 383:
        #     print str(datetime.datetime.now())[:19] + " The classifier testing for training set is done! The shape of the output is: ", numpy.shape(output)
        # elif numpy.shape(trainX)[0] == 216:
        #     print str(datetime.datetime.now())[:19] + " The classifier testing for testing set is done! The shape of the output is: ", numpy.shape(output)
        # print str(datetime.datetime.now())[:19] + " The classifier testing is done! the shape of {output} is: " + str(numpy.shape(output))
        return output


    # evaluate the training error, testing error, LGEM, training accuracy, testing accuracy
    def evaluateAll(self, trainX, trainY, trainOut, testX, testY, testOut):
        # paraV = [self.U, self.V, self.W]
        '''bug bug bug'''
        trainErr= evaluate.calcErr(trainOut, trainY)
        testErr = evaluate.calcErr(testOut, testY)
        trainErrV = list(numpy.array(trainErr)[0])
        testErrV = list(numpy.array(testErr)[0])
        '''bug bug bug'''
        trainAcc = evaluate.calcAcc(trainOut, trainY)
        testAcc = evaluate.calcAcc(testOut, testY)
        trainAccV = [trainAcc]
        testAccV = [testAcc]

        cmTrain = evaluate.calcConMat(trainOut, trainY)
        cmTest = evaluate.calcConMat(testOut, testY)

        '''bug bug bug'''
        STSM = evaluate.calcSTSM(trainX, trainY, self.W, self.U, self.V, self.Q)
        LGE = numpy.power(numpy.sqrt(trainErr) + numpy.sqrt(STSM), 2)
        STSMV = list(numpy.array(STSM)[0])
        LGEV = list(numpy.array(LGE)[0])
        '''bug bug bug'''
        print str(datetime.datetime.now())[:19] + " The classifier evaluating is done! the values of {trainAcc, testAcc} are: " + str(trainAcc)[0:6] + ", " + str(testAcc)[0:6] 
        
        '''bug bug bug'''
        resultsV = trainErrV + trainAccV + testErrV + testAccV + LGEV
        # resultsEXV = trainErrV + STSMV
        return resultsV, cmTrain, cmTest
        '''bug bug bug'''


if __name__ == '__main__':
    pass
else:
    print str(datetime.datetime.now())[:19] + " importing module RFBNetwork ... "


# end