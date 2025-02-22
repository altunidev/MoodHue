import threading
from queue import Queue
from listener import start_listener
from processor import process_data, send_hue_shift

# Configuration
IP = "127.0.0.1"
LISTEN_PORT = 9000
SEND_PORT = 9001

def run_listener():
    start_listener(queue, IP, LISTEN_PORT)

def run_processor():
    while True:
        value = queue.get()
        send_hue_shift(process_data(value)) 

if __name__ == "__main__":
    queue = Queue() 
    listener_thread = threading.Thread(target=run_listener)
    processor_thread = threading.Thread(target=run_processor)

    listener_thread.start()
    processor_thread.start()
   
    listener_thread.join()
    processor_thread.join() 

