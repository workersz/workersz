import workersz.sig
import workersz.pool
from   workersz.worker import Task
from random import uniform,randint
from time import time,sleep
from threading import Lock

from multiprocessing import Pool


S = workersz.sig.Sigtool
WP = workersz.pool.WorkerPool


def on_err( w, e ):
    print "err",w._get_id()
    print e

def on_done( w, r ):
    print " w",w._get_id()," done ",r,
    #print "task result:  ",r

def all_done(p):
    global st
    et = time()
    print "all_done",et-st 


def fA():
    n  = 21
    st = time()
    x = n 
    for i in xrange(x):
        x=x*(x+i)     
    et = time() 
    return n,et-st


st = time()
wp = WP(mp=Pool(4),count=8,all_done=all_done)

done_lock = Lock()
err_lock  = Lock()

for i in xrange(0,10):
    wp._append_task(
        Task( 
              on_done = on_done
              #,done_lock = done_lock
              ,on_err = on_err
              ,target = fA
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

