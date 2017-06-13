import os 
import util 

KList = [k for k in xrange(128, 4096 + 1, 128)] + [200, 600, 1000, 4000]

for i in xrange(250): 
    if i not in KList: 
        filename = 'kth_bow_r0_k' + str(i) + '.cpkl'
        path = util.getPath2(filename)
        if(os.path.exists(path)):
            os.remove(path)
            print util.fetchTime() + ' ' + filename + 'is removed! '
        else: 
            # print util.fetchTime() + ' ' + filename + ' error! '
            pass