from multiprocessing import Queue
import multiprocessing
from sender import send_hue_shift  # Import sender function

def process_data(queue):
    """Continuously pulls data from the queue and processes it in real time."""
    while True:
        address, value = queue.get()  # Get data from the queue
        print(f"Processing: {address} -> {value}")

        # Example: Normalize value (assuming input range 0-1)
        processed_value = max(0, min(1, value))  

        # Send processed value to VRChat
        send_hue_shift(processed_value)

if __name__ == "__main__":
    queue = Queue()
    
    # Start the processor process
    processor_process = multiprocessing.Process(target=process_data, args=(queue,))
    processor_process.start()
