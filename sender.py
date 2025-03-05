from pythonosc.udp_client import SimpleUDPClient
import logging
from typing import Optional

class OSCSender:
    def __init__(
        self, 
        ip: str = "127.0.0.1", 
        port: int = 9000, 
        logger: Optional[logging.Logger] = None
    ):
        self.client = SimpleUDPClient(ip, port)
        self.logger = logger or logging.getLogger(__name__)
    
    def send_message(
        self, 
        address: str = "/avatar/parameters/HueShift", 
        value: float = 0.0
    ) -> bool:
        """
        Send OSC message with optional default for hue shift
        
        Args:
            address: OSC message address (defaults to hue shift)
            value: Message value
        
        Returns:
            Boolean indicating successful message send
        """
        try:
            self.client.send_message(address, value)
            self.logger.debug(f"Sent: \"{address}\" : {value}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message to {address}: {e}")
            return False

# Module-level sender for backward compatibility
sender = OSCSender()
send_message = sender.send_message