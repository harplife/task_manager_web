import time, sys, signal

def signal_handler(signal, frame):
    print('\nProgram exiting gracefully.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

i = 1
while True:
    print(f'To infinity and beyond! x({i})', end='\r', flush=True)
    i += 1
    time.sleep(1)