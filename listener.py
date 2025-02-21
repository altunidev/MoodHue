from pythonosc import dispatcher, osc_server
from multiprocessing import Queue, Process
from processor import process_data  # Import processor function

def receive_osc(queue, address, *args):
    """Receives OSC messages and stores them in a multiprocessing queue."""
    data = (address, args[0])       # Store address and value
    queue.put(data)                 # Send data to the processor
    print(f"Received OSC: {data}")

def start_listener(queue):
    """Starts an OSC listener server and forwards data to a queue."""
    ip = "127.0.0.1"
    port = 9000  # Ensure this matches your VRCFT output port

    disp = dispatcher.Dispatcher()
    disp.set_default_handler(lambda addr, *args: receive_osc(queue, addr, *args))

    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Listening for OSC messages on {ip}:{port}...")
    server.serve_forever()

if __name__ == "__main__":
    queue = Queue()

    # Start the listener process
    listener_process = Process(target=start_listener, args=(queue,))
    listener_process.start()

    # Start the processor process
    processor_process = Process(target=process_data, args=(queue,))
    processor_process.start()
