import sys
from multiprocessing import Queue, Process

# Import from local modules
from config import OSC_CONFIG, LOGGING_CONFIG
from utils import setup_logging, validate_config, get_default_config
from listener import start_listener
from processor import process_data
from modular_processor import FacialParameterProcessor, ProcessorConfig

def setup_processes(config):
    """
    Setup listener and processor processes
    """
    queue = Queue()
    
    processor = FacialParameterProcessor(queue, ProcessorConfig(debug_level=config['debug_level']))
    processor_process = Process(target=processor.process, name="Facial-Processor")

    listener_process = Process(
        target=start_listener, 
        args=(queue, config['ip'], config['port']),
        name="OSC-Listener"
    )
    
    processor_process = Process(
        target=process_data, 
        args=(
            queue, 
            config['debug_level'], 
            config.get('throttle_ms', LOGGING_CONFIG['DEFAULT_THROTTLE_MS'])
        ),
        name="Facial-Processor"
    )
    
    listener_process.daemon = True
    processor_process.daemon = True
    
    return queue, listener_process, processor_process

def main():
    # Get default configuration
    config = get_default_config()
    
    # Setup logging
    logger = setup_logging(
        debug_level=config['debug_level']
    )
    
    # Validate configuration
    if not validate_config(config):
        logger.error("Invalid configuration")
        sys.exit(1)
    
    try:
        # Setup and start processes
        queue, listener_process, processor_process = setup_processes(config)
        
        listener_process.start()
        processor_process.start()
        
        # Wait for processes
        listener_process.join()
        processor_process.join()
    
    except KeyboardInterrupt:
        logger.info("Shutdown initiated by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        logger.info("Shutting down processes...")
        listener_process.terminate()
        processor_process.terminate()
        listener_process.join()
        processor_process.join()
        logger.info("VRCFT Emotion Detection system shut down.")


if __name__ == "__main__":
    main()