from pythonosc import dispatcher, osc_server

def receive_osc(queue, address, *args):
    data = (address, args[0])       # Store address and value
    queue.put(data)                 # Send data to the processor
    #print(f"Received OSC: {data}")

def start_listener(queue, ip, port):

    disp = dispatcher.Dispatcher()
    disp.set_default_handler(lambda addr, *args: receive_osc(queue, addr, *args))
    
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Listening for OSC messages on {ip}:{port}...")
    server.serve_forever()


'''# Unit testing
from multiprocessing import Queue, Process
from processor import process_data

if __name__ == "__main__":
    queue = Queue()

    IP = "127.0.0.1"
    LISTEN_PORT = 9000
    SEND_PORT = 9001

    # Start the listener process
    listener_process = Process(target=start_listener, args=(queue, IP, LISTEN_PORT))
    listener_process.start()

    # Start the processor process
    processor_process = Process(target=process_data, args=(queue,))
    processor_process.start()
'''