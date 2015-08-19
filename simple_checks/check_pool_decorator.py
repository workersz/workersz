import workersz.sig
import workersz.pool
import workersz.decorator
from   workersz.worker import Task
from random import uniform
from time import sleep
from threading import Lock

S = workersz.sig.Sigtool
WP = workersz.pool.WorkerPool
D = workersz.decorator


done_lock = Lock()
err_lock  = Lock()


def all_done(wp):
    print "all_done",wp

wp = WP(count=4,all_done=all_done)

def on_err( w, e ):
    print "err",w._get_id()
    print e

def on_done( w, r ):
    print "worker id done",w._get_id()
    print "task result:  ",r

async = {
    'worker_pool':wp
   ,'task_kw':{
             'on_done':on_done
             ,'done_lock':done_lock
             ,'on_err':on_err
             ,'err_lock':err_lock
             }
   }


@D.worker_pool ( **async )
def fA( a,b, key=None ):
    sleepfor = uniform(0,3)
    r = (a,b,key,"A sleepfor",sleepfor)
    sleep( sleepfor )
    return r

print fA.info()

for i in xrange(0,10):
    fA( i,i+1,key="test %d"%i )    

def sigint( *args, **kwargs ):
    global wp
    print "sigint"
    wp._exit()
    exit(0)


s = S()
s.handle('int',sigint )
s.loop()

