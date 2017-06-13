#-*- coding: UTF-8 -*-

import os
import datetime
import itertools
import numpy
import pp
import util
import actRec
import databases
import dataLoader3
import classifier
import cluster
import splitter


'''*********************************************************'''
dbname = 'kth'
'''*********************************************************'''


ratio = 2.0/3.0
actions, cate, stipfile, alphaList, QList, numCenterList, KList = databases.retrive(dbname)
lenPara = databases.paraInfo(cate)


'''*********************************************************'''
iterflag = 'X'
modeflag = 'M'
sRound = 9
nRound = 10
'''*********************************************************'''


'''*********************************************************'''
# numCenterList = [20, 30, 40, 60, 70, 80, 90, 100, 120, 140, 190, 200]
# KList = [200, 600, 1000]
'''*********************************************************'''


# the inlet of application
for r in xrange(sRound, nRound, 1):
    actRec.cluster2(r, KList, actions, stipfile, dbname) 
    '''
    if modeflag == 'TEST': 
        classifier.seqLearnTest(cate, ratio, r, numCenterList, alphaList, QList, KList, lenPara, dbname, iter = iterflag, mode = modeflag)
    elif modeflag == 'CM': 
        classifier.seqLearnCM(cate, ratio, r, numCenterList, alphaList, QList, KList, lenPara, dbname, iter = iterflag, mode = modeflag)
    else: 
        classifier.seqLearn(cate, ratio, r, numCenterList, alphaList, QList, KList, lenPara, dbname, iter = iterflag, mode = modeflag)
    '''