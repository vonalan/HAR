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
import iMetrics


'''*********************************************************'''
dbname = 'kth'
cate = 6

r = 9
iterflag = 'X'
modeflag = 'CM'
modelist = ['A1']

# func = 'conc'
func = 'exCM'
# mode = 'anCM'

mlower = 0
klower = 0
mupper = 200
kupper = 4096

KList = [4000, 4096, 200, 600, 1000]
'''*********************************************************'''


mtclistMlist = iMetrics.evaluate(dbname, r, iterflag, modeflag)

tmplist = [[0] * 7]
tmparry = numpy.array(tmplist)

summer = numpy.zeros((0, 7))
for mtc in mtclistMlist: 
    summer = numpy.concatenate((summer, mtc), axis = 0)
    summer = numpy.concatenate((summer, tmparry), axis = 0)
    

fn8 = dbname + '_result_r' + str(r) + '_' + iterflag + '_mtc' + modeflag + '.cpkl'
path8 = util.getPath2(fn8)
dataLoader3.cpklsave(mtclistMlist, path8)













