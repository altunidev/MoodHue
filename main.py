from multiprocessing import Queue, Process
from listener import start_listener
from processor import process_data


IP = "127.0.0.1"
LISTEN_PORT = 9000
SEND_PORT = 9001


if __name__ == "__main__":
    queue = Queue()

    listener_process = Process(target=start_listener, args=(queue, IP, LISTEN_PORT))
    processor_process = Process(target=process_data, args=(queue,))

    listener_process.daemon
    processor_process.daemon

    listener_process.start()
    processor_process.start()
