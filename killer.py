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
            process.terminate()
            print('termination complete')
            sys.exit(0)
        else:
            print('not interested')