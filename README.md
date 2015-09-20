# Asynchronous library of workers and pools for python

# Installation

    1. Check your system for setuputils
    
    2. Run setup.py in the directory (it may require root) 
        python ./setup.py install
        
# About GIL
    # GIL is in effect, so multiprocessing.Pool could be used with very basic support for CPU bound tasks
    # wp = WorkerPool( mp = Pool(4),count=4 ) # with multiprocessing 
    # wp = WorkerPool( count = 40 ) # without multiprocessing, threaded but with GIL and single process
    
# Usage
    # Simple, make any target function runnable in worker pool context
```python
    from workersz.pool import WorkerPool
    import workersz.decorator as WD
    
    # create pool with default count workers
    wp = WorkerPool()
    
    @WD.worker_pool ( worker_pool=wp )
    def my_target( *args, **kwargs ):
        pass
        # code 
```
    # Error handling and locks 
```python
from workersz.pool import WorkerPool
import workersz.decorator as WD
from time import sleep
    
#calbacks
def all_done(wp):
    # wp is WorkerPool
    print "all_done",wp
    # shutdown all workers in pool
    wp._exit()

def on_err( w, e ):
    print "err on worker id: ",w._get_id()
    print e

def on_done( w, r ):
    print "worker id done",w._get_id()
    print "task result:  ",r
 
# init pool with threads count or default 4
wp = WorkerPool( count = 32 )
    
#keyword arguments for decoration wraper on user target
    
pool_kw = { 
    'worker_pool':wp
    # keyword arguments for Task object
   ,'task_kw':{
             # callback function when task done
             # getting worker object and target result as arguments w,r
             
             'on_done':on_done     
             # make it synchronized with Threading Lock()
             ,'done_lock':done_lock
             
             # callback if target raise exception 
              ,'on_err':on_err
             # make it synchronized 
             ,'err_lock':err_lock
             }
   }
   
# example blocking target to run asynchronously 
@WD.worker_pool ( **async )
def blocking_target():
    sleepfor = uniform(0,3)
    print "sleeping for: ",sleepfor
    sleep( sleepfor )
    return r

# info attached on decoration
print blocking_target.info()
   
# tun 10 times task in parallel
for i in xrange(0,10):
    blocking_target()   
```
    # Dynamic decoration to external library function like requests.get

```python
import requests
import workersz.pool
import workersz.decorator

urls = [
 'https://api.github.com/events'
,'http://google.com'
,'http://yahoo.com'
,'http://mail.ru'
,'http://dir.bg'
,'http://somesome.tld'
]


def all_done(wp):
    print "all tasks done"
    wp._exit()

def task_done(w,r):
    print r.url, r


def task_err(w,e):
    print "err in ",w
    print "err:",e


kw = {
    'worker_pool':workersz.pool.WorkerPool( count = 5, all_done = all_done )
   ,'task_kw':{
       'on_done':task_done
      ,'on_err':task_err
      }
}


requests.get =  workersz.decorator.worker_pool( **kw )( requests.get )


for url in urls:
  print url,requests.get( url )
```

Also check resources/docs
