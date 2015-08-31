import requests

import workersz.pool
import workersz.decorator
import workersz.sig
from  threading import Lock


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

