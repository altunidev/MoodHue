import time
#import logging
import traceback
from typing import Dict, Any, Tuple
from collections import deque
from multiprocessing import Queue

# Import from local modules
from unified_expressions import FACIAL_PARAMS
from sentiment import (
    calculate_emotion_scores, 
    calculate_emotion_hue, 
    smooth_value
)
from sender import send_message
from utils import setup_logging  # Assuming we've created a utils module

class FacialParameterProcessor:
    def __init__(
        self, 
        queue: Queue, 
        debug_level: int = 1, 
        throttle_ms: int = 1000
    ):
        """
        Initialize the facial parameter processor
        
        Args:
            queue: Multiprocessing queue for receiving OSC messages
            debug_level: Logging verbosity (0-2)
            throttle_ms: Minimum time between processing cycles
        """
        # Setup logging
        self.logger = setup_logging(debug_level)
        
        # Configuration
        self.queue = queue
        self.debug_level = debug_level
        self.throttle_ms = throttle_ms
        
        # Initialize state
        self.facial_params = FACIAL_PARAMS.copy()
        self.param_name_mapping = self._create_param_mapping()
        
        # Error and performance tracking
        self.error_tracking = self._init_error_tracking()
        
        # Smoothing history
        self.value_history = deque(maxlen=10)
        
        # Timing
        self.start_time = time.time()
        self.last_update_time = time.time()
        
        # Log initialization
        self.logger.info(f"Facial Parameter Processor Initialized")
        self.logger.info(f"Debug Level: {debug_level}, Throttle: {throttle_ms}ms")
    
    def _create_param_mapping(self) -> Dict[str, str]:
        """
        Create a comprehensive parameter name mapping
        
        Returns:
            Dictionary mapping various parameter names to standard names
        """
        param_mapping = {}
        for std_name, data in self.facial_params.items():
            param_mapping[std_name] = std_name
            for alt_name in data.get("alt_names", []):
                param_mapping[alt_name] = std_name
        return param_mapping
    
    def _init_error_tracking(self) -> Dict[str, Any]:
        """
        Initialize error and performance tracking dictionary
        
        Returns:
            Dictionary for tracking processing metrics
        """
        return {
            'total_messages': 0,
            'recognized_messages': 0,
            'unrecognized_messages': 0,
            'processing_errors': 0,
            'unrecognized_params': {}
        }
    
    def _match_parameter(self, param_name: str) -> Tuple[bool, str, float]:
        """
        Flexibly match incoming parameter names
        
        Args:
            param_name: Incoming parameter name
        
        Returns:
            Tuple of (matched, standard_name, value)
        """
        # Direct match
        if param_name in self.param_name_mapping:
            std_name = self.param_name_mapping[param_name]
            return True, std_name, self.facial_params[std_name]["value"]
        
        # Case-insensitive match
        lower_name = param_name.lower()
        for possible_name, std_name in self.param_name_mapping.items():
            if possible_name.lower() == lower_name:
                return True, std_name, self.facial_params[std_name]["value"]
        
        return False, param_name, 0.0
    
    def _log_periodic_summary(self):
        """
        Log periodic processing summary
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        tracking = self.error_tracking
        
        self.logger.info("\nParameter Processing Summary:")
        self.logger.info(f"  Total Messages: {tracking['total_messages']}")
        self.logger.info(f"  Recognized: {tracking['recognized_messages']} "
                         f"({tracking['recognized_messages']/tracking['total_messages']*100:.2f}%)")
        self.logger.info(f"  Unrecognized: {tracking['unrecognized_messages']} "
                         f"({tracking['unrecognized_messages']/tracking['total_messages']*100:.2f}%)")
        self.logger.info(f"  Processing Rate: {tracking['total_messages']/elapsed_time:.2f} msg/sec")
        
        # Log top unrecognized parameters
        if tracking['unrecognized_params']:
            self.logger.info("Top Unrecognized Parameters:")
            for param, count in sorted(
                tracking['unrecognized_params'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]:
                self.logger.info(f"    {param}: {count} occurrences")
    
    def process(self):
        """
        Main processing loop for facial parameters
        """
        while True:
            try:
                # Retrieve OSC message with timeout
                address, value = self.queue.get(timeout=5)
                self.error_tracking['total_messages'] += 1
                
                # Log incoming message at debug level
                self.logger.debug(f"Received: {address} = {value:.4f}")
                
                # Parameter matching
                matched, std_param_name, param_value = self._match_parameter(address.split('/')[-1])
                
                if matched:
                    self.facial_params[std_param_name]["value"] = value
                    self.error_tracking['recognized_messages'] += 1
                else:
                    self.error_tracking['unrecognized_messages'] += 1
                    unrecognized_params = self.error_tracking['unrecognized_params']
                    unrecognized_params[address] = unrecognized_params.get(address, 0) + 1
                    self.logger.warning(f"Unrecognized Parameter: {address} = {value:.4f}")
                
                # Check if it's time to process and send
                current_time = time.time()
                time_diff_ms = (current_time - self.last_update_time) * 1000
                
                if time_diff_ms >= self.throttle_ms:
                    # Get current parameter values
                    current_values = {
                        name: data["value"] for name, data in self.facial_params.items()
                    }
                    
                    # Calculate emotion scores
                    emotion_scores, dominant_emotion, dominant_score = calculate_emotion_scores(current_values)
                    
                    # Calculate hue based on emotion blend
                    hue = calculate_emotion_hue(emotion_scores)
                    
                    # Smooth the hue value
                    smoothed_hue = smooth_value(self.value_history, hue)
                    
                    # Log emotion details
                    self.logger.info(f"Dominant Emotion: {dominant_emotion} (Score: {dominant_score:.2f})")
                    self.logger.info(f"Emotion Scores: {emotion_scores}")
                    self.logger.info(f"Calculated Hue: {smoothed_hue:.3f}")
                    
                    # Send smoothed hue value
                    send_message(address, value)
                    send_message("/avatar/parameters/HueShift", smoothed_hue)
                    
                    # Update last update time
                    self.last_update_time = current_time
                    
                    # Periodic summary logging
                    if self.error_tracking['total_messages'] % 100 == 0:
                        self._log_periodic_summary()
            
            except Exception as e:
                self.error_tracking['processing_errors'] += 1
                self.logger.error(f"Processing Error: {str(e)}")
                self.logger.error(traceback.format_exc())
                
                if "Empty" in str(e):
                    self.logger.warning("No OSC messages received in the last 5 seconds")
                
                time.sleep(1)  # Prevent rapid error logging

def process_data(queue: Queue, debug_level: int = 1, throttle_ms: int = 1000):
    """
    Entry point for processing facial parameters
    
    Args:
        queue: Multiprocessing queue
        debug_level: Logging verbosity
        throttle_ms: Minimum time between processing cycles
    """
    processor = FacialParameterProcessor(queue, debug_level, throttle_ms)
    processor.process()