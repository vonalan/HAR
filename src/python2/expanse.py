#-*- coding: UTF-8 -*- 

import os
import numpy as np
import cv2

def imgsize(path): 
    mlen, mhei = 0, 0 
    
    pcount = 0
    filelist =  os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if(os.path.isdir(filepath)):
            pass 
        else:
            # *.jpg, *.png 
            if(('.jpg' in filename) or ('.png' in filename)):
                frame = cv2.imread(filepath)
                clen, chei = frame.shape[1], frame.shape[0]                
                if mlen < clen: 
                    mlen = clen 
                if mhei < chei: 
                    mhei = chei 
                pcount += 1
                # print "frame: " + str(pcount) + ' ' + str((len, hei)) 
            else: 
                pass 
    return (mlen, mhei) 

def imgtovid(path, objPath, vname):
    print '\n' 
    oname = vname + '_o' + '.avi'
    hname = vname + '_h' + '.avi'

    outPath1 = os.path.join(objPath, oname) 
    outPath2 = os.path.join(objPath, hname)
    if (os.path.exists(outPath1) or os.path.exists(outPath2)):
        raise Exception("The path of {" + outPath1 + ", " + outPath2 + "} are overloaded! ")

    # fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
    # fourcc = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
    fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
    # fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
    # size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    fps = 10
    # size = (1920, 1080)
    size = imgsize(path)
    out1 = cv2.VideoWriter(outPath1, fourcc, fps, size)
    out2 = cv2.VideoWriter(outPath2, fourcc, fps, size)
    
    # print '\n' 
    print 'Generating videos {' + oname + ', ' + hname + '} from picutures ... '
    pcount = 0 
    filelist =  os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if(os.path.isdir(filepath)):
            # tranverse(pwdPath, chdDir) 
            pass 
        else:
            # print childPath.decode('gbk')
            # print vname.decode('gbk')
            
            # *.jpg, *.png 
            if(('.jpg' in filename) or ('.png' in filename)):
                frame = cv2.imread(filepath)
                # print "frame: " + str(pcount + 1)
                out1.write(frame)
                # cv2.imshow('frame',frame)
                nframe = cv2.flip(frame,1)
                # cv2.imshow('nframe',nframe)
                out2.write(nframe)
                pcount += 1
            else: 
                pass 

    out1.release()
    out2.release() 
    cv2.destroyAllWindows()
    
def distort(inPath):
    pass 

def vflip(inPath):
    pass 

def hflip(vPath, objPath, vname):
    print '\n' 
    # print vname
    
    outPath1 = os.path.join(objPath, vname[:-4] + '_o' + '.avi')
    outPath2 = os.path.join(objPath, vname[:-4] + '_h' + '.avi')
    if(os.path.exists(outPath1) or os.path.exists(outPath2)):
        raise Exception("The path of {" + outPath1 + ", " + outPath2 + "} are overloaded! ")

    videoCapture = cv2.VideoCapture(vPath)

    fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
    fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    out1 = cv2.VideoWriter(outPath1, fourcc, fps, size)
    out2 = cv2.VideoWriter(outPath2, fourcc, fps, size)
    
    print 'Flipping video {' + vname + '} horizontally ... ' 
    count = 0
    while(videoCapture.isOpened()):
        success, frame = videoCapture.read()
        if success == True:
            # print "frame: " + str(count + 1)
            out1.write(frame)
            # cv2.imshow('frame',frame)
            nframe = cv2.flip(frame,1)
            # cv2.imshow('nframe',nframe)
            out2.write(nframe)
            count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
            
    videoCapture.release()
    out1.release()
    out2.release() 
    cv2.destroyAllWindows()

    return count, outPath1, outPath2

if __name__ == '__main__':
    objPath = "/home/kingdom/UCF/UCF" 
    imgPath = "/home/kingdom/UCF/openCV/img" 
    imgtovid(imgPath, objPath, 'imgtovid') 
    
    vPath = "/home/kingdom/UCF/openCV/video/halo.avi" 
    hflip(vPath, objPath, 'halo.avi') 
else: 
    print "Importing module expanse ... "

# end 
