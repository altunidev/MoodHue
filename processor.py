from sender import send_hue_shift
import math
from collections import deque
import time
import datetime
import logging
import traceback
from facial_params_config import FACIAL_PARAMS
from sentiment import (
    calculate_emotion_scores, 
    calculate_emotion_hue, 
    smooth_value
)

def setup_logging(debug_level):
    log_levels = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
    }
    
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d | %(levelname)8s | %(message)s', 
        datefmt='%H:%M:%S'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler('facial_processing.log', mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    logging.basicConfig(
        level=log_levels.get(debug_level, logging.INFO),
        handlers=[console_handler, file_handler]
    )
    
    return logging.getLogger(__name__)

def process_data(queue, debug_level=1, throttle_ms=1000):
    # Setup logging
    logger = setup_logging(debug_level)
    logger.info(f"Starting facial parameter processor")
    logger.info(f"Debug Level: {debug_level}, Throttle: {throttle_ms}ms")
    
    facial_params = FACIAL_PARAMS.copy()
    
    # Create a mapping from all possible names to standard parameter names
    param_name_mapping = {}
    for std_name, data in facial_params.items():
        param_name_mapping[std_name] = std_name
        for alt_name in data["alt_names"]:
            param_name_mapping[alt_name] = std_name
    
    # Enhanced error tracking
    error_tracking = {
        'total_messages': 0,
        'recognized_messages': 0,
        'unrecognized_messages': 0,
        'processing_errors': 0,
        'unrecognized_params': {}
    }
    
    # Rolling window for smoothing
    window_size = 10
    value_history = deque(maxlen=window_size)
    for _ in range(window_size):
        value_history.append(0)
    
    # Performance tracking
    start_time = time.time()
    
    while True:
        try:
            # Retrieve OSC message
            address, value = queue.get(timeout=5)
            error_tracking['total_messages'] += 1
            
            # Log incoming message at debug level
            logger.debug(f"Received: {address} = {value:.4f}")
            
            # Parameter name extraction and matching
            parts = address.split('/')
            param_name = parts[-1]
            
            # Matching logic with enhanced logging
            matched = False
            std_param_name = None
            
            # Direct mapping
            if param_name in param_name_mapping:
                std_param_name = param_name_mapping[param_name]
                facial_params[std_param_name]["value"] = value
                matched = True
                error_tracking['recognized_messages'] += 1
                logger.debug(f"Direct Match: {param_name} -> {std_param_name}")
            
            # Fallback matching if not directly matched
            if not matched:
                # Case-insensitive matching
                for possible_name in param_name_mapping.keys():
                    if possible_name.lower() == param_name.lower():
                        std_param_name = param_name_mapping[possible_name]
                        facial_params[std_param_name]["value"] = value
                        matched = True
                        error_tracking['recognized_messages'] += 1
                        logger.info(f"Fuzzy Match: {param_name} → {std_param_name}")
                        break
            
            # Track unrecognized parameters
            if not matched:
                error_tracking['unrecognized_messages'] += 1
                error_tracking['unrecognized_params'][param_name] = \
                    error_tracking['unrecognized_params'].get(param_name, 0) + 1
                logger.warning(f"Unrecognized Parameter: {param_name} = {value:.4f}")
            
            # Periodic summary and performance logging
            if error_tracking['total_messages'] % 10 == 0:
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                logger.info("Parameter Processing Summary:")
                logger.info(f"  Total Messages: {error_tracking['total_messages']}")
                logger.info(f"  Recognized: {error_tracking['recognized_messages']} ({error_tracking['recognized_messages']/error_tracking['total_messages']*100:.2f}%)")
                logger.info(f"  Unrecognized: {error_tracking['unrecognized_messages']} ({error_tracking['unrecognized_messages']/error_tracking['total_messages']*100:.2f}%)")
                logger.info(f"  Processing Rate: {error_tracking['total_messages']/elapsed_time:.2f} msg/sec")
                
                # Log top unrecognized parameters
                if error_tracking['unrecognized_params']:
                    logger.info("Top Unrecognized Parameters:")
                    for param, count in sorted(error_tracking['unrecognized_params'].items(), key=lambda x: x[1], reverse=True)[:5]:
                        logger.info(f"    {param}: {count} occurrences")
            
        except Exception as e:
            error_tracking['processing_errors'] += 1
            logger.error(f"Processing Error: {str(e)}")
            logger.error(traceback.format_exc())
            
            if "Empty" in str(e):
                logger.warning("No OSC messages received in the last 5 seconds")
            
            time.sleep(1)  # Prevent rapid error logging
