from workersz.pool import WorkerPool
import workersz.decorator
from   workersz.worker import Task
from random import uniform
from time import sleep
from threading import Lock




class EventHandlers(object):
    def __init__(self):
        self.done_lock = Lock()
        self.err_lock  = Lock()

    def all_done(sefl,wp):
        print "all_done",wp
        wp._exit()


    def on_err( self, e ):
        print "err",w._get_id()
        print e

    def on_done( self,w, r ):
        print "worker id done",w._get_id()
        print "task result:  ",r


class RandomWaiter(object):
    
    def __init__(self, wp_kw):
        # decorate _random_wait to run at workersz
        self.random_wait = workersz.decorator.worker_pool (
             **wp_kw ) ( self._random_wait )

  
    def _random_wait(self, a, b, key=None):
        sleepfor = uniform(0,3)
        r = (a,b,key,"A sleepfor",sleepfor)
        sleep( sleepfor )
        return r



evt = EventHandlers() 

wp = WorkerPool(count = 4, all_done = evt.all_done)

async= {
    'worker_pool':wp
   ,'task_kw':{
             'on_done':evt.on_done
             ,'done_lock':evt.done_lock
             ,'on_err':evt.on_err
             ,'err_lock':evt.err_lock
             }
   }


rndw = RandomWaiter(async)


for i in xrange(0,10):
    rndw.random_wait( i,i+1,key="test %d"%i )    


