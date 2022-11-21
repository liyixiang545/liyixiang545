# 自定义线程
import threading
import time
exitFlag = 0
class myThread (threading.Thread):
    # 方法初始化 必须填写4个参数 threadID：线程身份证信息，name：自定义线程名称，counter：线程执行次数，app_ip：获取的参数扔到线程进行处理
    def __init__(self, threadID, name, counter,app_id,count):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.app_id = app_id
        self.count = count
    def run(self):
        print ("开启线程： " + self.name)
        # 获取锁，用于线程同步
        T.acquire()
        # 调用print_time方法 传入线程名称，线程次数，线程状态
        print_time(self.name, self.counter,self.count)
        # 释放锁，开启下一个线程
        T.release()
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
def fun1():
    d = 0
    d+=1
    print(d)
def fun2():
    c=0
    c=c+1
    print(c)
T = threading.Lock()
threads=[]
#

# thread1 = myThread(1, "Thread-1", 1,fun1,2)
# thread2 = myThread(2, "Thread-2", 1,fun2,5)
# thread1.start()
# thread2.start()
# threads.append(thread1)
# threads.append(thread2)
#
# for t in threads:
#     t.join()
# print ("退出主线程")