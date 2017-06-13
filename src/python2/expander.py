#-*- coding: UTF-8 -*- 

import os 
import shutil 
import cPickle 
import gzip 
import tranverse 

''' 
path = "/home/kingdom/TranExp/raw_ucf" 
objPath = "/home/kingdom/TranExp/UCF" 

vfiles = tranverse.tranverse(path, objPath, [], 'ucf') 

print "\nBe careful of following path(s): " 
for vf in vfiles: 
    print vf 

txPath = "/home/kingdom/TranExp/UCF/a_step_to_victory.txt" 
with open(txPath, "wb") as txFile: 
    for file in vfiles: 
        txFile.write(file + '\n') 
        print file

gzPath = "/home/kingdom/TranExp/UCF/a_step_to_victory.cpkl.gz" 
with gzip.open(gzPath, "wb") as gzFile: 
    dmp = cPickle.dumps(vfiles) 
    gzFile.write(dmp) 
'''

gzPath = "/home/kingdom/TranExp/UCF/a_step_to_victory.cpkl.gz" 
with gzip.open(gzPath, "rb") as gzFile: 
    dmp = gzFile.read() 
    vfiles = cPickle.loads(dmp) 
    for vf in vfiles: 
        opath = '/home/kingdom/TranExp/UCF/' + vf[17:] # all videos 
        mpath = '/home/kingdom/TranExp/CAN/' + vf[17:] # candidate videos need to confirm 
        print opath, mpath 
        
        if os.path.exists(opath):  
            repeat= 0 
            while repeat < 3: 
                os.system('ffplay -autoexit ' + opath)
                repeat += 1 
        
            count = 0 
            rec = True 
            while rec: 
                if count < 3: 
                    check = raw_input("confirm to move? 'yes' or 'no': ")
                    if check == 'yes': 
                        print 'moving ... ' 
                        shutil.move(opath, mpath)
                        rec = False 
                    elif check == 'no': 
                        rec = False 
                    else: 
                        count += 1  
                else: 
                    print '\ngo fucking yourself! ' 
                    count = 0 
        else: 
            print opath + " doesn't exist! "  

ngzPath = "/home/kingdom/TranExp/CAN/a_step_to_victory.cpkl.gz" 
shutil.move(gzPath, ngzPath)

''' 
txPath = "/home/kingdom/TranExp/UCF/a_step_to_victory.txt" 
with open(txPath, "rb") as pathFile: 
    for line in pathFile.readlines(): 
        opath = '/home/kingdom/TranExp/UCF/' + vf[17:] # all videos 
        mpath = '/home/kingdom/TranExp/CAN/' + vf[17:] # candidate videos need to confirm 
        print opath, mpath 
        
        repeat= 0 
        while repeat < 3: 
            os.system('ffplay -autoexit -fs ' + opath)
            repeat += 1 
        
        count = 0 
        rec = True 
        while rec: 
            if count < 3: 
                check = raw_input("confirm to move? 'yes' or 'no': ")
                if check == 'yes': 
                    if os.path.exists(opath): 
                        print 'moving ... ' 
                        shutil.move(opath, mpath)
                    rec = False 
                elif check == 'no': 
                    rec = False 
                else: 
                    count += 1 
            else: 
                print '\ngo fucking yourself! ' 
                count = 0 

ntxPath = "/home/kingdom/TranExp/CAN/a_step_to_victory.txt" 
shutil.move(txPath, ntxPath) 
''' 

# end 
