import random
import time

def getLottery(sec):
    now = int(time.time()) + sec
    lottery_num = []
    for i in range(5): # 5 lottery number (for next 5sec)
        seed = now + i
        random.seed(seed)
        lottery_num.append(str(random.randint(0,999999)))
    print(f'{",".join(lottery_num)}')
        
getLottery(5)
