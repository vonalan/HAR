#-*- coding: UTF-8 -*-


import os
import util 
import numpy
import dataLoader3
import analyzer


'''*********************************************************'''
dbname = 'kth'
cate = 6

r = 9
iterflag = 'X'
modeflag = 'CM'
modelist = ['A1']

func = 'anCM'

mlower = 0
klower = 0
mupper = 200
kupper = 4096

KList = [200, 600, 1000, 4000, 3456, 1408]
'''*********************************************************'''


if func == 'conc': 
    analist, conclist = analyzer.conclude(dbname, r, iterflag, modelist, cate, KList, mlower = mlower, mupper = mupper, klower = klower, kupper = kupper)
elif func == 'exCM': 
    analyzer.exConMat(dbname, r, cate, iterflag, modeflag)
elif func == 'anCM':
    ana3, conc3, cres, icc = analyzer.anaCMat(dbname, r, iterflag, cate)
    
    tmplist = [[0] * cate]
    tmparry = numpy.array(tmplist)

    summer = numpy.zeros((0, cate))
    for mtc in icc: 
        summer = numpy.concatenate((summer, mtc), axis = 0)
        summer = numpy.concatenate((summer, tmparry), axis = 0)