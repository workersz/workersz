from threading import Lock
from worker import Task


def worker(*da,**dkw): #*args, **kwargs ):
    def __wrap( func ):
        if 'worker' in dkw:
            _wrk = dkw['worker']
        else:
            # fix this
            raise Exception("there is no worker")
        if 'task_kw' in dkw:
            _task_kw = dkw['task_kw']
        else:
            _task_kw = dict({})

        def __f( *a,**kw ):
            _task_kw['target'] = func
            _task_kw['args'] = a
            _task_kw['kwargs'] = kw
            #print _task_kw 
            try:
                #print "set task"
                _wrk._set_task( Task( **_task_kw) ) 
            except Exception,e:
                 # fix this
                 print "set task failed",e
        def _info():
            return  "workerized %s"%func.__name__
        __f.info = _info 
        __f.__name__ = func.__name__
        return __f 
    return __wrap


def worker_pool(*da,**dkw): #*args, **kwargs ):
    def __wrap( func ):
        if 'worker_pool' in dkw:
            _pool = dkw['worker_pool']
        else:
            # fix this
            raise Exception("there is no worker pool")
        if 'task_kw' in dkw:
            _task_kw = dkw['task_kw']
        else:
            _task_kw = dict({})

        def __f( *a,**kw ):
            _task_kw['target'] = func
            _task_kw['args'] = a
            _task_kw['kwargs'] = kw
            #print _task_kw 
            try:
                #print "set task"
                _pool._append_task( Task( **_task_kw) )
            except Exception,e:
                 #refactor
                 print "append task failed",e
            try:
                _pool._commit_tasks()
            except Exception, e:
                 #refactor
                print "commit task failed",e_
 
        def _info():
            return  "workerpoolerized %s"%func.__name__
        __f.info = _info
        __f.__name__ = func.__name__
        return __f
    return __wrap

