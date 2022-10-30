import requests
from datetime import datetime, timedelta
import random
import time

print(datetime.now())
p = "%a, %d %b %Y %H:%M:%S"
unix_epoch = datetime(1970, 1, 1)

def getLottery(m):
    r = requests.get("http://45.77.169.171:10021")
    print("Server time: " + r.headers["date"])
    server_time_str = r.headers["date"][:-4]
    server_time = datetime.strptime(server_time_str, p)
    now = datetime.now()
    for i in range(m): # Next m min
        lottery_min = server_time - timedelta(seconds=server_time.second) + timedelta(minutes=i+1) # Set seconds to 0 and add nearest min
        lottery_min_epoch = (lottery_min - unix_epoch).total_seconds()
        lottery_num = []
        for j in range(5): # 5 lottery number (for next 5sec)
            lottery_sec_epoch = lottery_min_epoch + j
            random.seed(lottery_sec_epoch)
            lottery_num.append(str(random.randint(0,999999)))
        print(f'{str(now.minute+i+1)}:00 -> {",".join(lottery_num)}')
        
getLottery(5)
