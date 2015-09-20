import requests

import workersz.pool
import workersz.decorator
import workersz.sig
from  threading import Lock
from time import sleep
from multiprocessing import Pool

urls = [
 'https://api.github.com/events'
,'http://google.com'
,'http://yahoo.com'
,'http://mail.ru'
,'http://dir.bg'
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
    'worker_pool':workersz.pool.WorkerPool(mp=Pool(4), count = 10, all_done = all_done ) 
   ,'task_kw':{ 
       'on_done':task_done 
      ,'on_err':task_err 
      }
}


requests.get =  workersz.decorator.worker_pool( **kw )( requests.get )

for i in xrange(10):
    for url in urls:
        requests.get( url )


