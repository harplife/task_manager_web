import psutil
import subprocess
from subprocess import Popen

subp = Popen(
    ['python', 'infinite.py'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )

def print_process_info(proc_obj):
    with proc_obj.oneshot():
        print('name: ', proc_obj.name())
        print('pid: ', proc_obj.pid)
        print('cpu_times: ', proc_obj.cpu_times())
        print('cpu_percent: ', proc_obj.cpu_percent())
        print('create_time: ', proc_obj.create_time())
        print('status: ', proc_obj.status())
        print('threads: ', proc_obj.threads())
        print('exe: ', proc_obj.exe())
        try:
            parent_pid = proc_obj.ppid()
        except:
            pass
        else:
            print('parent id: ', parent_pid)
            try:
                parent = psutil.Process(parent_pid)
            except psutil.NoSuchProcess:
                print(f'NoSuchProcess: failed to find process by pid {parent_pid}')
            else:
                print('\nPrinting parent process info\n')
                print_process_info(parent)

p = psutil.Process()

print_process_info(p)
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

subp.terminate()