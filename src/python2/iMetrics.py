#-*- coding: UTF-8 -*- 


import numpy 
import sklearn.metrics as sklmetrics
import util 
import dataProcess
import dataLoader3


def transLabelML(labelsetM): 
    sumR =  numpy.sum(labelsetM, axis = 1)
    assert (sumR == 1).all() == True
    
    labelR = numpy.argmax(labelsetM, axis = 1)
    labelC = numpy.transpose(labelR)
    labelsetA  = numpy.array(labelC)[0]

    return labelsetA


def transLabelLM(labelsetL): 
    pass 


# confused matrix
def ConMat(out, tar):
    return sklmetrics.confusion_matrix(out, tar)


# area under roc curve
def AUC(tar, out):
    return sklmetrics.roc_auc_score(tar, out, average='macro')


# f1-score
def F1Score(tar, out): # binary class or multiple class
    return sklmetrics.f1_score(tar, out, average = None)


# precision, recall, thresholds
def PRC(tar, out):
    pre, rec, thres = sklmetrics.precision_recall_curve(tar, out, pos_label = 1)
    return pre, rec, thres

    
def multi2bin(labelA, pos):
    labelAT = labelA.copy()
    ilabelAT = labelA.copy() # reverse the positive class and negative class 
    n = numpy.shape(labelAT)[0]
    # for i in xrange(m): 
    for j in xrange(n): 
        if labelA[j] == pos:
            labelAT[j] = 1
            ilabelAT[j] = 0
        else:
            labelAT[j] = 0
            ilabelAT[j] = 1
    return labelAT, ilabelAT


def AnaConMat(cm, threshold = 0.65):
    fcm = cm.astype(float)
    print fcm

    trace = numpy.trace(fcm)
    total = numpy.sum(fcm)
    acc = trace/total

    sumR = numpy.sum(fcm, axis = 1)
    sumC = numpy.sum(fcm, axis = 0)
    
    TP = numpy.diag(fcm)
    FP = sumC - TP
    FN = sumR - TP
    TN = trace - TP

    '''element-wise operations'''
    '''**************bugs***************'''
    P = TP/(TP + FP) # precision
    R = TP/(TP + FN) # recall
    F1 = 2 * (P * R) / (P + R)

    TPR = TP/(TP + FN) # recall
    TNR = TN/(TN + FP) #
    G = numpy.sqrt(TPR * TNR)
    '''**************bugs***************'''
    '''element-wise operations'''

    '''AUC_ROC_CURVE'''
    '''PRECISION_RECALL_CURVE'''

    # Reduction of Uncertainty
    ACC = TP/sumC
    idxcx = numpy.nonzero(ACC >= threshold)[0]
    idxsx = numpy.argsort(ACC) # ascend

    idxc = [i for i in idxsx if i not in idxcx]
    
    cms = fcm - 0
    for i in xrange(len(cms)): 
        cms[i,i] = -1
    print cms

    idxr = numpy.argmax(cms, axis = 0)[idxc]

    pairs = []
    for r, c in zip(idxr, idxc):
        p = (r,c)
        pairs.append(p)

    return F1, G, pairs


# AUC_ROC, F1-MEASURE, G-MEAN, RECALL-PRECISION-CURVE

def evaluate(dbname, r, iterflag, modeflag): 
    fn6 = dbname + '_result_r' + str(r) + '_' + iterflag + '_ex' + modeflag + '.cpkl'
    fn4 = dbname + "_ycobjs_r" + str(r) + ".cpkl" 
    
    path4 = util.getPath2(fn4)
    path6 = util.getPath2(fn6)
    
    ycobj = dataLoader3.cpklload(path4)
    outcm = dataLoader3.cpklload(path6)
    
    ctrain, ctest, ytrain, ytest = ycobj[0], ycobj[1], ycobj[2], ycobj[3]

    mtclistMlist = []
    for oc in outcm:
        m, k, outtrain, outtest, cmtrain, cmtest = oc[0], oc[1], oc[2], oc[3], oc[4], oc[5]
        # tartrainL = transLabelML(ytrain)
        # outtrainL = transLabelML(outtrain)
        outtestI = dataProcess.ftoi(outtest)

        '''designed for kth'''
        ytestM = numpy.mat(ytest)

        tar = transLabelML(ytestM)
        out = transLabelML(outtestI)

        cm =  ConMat(out, tar) # not (tar, out)
        print cm

        # iF1, iG, ipairs = AnaConMat(cm)
        
        mtclist = []
        for i in xrange(numpy.shape(cm)[1]): 
            t, it = multi2bin(tar, i)
            o, io = multi2bin(out, i)

            auc = AUC(t, o)
            print auc

            '''**************bugs***************'''
            # assumption: TNR == iTPR and TPR == iTNR 
            # TPR, TNR = func(t, o)
            # iTPR, iTNR = func(it, io)
            print m, k, i
            pre, rec, thre = PRC(t,o) 
            ipre, irec, ithre = PRC(it, io)
            tnr, itnr = rec, irec
            tpr, itpr = irec, rec
            gmean = numpy.sqrt(tpr[-2] * tnr[-2])
            print pre, rec, thre 
            print ipre, irec, ithre 
            print gmean 
            '''**************bugs***************'''

            f1s = F1Score(t, o)
            print f1s
            
            mtc = [auc, pre[-2], rec[-2], tpr[-2], tnr[-2], gmean, f1s[-1]]
            mtclist.append(mtc)
        mtclistM  = numpy.array(mtclist)
        mtclistMlist.append(mtclistM)

    return mtclistMlist


if __name__ == '__main__':
    path1 = util.getPath2('targetSetTrain.npy')
    path2 = util.getPath2('targetSetTest.npy')

    m = numpy.load(path1)
    n = numpy.load(path2)

    a = numpy.mat([[1, 0, 0, 0],[0, 0, 1, 0],[0, 1, 0, 0],[0, 0, 0, 1],[1, 0, 0, 0],[0, 0, 1, 0]])
    b = numpy.mat([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 0, 1],[0, 0, 1, 0],[1, 0, 0, 0],[0, 1, 0, 0]])

    tar = transLabelML(m)
    out = transLabelML(n)

    cm =  ConMat(out, tar) # not (tar, out)
    print cm

    iF1, iG, ipairs = AnaConMat(cm)
    
    mtclist = []
    for i in xrange(numpy.shape(cm)[1]): 
        t, it = multi2bin(tar, i)
        o, io = multi2bin(out, i)

        auc = AUC(t, o)
        print auc

        '''**************bugs***************'''
        pre, rec, thre = PRC(t,o)
        ipre, irec, ithre = PRC(it, io) # new way to calculate TPR
        gmean = numpy.sqrt(rec * irec)
        print pre, rec, thre
        print ipre, irec, ithre
        print gmean
        '''**************bugs***************'''

        f1s = F1Score(t, o)
        print f1s
        
        mtc = [auc, pre, rec, thre, gmean, f1s]
        mtclist.append(mtc)

    print 'hahaha, no bugs !!! '
else: 
    print util.fetchTime() + " importing module iMetrics ... "
    
# end 
