#-*- coding: UTF-8 -*-
# designed for UCF databases
# should check the suspicious file at last

import os
import expanse 

def tranverse(path, objPath, vfiles, vname):
    print '\n'
    print path

    vcount, pcount = 0, 0
    vpaths = []
    filelist =  os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename) 
        name = vname + '-' + filename 
        print filepath 
        print name 
        if(os.path.isdir(filepath)):
            tranverse(filepath, objPath, vfiles, name)
        else:
            # allfile.append(filepath)
            
            # *.jpg, *.png 
            if(('.jpg' in filename) or ('.png' in filename)): 
                pcount += 1 
            else: 
                pass 
            
            # *.avi, *.mp4 
            if(('.avi' in filename) or ('.mp4' in filename)): 
                # print 'flipping ... '
                nframe, outPath1, outPath2 = expanse.hflip(filepath, objPath, name)
                vcount += 1
                vpaths += ([outPath1] + [outPath2])
            else: 
                pass

    assert vcount <= 1

    if vcount == 0:
        if pcount > 0:
            # print 'generating ... '
            expanse.imgtovid(path, objPath, vname)
        else:
            pass

    if vcount == 1:
        if pcount > 0:
            if nframe < pcount:
                expanse.imgtovid(path, objPath, vname)
                vfiles += vpaths
            else:
                pass
        else:
            pass

    # if vcount > 1:
    #     pass

    return vfiles
    
if __name__ == '__main__':
    path = "/home/kingdom/UCF/openCV"
    objPath = "/home/kingdom/UCF/UCF"
    tranverse(path, objPath, [], 'UCF')
else: 
    print "Importing module tranverse ... " 

# end