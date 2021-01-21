# PSUTIL Web Console

## 개요

I want:

1. monitor processes and threads
2. specifically monitor a program (such as java, or python)
3. run flask and provide real-time monitoring
4. save log to DB to view history
5. add in Alarm for when there's any SPIKE

## Dependencies

1. psutil = 5.8.0
2. flask == 1.1.2

## Current Functions

1. Flask Web Server
2. HTML with Ajax query
3. Listing all processes
4. Find process by name
5. TODO: monitor CPU usuage
6. TODO: Find "main" processes, and list its children

## TODO

1. Flask + SocketIO for streaming process STDOUT and STDERR
    - [ref1](https://medium.com/swlh/implement-a-websocket-using-flask-and-socket-io-python-76afa5bbeae1)
    - [ref2](https://stackoverflow.com/a/38643387/10570582)

## by file explanation

### apm.py

running `apm.py` will start a flask app that can start/stop/monitor a process.

#### details

1. it runs flask app
2. `/start/number` will Popen on a given file (e.g. infinite.bat), on a given number of times
3. `/running` will return pids of processes that are running the file
4. `/stop` will stop all procesess that are running the file
5. `/monitor` will give information about all proceses running the file

## NOTE

1. Flask can't clean up after subprocess properly. atexit.register() is required. Moe tails [here](https://medium.com/better-programming/create-exit-handlers-for-your-python-appl-bc279e796b6b)
2. Flask has a weird thing where it initializes things twice. More detail [here](https://stackoverflow.com/a/15491587/10570582)
