from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 9001             # VRChat's OSC receiver port
client = SimpleUDPClient(ip, port)

def send_hue_shift(value):
    """Sends processed value as a hue shift parameter to VRChat."""
    print(f"Preparing to send HueShift: {value}")   # Debugging statement
    try:
        client.send_message("/avatar/parameters/HueShift", value)
        print(f"Sent: \"/avatar/parameters/HueShift\" : {value}")  # Debugging statement
    except Exception as e:
        print(f"Error sending: {e}")                # Debugging if an error occurs
