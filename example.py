import requests
import json
import time

'''
this is a simple example script where we submit and monitor
two long running tasks. in this example, I just repeatedly
poll the API to get the status of the tasks and break when they 
are both done. I do not capture/save the result of the tasks, 
but it would be easy to do so. I just wanted to show the lifecycle
of tasks and how the api handles tasks throughout their lifetime
'''

# submit a task
task1 = requests.post('http://127.0.0.1:5000/v1/task',
                     data={'task': 'some_long_task'})
# submit another task
task2 = requests.post('http://127.0.0.1:5000/v1/task',
                     data={'task': 'another_long_task'})

# initial checkup on tasks
t1 = task1.json()
tid1 = t1['tid']
status1 = None
print("Submitting task 1:")
print(json.dumps(task1.json(), indent=4))
t2 = task2.json()
tid2 = t2['tid']
status2 = None
print("\nSubmitting task 2:")
print(json.dumps(task2.json(), indent=4))

# poll tasks
print("\nPolling tasks...")
count = 0
while 1:
    status1 = requests.get('http://127.0.0.1:5000/v1/task/' + tid1).json()
    status2 = requests.get('http://127.0.0.1:5000/v1/task/' + tid2).json()
    print(" - Seconds elapsed: " + str(count))
    print(" - T1: ", status1)
    print(" - T2: ", status2)
    print()
    status1, status2 = status1['status'], status2['status']
    if status1 == status2 == 'does not exist':
        print("\nBoth tasks have finished")
        break
    time.sleep(1)
    count += 1
    
