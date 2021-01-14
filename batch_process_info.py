import psutil
import subprocess
from subprocess import Popen

subp = Popen(
    'infinite.bat',
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )

p = psutil.Process()

with p.oneshot():
    print('name: ', p.name())
    print('cpu_times: ', p.cpu_times())
    print('cpu_percent: ', p.cpu_percent())
    print('create_time: ', p.create_time())
    print('parent id: ', p.ppid())
    print('status: ', p.status())
    print('threads: ', p.threads())
    print('exe: ', p.exe())
    children = p.children(recursive=True)
    for child in children:
        with child.oneshot():
            print('child')
            print('name: ', child.name())
            print('cpu_times: ', child.cpu_times())
            print('cpu_percent: ', child.cpu_percent())
            print('create_time: ', child.create_time())
            print('parent id: ', child.ppid())
            print('status: ', child.status())
            print('threads: ', child.threads())
            print('exe: ', child.exe())

subp.terminate()