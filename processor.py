from sender import send_hue_shift

def process_data(queue):
    """Continuously pulls data from the queue and processes it in real time."""
    eye_blink_left = 0
    eye_blink_right = 0
    mouth_open = 0
    # Assuming these values come in through the queue from VRCFT OSC data

    while True:
        address, value = queue.get()  # Get data from the queue
        print(f"Processing: {address} -> {value}")

        # Process different data types based on address
        if address == "/avatar/parameters/v2/eyeBlinkLeft":
            eye_blink_left = value
        elif address == "/avatar/parameters/v2/eyeBlinkRight":
            eye_blink_right = value
        elif address == "/avatar/parameters/v2/mouthOpen":
            mouth_open = value

        # Calculate average value of facial features (normalize to 0-1 range)
        # You could create more complex calculations here
        average_expression = (eye_blink_left + eye_blink_right + mouth_open) / 3

        # Normalize to 0-1 (this can also be adjusted based on your needs)
        processed_value = max(0, min(1, average_expression))

        print(f"Calculated HueShift: {processed_value}")  # Debugging statement
        
        # Send processed value to VRChat for hue shift
        send_hue_shift(processed_value)


''' # Debugging
from multiprocessing import Queue, Process
if __name__ == "__main__":
    queue = Queue()
    
    # Start the processor process
    processor_process = multiprocessing.Process(target=process_data, args=(queue,))
    processor_process.start()
'''