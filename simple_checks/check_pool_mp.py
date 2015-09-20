import workersz.sig
import workersz.pool
from   workersz.worker import Task
from random import uniform
from time import sleep
from threading import Lock
from multiprocessing import Pool

S = workersz.sig.Sigtool
WP = workersz.pool.WorkerPool


def on_err( w, e ):
    print "err",w._get_id()
    print e

def on_done( w, r ):
    print "worker id done",w._get_id()
    print "task result:  ",r

def all_done(p):
    print "all_done"


def fA( a,b, key=None ):
    sleepfor = uniform(0,3)
    r = (a,b,key,"A sleepfor",sleepfor)
    sleep( sleepfor )
    return r



wp = WP(mp=Pool(4), count=8,all_done=all_done)

done_lock = Lock()
err_lock  = Lock()

for i in xrange(0,10):
    wp._append_task(
        Task( 
              on_done = on_done
              ,on_err = on_err
              #,done_lock = done_lock
              #,err_lock = err_lock
              ,target = fA
              ,args = (1,2)
              ,kwargs = { 'key':'thekey' }
            )
        )
    wp._commit_tasks()


def sigint( *args, **kwargs ):
    global wrk
    print "sigint"
    wp._exit()
    exit(0)


s = S()
s.handle('int',sigint )
s.loop()

