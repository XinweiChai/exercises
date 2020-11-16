from gevent import monkey
monkey.patch_all()
import gevent
import redis
import  time

r = redis.Redis(host="192.168.1.3",port=6379)

def getFunc(key):
    """取key"""
    v=r.get(key)
    # print(v)

def call_gevent(count):
    """调用gevent 模拟高并发"""
    begin_time = time.time()
    run_gevent_list = []
    num = 1
    for i in range(count):
        print('--------------%d--Test-------------' % i)
        mykey = 'test' + str(num)
        run_gevent_list.append(gevent.spawn(getFunc,mykey))
        num = num + 1
    gevent.joinall(run_gevent_list)
    end = time.time()
    print('测试并发量'+ str(count))
    print('单次测试时间（平均）s:', (end - begin_time) / count)
    print('累计测试时间 s:', end - begin_time)

if __name__ == '__main__':
    # 并发请求数量
    test_count = 20000  #改变并发量查看测试效果。。我这里取7000，10000，20000进行测试。记得将rdis的最大连接数改为30000并重启redis。
    # while 1:
    call_gevent(count=test_count)