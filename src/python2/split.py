#-*- coding: UTF-8 -*- 

import random
import math 
import datetime 
import splitter


def mklist(actions): 
    vclist = [] 
    for i in xrange(len(actions)): 
        vclist.append(0)    
    
    return vclist 

'''***************************************************'''
def vcount2(targetSet, actions): 
    vclist = mklist(actions)

    for i in xrange(len(actions)):
        for tar in targetSet: 
            if tar == splitter.itov(i + 1, actions): 
                vclist[i] += 1 
    
    total = 0 
    for i in vclist: 
        total += i
        print i, total 
    
    return total, vclist
'''***************************************************'''

def vcount(vlistfile, actions): 
    vclist = mklist(actions)
    
    with open(vlistfile, 'r') as vlf: 
        for line in vlf.readlines(): 
            for i in xrange(len(actions)):
                if line[-1] == 'o': 
                    if actions[i] in line: 
                        vclist[i] += 1 
                    else: 
                        pass 
                else: 
                    pass 
    
    total = 0 
    for i in vclist: 
        total += i
        # print i, total 
    
    return total, vclist

# Roulette 
def split(vclist): 
    splitlist = [] 
    for cv in vclist: 
        cv = int(cv)
        num = int(math.ceil(cv * 2.0/3.0))
        # print num, cv - num 
        
        totalist = [i for i in xrange(cv)] 
        # random.shuffle(totalist) 
        clip = random.sample(totalist, num) 
        left = [i for i in totalist if i not in clip] # for the element of totls and clip is uniq
        print clip, left
        splitlist.append((clip, left))
    return splitlist

if __name__ == '__main__':
    vlistfile = 'ucflist.txt'
    ucflist = ['Diving', 'Golf-Swing', 'Kicking', 'Lifting', 'Riding-Horse', 'Run', 'SkateBoarding', 'Swing-Bench', 'Swing-SideAngle', 'Walk']
    
    total, vclist = vcount(vlistfile, ucflist) 
    splitlist = split(vclist)
else: 
    print str(datetime.datetime.now())[:19] + " importing module split ... "

# end
