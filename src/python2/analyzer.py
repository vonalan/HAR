# -*- coding: UTF-8 -*-

import os
import datetime
import util
import numpy
import dataLoader3


def exConMat(dbname, r, cate, iterflag, modeflag):
    fn4 = dbname + '_results_r' + str(r) + '_' + iterflag + '_' + modeflag + '.npy'
    fn5 = dbname + '_results_r' + str(r) + '_' + iterflag + '_' + modeflag + '.cpkl'

    path4 = util.getPath2(fn4)
    path5 = util.getPath2(fn5)

    cres = numpy.load(path4)
    objs = dataLoader3.cpklload(path5)

    anaT, concT = summarize(cres, cate)

    cml = []
    for i in xrange(numpy.shape(concT)[0]):
        x1 =  concT[i, 2]
        x2 =  concT[i, 1]

        s, t = numpy.shape(cres)
        for m in xrange(s):
            y1 = cres[m,2]
            y2 = cres[m,5]

            if cres[m,2] == concT[i, 2] and cres[m,5] == concT[i, 1]:
                cml.append([concT[i, 2], concT[i, 1], objs[m][0], objs[m][1], objs[m][2], objs[m][3]])

    fn6 = dbname + '_result_r' + str(r) + '_' + iterflag + '_ex' + modeflag + '.cpkl'
    path6 = util.getPath2(fn6)
    dataLoader3.cpklsave(cml, path6)


def anaCMat(dbname, r, iterflag, cate):
    fn4 = dbname + '_results_r' + str(r) + '_' + iterflag + '_CM.npy'
    fn5 = dbname + '_results_r' + str(r) + '_' + iterflag + '_exCM.cpkl'

    path4 = util.getPath2(fn4)
    path5 = util.getPath2(fn5)

    cres = numpy.load(path4)
    ana3, conc3 = summarize(cres, cate)

    cmat = dataLoader3.cpklload(path5)

    icc = []
    for cm in cmat:
        icc.append(cm[5])

    return ana3, conc3, cres, icc


def mergeList(pathlist):
    result = []
    for path in pathlist:
        if os.path.exists(path):
            objs = dataLoader3.cpklload(path)
            for obj in objs:
                result.append(obj)
        else:
            util.noPath(path)
    return result


def mergeMatrix(dbname, r, iterflag, modelist):
    fn1 = dbname + '_results_r' + str(r) + '_' + iterflag + '.npy'
    path1 = util.getPath2(fn1)
    result = numpy.load(path1)

    checklist = []
    for mode in modelist:
        fn2 = dbname + '_results_r' + str(r) + '_' + iterflag + '_' + mode + '.npy'
        path2 = util.getPath2(fn2)

        if os.path.exists(path2) and path2 not in checklist:
            res = numpy.load(path2)
            result = numpy.concatenate((result, res), axis=0)
            checklist.append(path2)
        else:
            util.noPath(path2)

    return result


def sumList(ls):
    sum = 0
    sl = []
    for i in ls:
        sum += i
        sl.append(sum)
    # print ls
    # print sl
    return sl


def summarize(result1, cate):
    para = ["ratio", "round", "numCenter", "alpha", "Q", "K", "trainErr", "trainAcc", "testErr", "testAcc", "LGE"]
    cpara = [1, 1, 1, 1, 1, 1, cate, 1, cate, 1, cate]
    spara = sumList(cpara)

    col = ['M', 'alpha', 'Q', 'K', 'testAcc', 'trainAcc', 'argMSE', 'argLGE', 'MSE', 'LGE']
    ccol = [1, 1, 1, 1, 1, 1, 3, 3, cate, cate]
    scol = sumList(ccol)
    nrow = scol[-1]

    analysis = numpy.zeros((numpy.shape(result1)[0], nrow))
    conclusion = numpy.zeros((8, 3))

    a1 = spara[para.index('numCenter') - 1]
    a2 = spara[para.index('K')]
    u = scol[col.index('K')]
    analysis[:, :u] = result1[:, a1:a2]  # [M, alpha, Q, K]

    b = spara[para.index('testAcc') - 1]  # testAcc
    c = spara[para.index('trainAcc') - 1]  # trainAcc
    v = scol[col.index('testAcc') - 1]  # testAcc
    w = scol[col.index('trainAcc') - 1]  # trainAcc
    analysis[:, v] = result1[:, b]  # testAcc
    analysis[:, w] = result1[:, c]  # trainAcc

    # trainErr
    d1 = spara[para.index('trainErr') - 1]
    d2 = spara[para.index('trainErr')]
    x = scol[col.index('argMSE') - 1]
    y = x + 1
    z = x + 2
    analysis[:, x] = numpy.mean(result1[:, d1:d2], axis=1)  # trainErr
    analysis[:, y] = numpy.min(result1[:, d1:d2], axis=1)  # trainErr
    analysis[:, z] = numpy.max(result1[:, d1:d2], axis=1)  # trainErr
    o = scol[col.index('MSE') - 1]
    p = scol[col.index('MSE')]
    analysis[:, o:p] = result1[:, d1:d2]

    # LGE
    f1 = spara[para.index('LGE')-1]
    f2 = spara[-1]
    r = scol[col.index('argLGE') - 1]
    s = r + 1
    t = r + 2
    analysis[:, r] = numpy.mean(result1[:, f1:f2], axis=1)  # LGE
    analysis[:, s] = numpy.min(result1[:, f1:f2], axis=1)  # LGE
    analysis[:, t] = numpy.max(result1[:, f1:f2], axis=1)  # LGE
    h = scol[col.index('LGE') - 1]
    i = scol[col.index('LGE')]
    analysis[:, h:i] = result1[:, f1:f2]

    idxMax = list(numpy.argmax(analysis[:, 4:6], axis=0))
    idxMin = list(numpy.argmin(analysis[:, 6:12], axis=0))
    idx = idxMax + idxMin

    for i in xrange(len(idx)):
        conclusion[i, :] = analysis[idx[i], [4, 3, 0]]

    return analysis, conclusion


def conclude(dbname, r, iterflag, mode, cate, Klist, mlower = 0, mupper = 200, klower = 0, kupper = 4096):
    result = mergeMatrix(dbname, r, iterflag, mode)

    result = result[numpy.nonzero(result[:, 2] <= mupper)[0]] # m
    result = result[numpy.nonzero(result[:, 2] >= mlower)[0]] # m
    result = result[numpy.nonzero(result[:, 5] <= kupper)[0]] # k
    result = result[numpy.nonzero(result[:, 5] >= klower)[0]] # k

    analist = []
    conlist = []

    ana0, conc0 = summarize(result, cate)
    analist.append(ana0)
    conlist.append(conc0)

    for k in Klist:
        res1 = result[numpy.nonzero(result[:, 5] == k)[0]]
        if numpy.shape(res1)[0] != 0:
            ana1, conc1 = summarize(res1, cate)
            analist.append(ana1)
            conlist.append(conc1)

    return analist, conlist


if __name__ == '__main__':
    pass
else:
    print str(datetime.datetime.now())[:19] + " importing module analyzer ... "