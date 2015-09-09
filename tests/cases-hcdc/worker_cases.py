import unittest
from time import sleep
from workersz.worker import Task as T
from workersz.worker import  WorkerThread as W 
from random import randint,uniform
from threading import Lock as L


def waiter( *args, **kwargs ):
   sleepfor = uniform(0,1)
   print "run task sleep for",sleepfor
   sleep( sleepfor )
   return sleepfor 


def waiter_err( *args, **kwargs):
    return kwargs['nonexisting']


def waiter_err_handler( w, e ):
    print e
    return e 

def waiter_done( w, r ):
    print "waiter_task_done: ",w._get_id(),
    print "result :",r
    w._exit()

def worker_done( w ):
    idd = w._get_id()
    print "worker done:",idd 
    w._exit()

def target_err( w, e):
    print "err_in_worker: ",w._get_id()
    print "err: ",repr(e)

def task_err(w,e):
    print "err_task in w : ",w._get_id()
    print "err: ",repr(e)


tasks = [
 T( target = waiter )
,T( target = waiter, task_lock = L() )
,T( target = waiter, on_done = waiter_done ) 
,T( target = waiter, on_done = waiter_done, done_lock = L() )
,T( target = waiter_err, on_err = waiter_err_handler )
,T( target = waiter_err, on_err = waiter_err_handler, err_lock = L() )
]


class TestWorker(unittest.TestCase):
    def init_workers(self):
        print "init workers"
        self.workers = [ W(i) for i in xrange(1,9) ]
        print "init done"
        
    def close_workers(self):
        print "closing workers"
        for worker in self.workers:
            worker._exit()

    def set_task(self, task):
        for worker in self.workers:
            worker._set_task(task)

    def test_worker(self):
        print "start test"
        global tasks
        self.init_workers()
        for task in tasks:
            self.init_workers()
            self.set_task(task)
            sleep(5)
            self.close_workers()


if __name__ == '__main__':
    unittest.main()
