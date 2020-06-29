class Myerror(Exception):
    pass


try:
    raise Myerror('测试自定义的异常')
except Myerror as e:
    print(e)
