from multiprocessing import Queue, Process
from listener import start_listener
from processor import process_data
import argparse


IP = "127.0.0.1"
LISTEN_PORT = 9000
SEND_PORT = 9001
DEBUG_LEVEL = 2
DEBUG_THROTTLE = 500


if __name__ == "__main__":
    # Add command line arguments for debug level and throttle rate
    parser = argparse.ArgumentParser(description='VRCFT Emotion Detection')
    parser.add_argument('--debug', type=int, default=DEBUG_LEVEL, choices=[0, 1, 2],
                        help='Debug level: 0=minimal, 1=normal, 2=verbose')
    parser.add_argument('--throttle', type=int, default=DEBUG_THROTTLE,
                        help='Throttle rate in milliseconds')
    args = parser.parse_args()
    
    print(f"Starting with debug level {args.debug} and throttle rate {args.throttle}ms")
    
    queue = Queue()

    listener_process = Process(target=start_listener, args=(queue, IP, LISTEN_PORT))
    processor_process = Process(target=process_data, args=(queue, args.debug, args.throttle))

    # Fix: Add True to make processes daemon
    listener_process.daemon = True
    processor_process.daemon = True

    listener_process.start()
    processor_process.start()
    
    # Keep the main process running
    try:
        listener_process.join()
        processor_process.join()
    except KeyboardInterrupt:
        print("Shutting down...")
