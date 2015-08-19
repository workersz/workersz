import signal
import sys
import socket

from workersz.worker import Task
from workersz.pool import WorkerPool

from time import sleep
from time import time
from random import uniform

"""
minimalistic HTTP server using low level API
"""



def connection_accept( lsock  ):
   # wp = connection_accept.wp
    response  = "HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\nContent-Type: text/plain\r\nContent-Length: 13\r\n\r\nHello World\n\n\n\r\n"

    sz = 4096 
    while True:
        #(conn,addr)
        sock, addr = lsock.accept()
        _args = (sock,addr,response, sz)
        client_task = Task( args = _args 
                           ,target = client_data_target )
        
        wp._append_task(client_task)
        wp._commit_tasks()
                 

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
        print "SOCKET_ERROR: ",repr(e)
        return


# server program

HOST = '127.0.0.1' 
PORT = 50007      
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn = None


def signal_handler(signal, frame):
        wp._exit()
        print('closing pools')
        sys.exit(0)



wp = WorkerPool( count = 32 )
signal_handler.wp = wp
connection_accept.wp = wp

while 1:
    signal.signal(signal.SIGINT, signal_handler)
    connection_accept (s)


