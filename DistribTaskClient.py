import requests
import json
import time

statuses = {
    'submitted': 0,
    'collected': 1
}

class DistribTaskClient:

    def __init__(self, **kw):
        self.url = kw.get('url', 'http://127.0.0.1:5000/v1')
        self.counts = {
            'submitted': 0,
            'active': 0,
            'collected': 0
        }
        self.tasks = {}

    def show_tasks(self):
        print(json.dumps(self.tasks, indent=4))

    def submit(self, endpoint, *args):
        ''' submit a task 
        @args: 
            url:     str, send request to self.url+endpoint
            args[0]: dict, optional request data
        @return: 1
        '''
        req = requests.post(self.url + endpoint, data={} if not args[0] else args[0])
        req = req.json()
        print(req)
        self.counts['submitted'] += 1
        self.counts['active'] += 1
        self.tasks[req['taskid']] = {
            'status': statuses['submitted'],
            'endpoint': endpoint,
            'data': None if not args[0] else args[0],
            'response': None,
            'submit_time': int(time.time() * 1000),
            'collect_time': -1
        }
        return 1

    def poll_collect(self):
        ''' loop thru submitted tasks and check their status. if they're 
        finished, update the counts and record the 
        '''
        while self.counts['active'] > 0:
            for taskid in self.tasks:
                if self.tasks[taskid]['status'] == statuses['submitted']:
                    req = requests.get(self.url + '/task/' + taskid).json()
                    if req['status'] == 'finished':
                        self.counts['active'] -= 1
                        self.counts['collected'] += 1
                        self.tasks[taskid]['status'] = statuses['collected']
                        self.tasks[taskid]['response'] = req
                        self.tasks[taskid]['collect_time'] = int(time.time() * 1000)
                    time.sleep(0.5)
        return 1


if __name__ == "__main__":
    dtcli = DistribTaskClient()
    dtcli.submit('/task', {'task': 'some_long_task'})
    dtcli.submit('/task', {'task': 'another_long_task'})

    print("\nDo some other work while the jobs run...")
    for i in range(3):
        print("\tdoing work...")
        time.sleep(1)
    print("done doing other work, lets check the tasks\n")

    dtcli.poll_collect()
    dtcli.show_tasks()
    
