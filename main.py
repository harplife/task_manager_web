from flask import Flask, render_template
import psutil
import time
from operator import itemgetter

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def time_to_str(proc_list):
    time_format = '%Y-%m-%d %H:%M:%S'
    for x in proc_list:
        x['create_time'] = time.strftime(time_format, time.localtime(x['create_time']))

    return proc_list


def use_psutil(timetostr=True, tojson=True):
    captured_processes = []
    for proc in psutil.process_iter():
        captured_processes.append(proc)

    proc_info = []
    for proc in captured_processes:
        info = proc.as_dict(attrs=['name', 'pid', 'status', 'create_time'])
        proc_info.append(info)

    proc_sorted = sorted(proc_info, key=itemgetter('create_time'), reverse=True)

    if timetostr:
        proc_sorted = time_to_str(proc_sorted)

    if tojson:
        proc_sorted_json = {count: value for count, value in enumerate(proc_sorted)}

        return proc_sorted_json
    else:
        return proc_sorted


@app.route('/query_procs')
def query_procs():
    proc_sorted_json = use_psutil()

    return proc_sorted_json


@app.route('/processes')
def processes():
    return render_template('ajax_processes.html')


@app.route('/query_by_name/<name>')
def query_by_name(name):
    # TODO: create an AJAX call to query this function with user input
    proc_list = use_psutil(timetostr=False, tojson=False)
    found = []
    for proc in proc_list:
        if name in proc['name']:
            found.append(proc)
    
    proc_sorted = time_to_str(found)
    proc_sorted_json = {count: value for count, value in enumerate(proc_sorted)}

    return proc_sorted_json


if __name__ == '__main__':
    app.run(debug=True, port=8084, host='0.0.0.0')