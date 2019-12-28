## Flask server to distribute, track, and retrieve the output of long-running tasks on a cluster

### run `app.py` in one terminal and the `example.py` script in another to see it work
```
(venv) ~/py/DistributedTasks! p3 example.py 
Submitting task 1:
{
    "tid": "8e140617fa014596b40e80e40ed4eabc===1577507993445",
    "message": "task submitted successfully"
}

Submitting task 2:
{
    "tid": "d2d9b83a3a3f4cc6a85201799ac26a05===1577507993449",
    "message": "task submitted successfully"
}

Polling tasks...
 - Seconds elapsed: 0
 - T1:  {'status': 'pending'}
 - T2:  {'status': 'pending'}

 - Seconds elapsed: 1
 - T1:  {'status': 'pending'}
 - T2:  {'status': 'pending'}

 - Seconds elapsed: 2
 - T1:  {'status': 'pending'}
 - T2:  {'status': 'pending'}

 - Seconds elapsed: 3
 - T1:  {'status': 'finished', 'result': 'I took 3 seconds!'}
 - T2:  {'status': 'pending'}

 - Seconds elapsed: 4
 - T1:  {'status': 'does not exist'}
 - T2:  {'status': 'pending'}

 - Seconds elapsed: 5
 - T1:  {'status': 'does not exist'}
 - T2:  {'status': 'finished', 'result': 'I took 5 seconds!'}

 - Seconds elapsed: 6
 - T1:  {'status': 'does not exist'}
 - T2:  {'status': 'does not exist'}


Both tasks have finished

```

author: jack wolf
