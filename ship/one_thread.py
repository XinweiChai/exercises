import redis
import os, time, threading
import uuid
import random

# pool =redis.ConnectionPool(host='192.168.1.3',port=6379)
# r = redis.Redis(connection_pool=pool)

r = redis.Redis(host='192.168.1.3', port=6379)

r.set()
def setKey():
    num = 1
    set_start = time.clock()
    while num < 80000:
        mykey = 'test' + str(num)
        num = num + 1
        myvalue = str(uuid.uuid1()) * 250 + str(random.randint(100000000, 1000000000))

        r.set(mykey, myvalue)
        # print(r[mykey])
        # print(r.get(mykey))

    set_end = time.clock()
    set_times = set_end - set_start
    print('单线程存8万个key的时间:' + str(set_times) + 's')


if __name__ == '__main__':
    setKey()