'''
This script runs an a process,
and reports info about the process at a given interval.

It will check if the process is running by looking up filename.
'''

import psutil
import subprocess
from subprocess import Popen
import time, sys, signal

def signal_handler(signal, frame):
    print('\nProgram exiting gracefully.')
    sys.exit(0)

filename = 'infinite.bat'
cmdline = [filename]
#filename = 'infinite.py'
#cmdline = ['python', filename],

for process in psutil.process_iter():
    try:
        p_cmdline = process.cmdline()
    except (PermissionError, psutil.AccessDenied):
        print('Permission denied, moving along')
    else:
        if filename in p_cmdline:
            print(f'{filename} is already running')
            sys.exit(0)
        else:
            print('not interested')

print(f'Starting {filename}')

subp = Popen(
    cmdline,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )

def print_process_info(proc_obj, proc_order=1):
    with proc_obj.oneshot():
        print(f'process order {proc_order}')
        print('name: ', proc_obj.name())
        print('cmdline: ', proc_obj.cmdline())
        print('pid: ', proc_obj.pid)
        print('cpu_times: ', proc_obj.cpu_times())
        print('cpu_percent: ', proc_obj.cpu_percent())
        print('create_time: ', proc_obj.create_time())
        print('status: ', proc_obj.status())
        print('threads: ', proc_obj.threads())
        print('exe: ', proc_obj.exe())
        '''
        try:
            parent_pid = proc_obj.ppid()
        except Exception as e:
            raise e
        else:
            print('parent id: ', parent_pid)
            try:
                parent = proc_obj.parent()
            except psutil.NoSuchProcess:
                print(f'Unable to find parent, {parent_pid}')
            else:
                if parent is not None:
                    print('\nPrinting parent process info\n')
                    proc_order += 1
                    print_process_info(parent, proc_order=proc_order)
                else:
                    print(f'Unable to find parent, {parent_pid}')
        '''

p = psutil.Process(subp.pid)

while True:
    try:
        print_process_info(p)
    except (psutil.NoSuchProcess, KeyboardInterrupt):
        print('process is killed by an outsider.')
        sys.exit(0)
    else:
        time.sleep(5)
'''
    children = p.children(recursive=True)
    for child in children:
        with child.oneshot():
            print('child')
            print('name: ', child.name())
            print('pid: ', child.pid)
            print('cpu_times: ', child.cpu_times())
            print('cpu_percent: ', child.cpu_percent())
            print('create_time: ', child.create_time())
            print('parent id: ', child.ppid())
            print('status: ', child.status())
            print('threads: ', child.threads())
            print('exe: ', child.exe())
'''

'''
subp_info = psutil.Process(subp.pid)

with subp_info.oneshot():
    print('name: ', subp_info.name())
    print('pid: ', subp_info.pid)
    print('cpu_times: ', subp_info.cpu_times())
    print('cpu_percent: ', subp_info.cpu_percent())
    print('create_time: ', subp_info.create_time())
    print('parent id: ', subp_info.ppid())
    print('status: ', subp_info.status())
    print('threads: ', subp_info.threads())
    print('exe: ', subp_info.exe())
'''

#subp.terminate()