from pythonosc.udp_client import SimpleUDPClient

# Debugging vars for unit testing
ip = "127.0.0.1"
port = 9000             # VRChat's OSC receiver port

client = SimpleUDPClient(ip, port)

def send_message(address, value):
    try:
        client.send_message(address, value)
        print(f"Sent: \"{address}\" : {value}")  # Debugging statement
    except Exception as e:
        print(f"Error sending: {e}")                # Debugging if an error occurs

def send_hue_shift(value):
    try:
        client.send_message("/avatar/parameters/HueShift", value)
        print(f"Sent: \"/avatar/parameters/HueShift\" : {value}")  # Debugging statement
    except Exception as e:
        print(f"Error sending: {e}")                # Debugging if an error occurs
