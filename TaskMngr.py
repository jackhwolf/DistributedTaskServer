from uuid import uuid4
import time
import numpy as np 

class Tasks:
    ''' class to define all the tasks that users can submit '''

    def some_long_task():
        ''' simulate a long running task '''
        x = np.random.randint(2, 8)
        time.sleep(x)
        return f'I took {x} seconds!'

    def another_long_task():
        ''' same as ^^, but diff name for examples '''
        return Tasks.some_long_task()
        
class TaskMngr:
    ''' class to help manage tasks that the user has submitted.
    this includes starting them, checking the progress, and getting
    the results back. '''
    
    def __init__(self):
        self.tasks = {}
        self.no_active_tasks = 0 
        self.defined_tasks = Tasks

    def _newtid(self):
        ''' helper function to make a new unique task id '''
        return f'{uuid4().hex}==={int(time.time()*1000)}'
        
    def submitTask(self, cli, taskfunc_key, *args, **kw):
        ''' submit a new task to be executed and tracked
        @args:
            cli:          instance of distributed.Client
            taskfunc_key: str, key to function to be executed in tasks
            args:         arguments to pass to taskfunc
            kw:           kwargs to pass to taskfunc
        @return:
            taskid if task successfully submitted, (0, msg) else
        '''
        # make sure our task is defined
        if not hasattr(self.defined_tasks, taskfunc_key):
            return 0, "task must be defined in Tasks"
        # generate a new task id and make sure it is valid
        taskid = self._newtid()
        if taskid in self.tasks:
            return 0, "task id taken"
        taskfunc = getattr(self.defined_tasks, taskfunc_key)
        # submit and track task
        future = cli.submit(taskfunc, *args, **kw)
        self.tasks[taskid] = future
        self.no_active_tasks += 1
        return taskid, "task submitted successfully"
    
    def getTaskStatus(self, tid):
        ''' get the status of a submitted task
        @args:
            tid: str, key to future in tasks dict
        @return
            str denoting status of future, or msg saying future does not exist
        '''
        if tid in self.tasks:
            return self.tasks[tid].status
        return "does not exist"
        
    def getTaskResult(self, cli, tid):
        ''' get result of task that is finished
        @args:
            tid: str, key to future in tasks dict
        @return:
            retval of future, or nothing if future DNE
        '''
        if self.getTaskStatus(tid) == 'finished':
            res = cli.gather(self.tasks[tid])
            del self.tasks[tid]
            self.no_active_tasks -= 1
            return res