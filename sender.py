from pythonosc.udp_client import SimpleUDPClient

# Debugging vars for unit testing
ip = "127.0.0.1"
port = 9001             # VRChat's OSC receiver port


client = SimpleUDPClient(ip, port)

def send_hue_shift(value):
    #print(f"Preparing to send HueShift: {value}")   # Debugging statement
    
    try:
        client.send_message("/avatar/parameters/HueShift", value)
        print(f"Sent: \"/avatar/parameters/HueShift\" : {value}")  # Debugging statement
    except Exception as e:
        print(f"Error sending: {e}")                # Debugging if an error occurs


'''
# provided by ChatGPT, not confirmed to work or provide bad output. Commented out for prototyping later.
from pythonosc import udp_client

def send_osc(send_queue, ip, port):
    client = udp_client.SimpleUDPClient(ip, port)
    
    while True:
        address, value = send_queue.get()
        client.send_message(address, value)
        print(f"Sent OSC: {address} -> {value}")
'''