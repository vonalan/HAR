#-*- coding: UTF-8 -*-

import os
import datetime
import itertools
import numpy
import pp
import util
import actRec
import dataLoader3
import classifier
import cluster
import splitter


class KTH(): 
    def __init__(self): 
        self.name = 'kth' 
        self.actions = ['walking', 'jogging', 'running', 'boxing', 'handwaving', 'handclapping'] 
        self.cate = len(self.actions)
        self.cvlist = [] 
        self.stipfile = '../data/' + self.name + 'stip.txt'
        self.alphaList = [1]
        self.QList = [0.1]
        self.numCenterList = [m for m in xrange(60, 180 + 1, self.cate)] 
        self.KList = [k for k in xrange(128, 4096 + 1, 128)] + [200, 600, 1000, 4000]

'''*********************************************************'''
# number of video sequences'''
'''
Diving (14 videos)
Golf Swing (18 videos)
Kicking (20 videos)
Lifting (6 videos)
Riding Horse (12 videos)
Running (13 videos)
SkateBoarding (12 videos)
Swing-Bench (20 videos)
Swing-Side (13 videos)
Walking (22 videos) 
'''
'''*********************************************************'''
class UCF():
    def __init__(self): 
        self.name = 'ucf' 
        self.actions = ['Diving', 'Golf-Swing', 'Kicking', 'Lifting', 'Riding-Horse', 'Run', 'SkateBoarding', 'Swing-Bench', 'Swing-SideAngle', 'Walk']
        self.cate = len(self.actions)      
        self.cvlist = [] 
        self.alphaList = [1]
        self.QList = [0.1]
        self.numCenterList = [m for m in xrange(10, 200 + 1, self.cate)] 
        self.KList = [k for k in xrange(128, 4096 + 1, 128)] + [200, 600, 1000, 4000]          


class HLWD(): 
    def __init__(self): 
        raise Exception('BROKEN DATABASE')
        self.name = 'hlwd' 
        self.actions = []
        self.cate = len(self.actions)
        self.cvlist = [] 


def retrive(dbname): 
    if dbname == 'kth': 
        database = KTH()
    elif dbname == 'ucf': 
        database = UCF() 
    else: 
        database = HLWD() 
        
    return database.actions, database.cate, database.stipfile, database.alphaList, database.QList, database.numCenterList, database.KList

def paraInfo(cate): 
    paraList1 = ["ratio", "round", "numCenter", "alpha", "Q", "K"]
    paraList2 = ["trainErr", "testErr", "LGE"]
    paraList3 = ["trainAcc", "testAcc"]
    lenPara = len(paraList1) + len(paraList3) + cate * len(paraList2)
    return lenPara

if __name__ == '__main__': 
    pass 
else: 
    print str(datetime.datetime.now())[:19] + 'importing module databases ... '
