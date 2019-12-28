## Flask server to distribute, track, and retrieve the output of long-running tasks on a cluster.

## an example, with the server running on top and the client script being executed on bottom
you can see the client polling the server, initially sending a `GET` for both tasks, until one of them
finishes. Then it only polls for the remaining active task. Once both tasks complete, the client closes.
<img src='example.png'/>