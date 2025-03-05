from pythonosc import dispatcher, osc_server
from multiprocessing import Queue
import logging
from typing import Any
from config import LOGGING_CONFIG
from utils import setup_logging

def receive_osc(queue: Queue, logger: logging.Logger, address: str, *args: Any) -> None:
    """
    Process and queue incoming OSC messages with error handling
    
    Args:
        queue: Multiprocessing queue to store messages
        logger: Logging instance
        address: OSC message address
        args: Message values
    """
    try:
        # Safely extract the first argument (value)
        value = args[0] if args else None
        
        if value is not None:
            # Log received message at debug level
            logger = setup_logging(debug_level=LOGGING_CONFIG['DEBUG_LEVEL'])
            queue.put((address, value))
        else:
            logger.warning(f"Received OSC message with no value: {address}")
    
    except Exception as e:
        logger.error(f"Error processing OSC message: {e}")

def start_listener(queue: Queue, ip: str, port: int) -> None:
    """
    Start OSC listener with enhanced logging and error handling
    
    Args:
        queue: Multiprocessing queue for message passing
        ip: IP address to listen on
        port: Port to listen for messages
    """
    # Setup logger for this module
    logger = logging.getLogger(__name__)
    
    # Create dispatcher with default handler
    disp = dispatcher.Dispatcher()
    disp.set_default_handler(
        lambda addr, *args: receive_osc(queue, logger, addr, *args)
    )
    
    try:
        # Start OSC server
        server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
        logger.info(f"Listening for OSC messages on {ip}:{port}")
        
        # Serve forever
        server.serve_forever()
    
    except Exception as e:
        logger.error(f"Failed to start OSC listener: {e}")
        raise