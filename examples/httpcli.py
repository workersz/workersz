import socket
from time import sleep
from time import time
from workersz.pool import WorkerPool
import workersz.decorator as WD
import signal
import sys
from threading import Lock



HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

from time import time
cnt = 0 
cntcount = 100000
RQ_SZ = 4096
rqsize =  4096 

REQUEST="""
GET /ok HTTP/1.1
Host: 127.0.0.1:50007
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36
Content-Type: text/plain; charset=utf-8
Accept: */*
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en-US,en;q=0.8
"""

def on_connect( w, r ):
     print "snddrcv"
     sendreceive(r)
     print "sndrcv"


def on_receive(w,r):
    k = r
    pass

def all_done( p ):
    print "all done timing", time() - all_done.st  
     

def on_error( w, e ):
    print "err",w._get_id(),e

wp = WorkerPool ( count = 4 , all_done = all_done)


done_lock = Lock()
task_lock = Lock()

rcv = {
    'worker_pool':wp
   ,'task_kw':{
             'on_done':on_receive
             #,'task_lock':done_lock
             #,'done_lock':done_lock
             }

}


@WD.worker_pool ( **rcv)
def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST,PORT))
    sock.sendall(REQUEST)
    resp = sock.recv( RQ_SZ )
    sock.close()
    return resp 

def signal_handler(signal, frame):
        global wp
        wp._exit()
        print('shutdown client')
        sys.exit(0)

for i in xrange(1,128):
    all_done.st = time()
    connect()
    

signal.signal(signal.SIGINT, signal_handler)
sleep(100000)

