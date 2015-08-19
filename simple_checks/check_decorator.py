from time import sleep
from random import uniform
import workersz.worker
import workersz.decorator
import workersz.sig
from  threading import Lock

W = workersz.worker.WorkerThread
D = workersz.decorator
L = Lock
S = workersz.sig.Sigtool
done_lock = L()
err_lock = L()
#workers    = [ W(1),W(2),W(3) ]

wrk = W(1)
wrk1 = W(2)
def on_done( w, r ):
    print "worker id done",w._get_id()
    print "task result:  ",r


def on_err( w, e ):
    print "ERR",w._get_id(),e

async = { 
    'worker':wrk
   ,'task_kw':{       
             'on_done':on_done      
             ,'done_lock':done_lock
              ,'on_err':on_err
             #,'err_lock':err_lock
             }
   }  
sync = {
    'worker':wrk1
   ,'task_kw':{
             #'on_done':on_done
             #,'done_lock':done_lock
             'on_err':on_err
             ,'task_lock':done_lock
             }
   }  



@D.worker(  **async ) 
def fA( a,b, key=None ):
    sleepfor = uniform(0,3)
    r = (a,b,key,"A sleepfor",sleepfor)
    sleep( sleepfor )
    return r 

@D.worker( **sync )
def fB( k,s,fss,v="" ):
    print "ok",k,s,fss
    


fA(1,2,key="test")
fB(100,200,300)


def sigint( *args, **kwargs ):
    global wrk
    print "sigint"
    #print "stoping test workers"
    wrk._exit()
    wrk1._exit()
    exit(0)

    
s = S()
s.handle('int',sigint )
s.loop()
