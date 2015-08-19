import signal
import sys
import socket


#from workersz.worker import Task
from workersz.pool import WorkerPool
import workersz.decorator as WD
from time import sleep
from time import time
from random import uniform


"""
minimalistic HTTP server using decorator
"""


              
wp = WorkerPool( count = 32 )
# client_data_target = D.worker_pool(
#       worker_pool = wp
#   ) ( client_data_target )
#
# context decorator no locks
@WD.worker_pool ( worker_pool=wp )
def client_data_target( sock, addr, resp, sz ):
    try: 
        data = None
        while True:
            data = sock.recv(sz)
            if len(data) == 0:
                break
            sock.sendall(resp)
        return
    except socket.error, e:
        print "ERR: ",repr(e)
        return

# accept ont stream socket
# and work on client_data
def connection_accept( lsock ):
    response  = "HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\nContent-Type: text/plain\r\nContent-Length: 13\r\n\r\nHello World\n\n\n\r\n"
    sz = 4096
    while True:
        sock, addr = lsock.accept()
        # just call original api
        client_data_target( sock,addr,response,sz) 
 
# handle ctr+c
def signal_handler(signal, frame):
        global wp
        wp._exit()
        print('shutdown server')
        sys.exit(0)

# main server event loop
def srv( host,port,signal, signal_handler ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn = None
    cn = 0
    while 1:
        cn+=1
        signal.signal(signal.SIGINT, signal_handler)
        connection_accept (s)

if __name__ == '__main__':
    print "starting server"
    srv('127.0.0.1',50007,signal, signal_handler )    

