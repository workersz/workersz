from threading import Thread,Event,Lock


class Task(object):
    """
    task storage object
    and default async callbacks
    on_done
    on_err
    """

    def ___pass(self, *args, **kwargs):
        pass


    def _on_done( self, worker, target_result ):
        """
        def implement on_done for assynchronous task 
        def my_on_done ( task, worker, target_result )
        """
        pass

    def _on_err( self, worker, target_exception ):
        """
        def implement on_err to handle exceptions
        raised from your targets
        def my_on_err( task,worker,raised_target_exception)
        """
        pass

    def __init__(self
        ,on_done = None
        ,on_err  = None 
        ,target  = None 
        ,args    = tuple()
        ,kwargs  = dict()
        ,task_lock = None 
        ,done_lock = None
        ,err_lock  = None
        ):
          
        if on_done is not None: 
            self._on_done = on_done
        if on_err is not None:
            self._on_err = on_err

        if target is not None:
            self._target = target
        else:
            self._target = self.___pass

        self._args = args
        self._kwargs = kwargs
        self._task_lock = task_lock
        self._done_lock = done_lock
        self._err_lock  = err_lock

    # helpers
    def _lock(self,l):
        if l is not None:
            return l.acquire()
        return False

    def _unlock(self,l):
        if l is not None:
            if l.locked():
                l.release()

# proxy       
#class WorkerLock():
#    def __new__():
#        return Lock()


class DummyPool(object):
    def apply( self, f, args, kwargs):
        return apply(f,args,kwargs)


class WorkerThread(Thread):
    """
    impements Thread with event loop
    """ 
    # worker have identity 
    def __init__(  self
                  ,wid 
                  ,mp = DummyPool() 
                  ,on_worker_done = None 
                  ,on_target_err  = None 
                  ,worker_done_lock = None
                  ,worker_err_lock = None
                ):
        """ wid, [
            on_worker_done = custom callback when worker done
            on_worker_err  = custom callback when target raise
            worker_done_lock = lock for on_worker_done
            worker_err_lock = lock for on_target_err
            ]
            
            prototypes:
            on_worker_done( worker )
            on_worker_error( worker, exception )
        """
        # multiprocessing or not
        self.mp = mp
        # callbacks
        if on_worker_done is not None:
            self._worker_task_done = on_worker_done

        if on_target_err is not None:
            self._worker_task_err = on_target_err

        # locks
        self._worker_done_lock = worker_done_lock
        self._worker_err_lock  = worker_err_lock
        # controll vars 
        self._bexit = False
        self._bworking = False
        # event 
        self._e = Event()
        # task
        self._task = Task()
        # id
        self._id = wid
        # handle thread init error 
        # how to do it properly ?
        try:
            Thread.__init__(self)
            self.start() #run and wait
        except Exception,e:
            raise e

    def run(self):
        self._e.clear() # ensure will wait before loop
        while True:
            # ------- event loop ---------------------------- 
            if self._bexit: break
            # ----------------------------------------------
            # ------- to wait or not to wait before task ----
            self._e.wait() 
            # -----------------------------------------------
            if self._bexit: break
            # ------- process target code ------- 
            self._bworking = True 
            # user on done taking result from async target
            _task = self._task
            try:
                _task._lock(_task._task_lock)
                r = self.mp.apply (
                            _task._target ,  # target result
                            _task._args ,
                            _task._kwargs
                          )

                _task._unlock(_task._task_lock)
                
                _task._lock(_task._done_lock)
                _task._on_done (self,r)
                _task._unlock(_task._done_lock) 

            except Exception,e: 
                _task._unlock(_task._task_lock)
                _task._lock( self._worker_err_lock)
                self._worker_task_err( self, e )
                _task._unlock( self._worker_err_lock)

                _task._lock( _task._err_lock)
                _task._on_err(self,e) 
                _task._unlock(_task._err_lock)
            
            # tell worker is done with task and it's free
            _task._lock( self._worker_done_lock )
            self._worker_task_done( self )
            _task._unlock( self._worker_done_lock )
            self._bworking = False
            # -----------------------------------
            if self._bexit: break #exit thread loop
            self._e.clear() # pause thread 
        return 0

    def _release_locks(self):
        #todo: refactor this
        t = self._task
        t._unlock(self._worker_done_lock)
        t._unlock(self._worker_err_lock)
        t._unlock(t._task_lock)
        t._unlock(t._err_lock)
        t._unlock(t._done_lock) 
    #default worker callbacks   
    def _worker_task_done(self,worker):
        """ ( worker )
        callback when target done
        used to ctl worker when
        user target is finished 
        default implementation releae all locks 
        then worker._wexit() to stop worker
        """
        worker._release_locks() 

    def _worker_task_err(self,worker,excpt):
        """ ( worker, excpt )
        default callback when user target raise exception
        used to handle exception
        default impl here release all locks
        """ 
        worker._release_locks()

    def _exit(self):
        """
        set control var and exit Thread loop
        """
        self._bexit = True
        if not self._e.is_set():
            self._e.set()

    def _is_exiting(self):
        return self._bexit

    # helper 
    def _resume(self):
        """ notify thread to resume if waiting """
        if not self._e.is_set():
            self._e.set()

    def _is_working(self):
        return self._bworking
  
    def _set_task(self, task ):
        """
        ( Task )
        supply task to worker
        return True / False
        if success / unsuccess
        """
        # check ctl 
        if self._bworking: return False
        # check event 
        # if set thread is running
        if self._e.is_set():
            return False
        # thread is wating set task now
        self._task = task
        self._e.set() # resume Thread with set task
        return True
    #helper
    def _get_id(self):
        """ return worker id """
        return self._id
