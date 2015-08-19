from worker import WorkerThread, Task
from scheduler import SchedulerThread
from time import sleep

class WorkerPool(object):
    """
    maintain asynchronous task distrubution
    over group ow working threads
    """
    #time to sleep in scheduler when all workers are busy:bsy
    DEFAULT_TICK = 0.01
    DEFAULT_WORKER_COUNT = 4
    # as lower is as scheduler loop consume more cpu over single thread

    def __init__(self,*args, **kwargs):

        if kwargs is not None:
            if 'count' in kwargs:
                self._wcnt = kwargs['count']
            else:
                self._wcnt = WorkerPool.DEFAULT_WORKER_COUNT 

            if 'all_done' in kwargs:
                self._all_done = kwargs['all_done']
            else:
                def ___pass( *args, **kwargs ):
                    pass
                self._all_done = ___pass
            if 'tick' in kwargs:
                self._tick = kwargs['tick'] 

        self._wpol = list([]) # all workers
        self._wbsy = dict({}) # busy
        self._wfre = list([]) # free
        self._tque = list([]) # task queue

        self._tick = WorkerPool.DEFAULT_TICK  # sleep time if all busy

        self._wrkr = SchedulerThread(0) # task schedule is worker
                

        self._task = Task()          # taks for scheduler
        self._task.target = self._task_schedule
        self._task.args = tuple()
        self._task.kwargs = dict()
        self._ball_done = False



        def _on_worker_task_done( worker ):
            """
            default calback for scheduler
            when some worker is done with a task
            it is appended to free workers queue
            also marked free in busy dict 
            """
            self._wfre.append(worker)
            self._wbsy[worker._id] = False

        self.____f = _on_worker_task_done 

        # pool initialization
 
        for i in xrange(1,self._wcnt+1) :
            w = WorkerThread(i)
            w._pool = self # back reference
            w._worker_task_done = self.____f
            self._wpol.append(w)
            self._wfre.append(w)
            self._wbsy[i] = False

        self._wrkr._target  = self._task_schedule
        self._wrkr._args = tuple()
        self._wrkr._kwargs = dict()
        
    def _task_schedule(self):
        """
        task scheduler worker target function: 
        check for tasks in queue 
        schedule to free workers 
        """
        #print ">>>>>>>>> task schedule"
        #loop = True
        while not self._wrkr._bexit: 
            #print "schedule loop"
            if self._tque: 
                #print "have in que"
                task = self._tque.pop()
                if  self._wfre: 
                    #print "have free workers"
                    w = self._wfre.pop()
                    success = w._set_task(task)
                    if success:
                        self._wbsy[w._id] = True
                    else:
                        #print "attach task to woker failed"
                        self._wbsy[w._id] = False
                        self._tque.append(task)
                        sleep(self._tick)
                else:
                    #print "thre is no free workers"
                    sleep(self._tick)
                    self._tque.append( task )
                self._wrkr._e.clear()
                self._wrkr._e.set()
            else:
                #print "noting in que"
                bsy_cnt = 0
                if len(self._wfre) == len(self._wpol):
                    #print "all done"
                    self._ball_done = True
                    self._all_done( self )
                    break
                    
                else:   
                    sleep(self._tick) 
                    self._wrkr._e.clear()
                    self._wrkr._e.set()

    def _task_schedule_done(self,task_result):
        #print "task chedule done"
        pass


    def _append_task(self,task):
        self._tque.append(task)

    def _commit_tasks(self):
        self._wrkr._e.clear()
        self._wrkr._e.set()

    def _exit(self):
        for w in self._wpol:
            w._exit() 
        self._wrkr._exit()
