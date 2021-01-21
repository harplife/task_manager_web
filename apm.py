'''
APM program that starts and monitors an application.

Functions:
1. Starts a web server
2. Starts a subprocess that runs
3. apscheduler? monitors the subprocess at interval
4. save data to db
5. web server to display data


NOTE:
1. use context start/close to terminate subprocesses properly.
   Otherwise, flask seems to hang on next startup
'''

from flask import Flask, g, redirect, url_for
import psutil
import subprocess
from subprocess import Popen
import atexit


filename = 'infinite.bat'
cmdline = [filename]
#filename = 'infinite.py'
#cmdline = ['python', filename],


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


app = Flask(__name__)

atexit.register(killer, filename)


@app.route('/')
def index():
    processes = check(filename)
    if len(processes) > 0:
        return redirect(url_for('running'))
    else:
        return redirect(url_for('start_subp'))


@app.route('/running')
def running():
    processes = check(filename)
    return {'running': processes}


@app.route('/start')
def start_subp():
    processes = check(filename)
    if len(processes) > 0:
        return redirect(url_for('running'))
    else:
        subp = Popen(
            cmdline,
            #['export', 'FLASK_APP=simpleweb.py', '&&', 'flask', 'run', '--host=0.0.0.0', '--port=8084'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            )
        #g.subp_id = subp.pid
        return {'status': 'started', 'id': subp.pid}


@app.route('/stop/<pid>')
def stop_subp(pid):
    pid = int(pid)
    try:
        p = psutil.Process(pid)
    except (psutil.NoSuchProcess):
        return {'status': f'No Process Found by pid {pid}'}
    else:
        try:
            p.terminate()
        except Exception as e:
            raise e
        else:
            return {'status': f'process {pid} terminated'}


@app.route('/monitor/<pid>')
def monitor_subp(pid):
    pid = int(pid)
    try:
        p = psutil.Process(pid)
    except (psutil.NoSuchProcess):
        return {'status': f'No Process Found by pid {pid}'}
    else:
        response = {}
        with p.oneshot():
            response['name'] = p.name()
            response['status'] = p.status()
            response['cmdline'] = p.cmdline()
        return response


if __name__ == '__main__':
    killer(filename)
    app.run(use_reloader=False, port=8083, host='0.0.0.0')