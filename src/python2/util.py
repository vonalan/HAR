import platform 
import datetime 


def getPath(filename): 
    path = ""
    
    getPlatform = platform.system()
    if 'Windows' in getPlatform:
        path = "E:\Users\kingdom\UCF\data\pwd\\" + filename 
    elif 'Linux' in getPlatform:
        path = "../data/pwd/" + filename 
    else:
        pass
    
    return path

def getPath2(filename): 
    path = ""
    
    getPlatform = platform.system()
    if 'Windows' in getPlatform:
        path = "..\data\pwd\\" + filename 
    elif 'Linux' in getPlatform:
        path = "../data/pwd/" + filename 
    else:
        pass
    
    return path

def fetchTime():
    return str(datetime.datetime.now())[:19]


def exPath(pathList):
    for path in pathList:
        print str(datetime.datetime.now())[:19] + " File: " + path + " has already exist! "


def noPath(pathList):
    for path in pathList:
        print str(datetime.datetime.now())[:19] + " File: " + path + " does not exist! "
        
def infoErr(pathList):
    for path in pathList: 
        print str(datetime.datetime.now())[:19] + " File: " + path + " error! please check! "


if __name__ == '__main__':
    print str(datetime.datetime.now())[:19] + " implemeting the application in the platform: " + platform.system()
else:
    print str(datetime.datetime.now())[:19] + " implemeting the application in the platform: " + platform.system()


# end
