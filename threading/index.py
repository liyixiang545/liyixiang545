import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开启线程： " + self.name)
        # 获取锁，用于线程同步
        T.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁，开启下一个线程
        T.release()
def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
T = threading.Lock()
threads=[]
#
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
# thread1.start()
# thread2.start()
# threads.append(thread1)
# threads.append(thread2)
#
# for t in threads:
#     t.join()
# print ("退出主线程")