import os
import datetime
import util
import dataLoader3
import dataProcess 

def kMeans(r, k, ctrain, ctest, xtrainM, xtestM, xrandMX, path):

    print "\n" + str(datetime.datetime.now())[:19] + " Building bag of features for {r = " + str(r) + ", " + "k = " + str(k) + "} ... "

    centroids = dataProcess.kMeans(xrandMX, k)

    catrain = dataProcess.centroidAssign(centroids, xtrainM)
    catest = dataProcess.centroidAssign(centroids, xtestM)

    bowTrain = dataProcess.BOW(catrain, ctrain, k)
    bowTest = dataProcess.BOW(catest, ctest, k)

    objs = [bowTrain, bowTest, centroids]
    dataLoader3.cpklsave(objs, path)

    print str(datetime.datetime.now())[:19] + " Building bag of features for {r = " + str(r) + ", " + "k = " + str(k) + "} is done! "

    # return bowTrain, bowTest, centroids


if __name__ == '__main__':
    pass
else:
    print str(datetime.datetime.now())[:19] + " importing module cluster ... "


# end
