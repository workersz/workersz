
import sys,signal
from time import sleep

class Sigtool():
    """
        signal handling tool
    """
        
    def __init__(self):
        self.sig_handler = {}
        self.names_sig = {
            "int":signal.SIGINT 
           ,"quit":signal.SIGQUIT
        }


    def handle( self, name, fun ):
        sig = self.names_sig[ name ]
        self.sig_handler[ sig ] = fun
    


    def loop( self ):
        while True:
            for sig_key in self.sig_handler:
                signal.signal(
                sig_key
               ,self.sig_handler[sig_key]
               )
            sleep(1000) 
    


