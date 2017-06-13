import os 
import sys 

assert len(sys.argv) == 2

if sys.argv[1] == 'link': 
    os.system('ssh -x kingdom@125.216.241.48')
    # os.system('cd UCF/src')
elif sys.argv[1] == 'push': 
    os.system('scp -r ./*.py kingdom@125.216.241.48:/home/kingdom/UCF/src')
elif sys.argv[1] == 'get': 
    os.system('scp kingdom@125.216.241.48:/home/kingdom/UCF/data/pwd/*bow_r1*512* ../data/pwd')
    os.system('scp kingdom@125.216.241.48:/home/kingdom/UCF/data/pwd/*bow_r1*1024* ../data/pwd')
    os.system('scp kingdom@125.216.241.48:/home/kingdom/UCF/data/pwd/*bow_r1*2048* ../data/pwd')
    
