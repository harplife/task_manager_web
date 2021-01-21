import psutil
import subprocess
from subprocess import Popen
import atexit
import time


#filename = 'infinite.bat'
#cmdline = [filename]
filename = 'infinite.py'
cmdline = ['python', filename],


def check(filename):
    processes = []
    for process in psutil.process_iter():
        try:
            p_cmdline = process.cmdline()
        except (PermissionError, psutil.AccessDenied):
            pass
            #print('Permission denied, moving along')
        else:
            if filename in p_cmdline:
                processes.append(process.pid)
            else:
                pass
                #print('not interested')
    return processes


def killer(filename):
    # NOTE: kills the program if it's already running
    processes = check(filename)
    for process in processes:
        p_obj = psutil.Process(process)
        try:
            p_obj.terminate()
        except Exception as e:
            raise e
        else:
            print(f'process {p_obj.pid} killed.')
    print('Nothing is alive.')
    return processes

atexit.register(killer, filename)

f = open('logs.txt', 'w')
subp = Popen(
    *cmdline,
    #['export', 'FLASK_APP=simpleweb.py', '&&', 'flask', 'run', '--host=0.0.0.0', '--port=8084'],
    stdout=f,
    stderr=subprocess.STDOUT
    )

time.sleep(5)

subp.terminate()
f.close()