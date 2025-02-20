from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 9000  # VRChat's OSC receiver port
client = SimpleUDPClient(ip, port)

def send_hue_shift(value):
    client.send_message("/avatar/parameters/HueShift", value)

send_hue_shift(0.75)  # Example: Set hue shift based on sentiment score
