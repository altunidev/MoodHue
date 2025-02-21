from pythonosc import dispatcher, osc_server

def debug_handler(address, *args):
    print(f"[OSC] {address}: {', '.join(map(str, args))}")

# Set up dispatcher to catch all messages
disp = dispatcher.Dispatcher()
disp.set_default_handler(debug_handler)  # Captures all messages

# Start OSC server
ip = "127.0.0.1"    # Localhost (change if needed)
port = 9000         # Make sure this matches VRChat's OSC output
server = osc_server.ThreadingOSCUDPServer((ip, port), disp)

print(f"Listening for all OSC messages on {ip}:{port}...")
server.serve_forever()
