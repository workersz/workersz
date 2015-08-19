from threading import Thread,Event


class Task(object):
    def __init__(self):
        self.on_done = None
        self.target = None
        self.args = None
        self.kwargs = None


class SchedulerThread(Thread):
 
    def __init__( self, wid ):
        # defaut target function 
        self._bexit = False
        self._bworking = False
        self._e = Event()
        self._target = None
        self._args = None 
        self._kwargs = None
        self._on_done = None
        self._id = wid
        Thread.__init__(self)
        self.start() 
        self._pool = None
        # start thread and wait to set target 
        

    def run(self):
        self._e.clear()
        while True:
            # ------- event loop ---------------------------- 
            if self._bexit: break
            # ----------------------------------------------
            # ------- to wait or not to wait before task ----
            #print "wait to schedule",self._id
            self._e.wait() 
            # -----------------------------------------------
            if self._bexit: break
            # ------- process target code ------- 
            self._bworking = True           
            self._target( *self._args, **self._kwargs ) 
            self._bworking = False
            # -----------------------------------
            if self._bexit: break #exit loop
            self._e.clear() 
                             #wait after loop
        #print "exiting thread",self           
        return 0

    def _worker_task_done(self,worker):
        pass

    def _exit(self):
        self._bexit = True
        if not self._e.is_set():
            self._e.set()

    def _notify(self):
        if not self._e.is_set():
            self._e.set()

    def _is_working(self):
        return self._bworking
  
    def _set_task(self, task ):
        if self._bworking: return False
        if self._e.is_set():
            return False
        self._on_done = task.on_done
        self._target = task.target
        self._args = task.args
        self._kwargs = task.kwargs
        self._e.set() # resume
        return True

           
    def _set_task2(self, task):
        self._on_done = task.on_done
        self._target = task.target
        self._args = task.args
        self._kwargs = task.kwargs

        if not self._e.is_set():
            self._e.set()
        

