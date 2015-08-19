from time import sleep
from workersz.worker import Task as T
from workersz.worker import  WorkerThread as W
from random import randint,uniform
from threading import Lock



def ctl_target( workers):
    import sys,signal
    def signal_handler(signal, frame):
        print "closing all workers"
        for worker in workers:
            print "closing worker",worker._get_id()
            worker._exit()
        sys.exit(0)
    while True:
        #print "wait for sig"
        signal.signal(signal.SIGINT, signal_handler)
        sleep(100) 

def waiter( *args, **kwargs ):
   idd = kwargs['worker']._get_id()
   sleepfor = uniform(0,1)
   sleep( sleepfor )
#   print res[ randint(0,50) ]
   return idd

def waiter_done( w, r ):
    print "waiter_task_done: ",w._get_id(),
    print "result :",r
    w._exit()

def worker_done( w ):
    global res
    idd = w._get_id()
    print "wrkdone:",idd 
    w._exit()

def target_err( w, e):
    print "err_in_worker: ",w._get_id()
    print "err: ",repr(e)
    #w._exit()
    #w._release_locks()

def task_err(w,e):
    print "err_task in w : ",w._get_id()
    print "err: ",repr(e)
 

locks = [ Lock() for i in xrange(1,100) ]



workers = [ W(i) for i in xrange(1,9) ] 


for worker in workers:
    worker._set_task( 
      T(    target = waiter 
           ,on_done = waiter_done 
           ,on_err = task_err 
           #,task_lock =  locks[2] 
           ,err_lock = locks[3] 
           ,done_lock = locks[4] 
           ,kwargs = {
               'worker':worker
            }
          )
       )

ctl_target( workers )


