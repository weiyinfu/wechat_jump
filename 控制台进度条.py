import sys
import time

"""
关键在于回车符的运用
"""
cnt = 0
while 1:
    sys.stdout.write("\r程序已经运行{}秒".format(cnt))
    sys.stdout.flush()
    time.sleep(1)
    cnt += 1
