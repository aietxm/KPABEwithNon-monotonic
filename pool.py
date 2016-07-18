__author__ = 'cirnotxm'
from threading import Thread
from Queue import Queue
from time import sleep
class ThreadPool():

    def __init__(self):
        self.q = Queue()
        self.NUM = 3
        self.JOBS = 10

    def do_somthing_using(self,arguments):
        print arguments

    def working(self):
        while True:
            arguments = self.q.get()
            self.do_somthing_using(arguments+1)
            sleep(1)
            self.q.task_done()
    def PoolStart(self):
        for i in range(self.NUM):
            t = Thread(target=self.working)
            t.setDaemon(True)
            t.start()

        for i in range(self.JOBS):
            self.q.put(i)
        self.q.join()


test = ThreadPool()
test.PoolStart()