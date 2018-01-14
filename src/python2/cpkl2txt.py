import numpy as np

import dataLoader3

dbname = 'ucf'
b_round=9
e_round=12

for sround in range(b_round, e_round):
    path2 = '../data/pwd/%s_origin_r%d.cpkl'%(dbname, sround)
    print path2
    splitlist, ctrain, ctest, ctrainM, ctestM, xtrainM, xtestM, ytrainM, ytestM, xrandMX = dataLoader3.cpklload(path2)

    np.savetxt('../data/pwd/%s_ctrain_r%d.txt'%(dbname, sround), ctrain)
    np.savetxt('../data/pwd/%s_ctest_r%d.txt'%(dbname, sround), ctest)

    np.savetxt('../data/pwd/%s_ytrain_r%d.txt'%(dbname, sround), ytrainM)
    np.savetxt('../data/pwd/%s_ytest_r%d.txt'%(dbname, sround), ytestM)

    np.savetxt('../data/pwd/%s_xtrain_r%d.txt'%(dbname, sround), xtrainM)
    np.savetxt('../data/pwd/%s_xtest_r%d.txt'%(dbname, sround), xtestM)
    np.savetxt('../data/pwd/%s_xrand_r%d.txt'%(dbname, sround), xrandMX)
