from pythonosc import dispatcher, osc_server

def face_data_handler(address, *args):
    print(f"Received {address}: {args}")

disp = dispatcher.Dispatcher()
disp.map("/avatar/parameters/FaceData", face_data_handler)

server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9002), disp)
print("Listening for VRChat OSC messages...")
server.serve_forever()
