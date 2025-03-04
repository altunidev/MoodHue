from sender import send_hue_shift
import math
from collections import deque
import time
import datetime
from facial_params_config import FACIAL_PARAMS
from sentiment import (
    calculate_emotion_scores, 
    calculate_emotion_hue, 
    smooth_value
)

def process_data(queue, debug_level=1, throttle_ms=1000):
    """
    Process facial data with parameter name matching
    """
    # Initialize parameters dictionary with both standard and alternative naming
    facial_params = FACIAL_PARAMS.copy()
    
    # Create a mapping from all possible names to standard parameter names
    param_name_mapping = {}
    for std_name, data in facial_params.items():
        # Add the standard name itself
        param_name_mapping[std_name] = std_name
        # Add all alternative names
        for alt_name in data["alt_names"]:
            param_name_mapping[alt_name] = std_name
    
    # Create a rolling window for smoothing output
    window_size = 10
    value_history = deque(maxlen=window_size)
    for _ in range(window_size):
        value_history.append(0)
    
    # Fallback parameters mapping (if standard params are missing)
    fallback_mappings = {
        # If BrowExpressionLeft/Right are used, map positive values to browUp, negative to browDown
        "BrowExpressionLeft": {"positive": "browUpLeft", "negative": "browDownLeft"},
        "BrowExpressionRight": {"positive": "browUpRight", "negative": "browDownRight"}
    }
    
    # For throttling outputs
    last_update_time = time.time()
    update_counter = 0
    recognized_counter = 0
    unrecognized_counter = 0
    
    # Dictionary to track unrecognized parameters for reporting
    unrecognized_params = {}
    
    def debug_print(level, message):
        """Print message only if debug level is sufficient"""
        if debug_level >= level:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {message}")
    
    debug_print(0, f"Starting processor with enhanced parameter matching")
    debug_print(0, f"Debug level: {debug_level}, Throttle: {throttle_ms}ms")
    
    while True:
        try:
            address, value = queue.get(timeout=5)  # 5 second timeout for diagnostics
            
            # Extract parameter name from address
            parts = address.split('/')
            param_name = parts[-1]  # Get the last part after splitting
            
            # Try to map to a standard parameter name
            matched = False
            std_param_name = None
            
            # Direct mapping via our dictionary
            if param_name in param_name_mapping:
                std_param_name = param_name_mapping[param_name]
                facial_params[std_param_name]["value"] = value
                matched = True
                recognized_counter += 1
                debug_print(2, f"✓ Parameter: {param_name} → {std_param_name} = {value:.3f}")
            
            # Special handling for expression parameters
            elif param_name in fallback_mappings:
                debug_print(2, f"! Expression parameter: {param_name} = {value:.3f}")
                mapping = fallback_mappings[param_name]
                
                if value > 0:
                    std_param_name = mapping["positive"]
                    facial_params[std_param_name]["value"] = value
                    debug_print(2, f"  Mapped to: {std_param_name} (positive) = {value:.3f}")
                else:
                    std_param_name = mapping["negative"]
                    facial_params[std_param_name]["value"] = -value  # Convert negative to positive
                    debug_print(2, f"  Mapped to: {std_param_name} (negative) = {-value:.3f}")
                
                matched = True
                recognized_counter += 1
            
            # Fuzzy matching as a last resort
            if not matched:
                # Try case-insensitive matching
                for possible_name in param_name_mapping.keys():
                    if possible_name.lower() == param_name.lower():
                        std_param_name = param_name_mapping[possible_name]
                        facial_params[std_param_name]["value"] = value
                        matched = True
                        recognized_counter += 1
                        debug_print(1, f"~ Close match: {param_name} → {std_param_name} = {value:.3f}")
                        break
            
            # If still no match, log the unrecognized parameter
            if not matched:
                unrecognized_counter += 1
                if param_name in unrecognized_params:
                    unrecognized_params[param_name] += 1
                else:
                    unrecognized_params[param_name] = 1
                    debug_print(1, f"✗ Unrecognized: {param_name} = {value:.3f}")
            
            # Only process and send updates at the throttled rate
            current_time = time.time()
            time_diff_ms = (current_time - last_update_time) * 1000
            
            if time_diff_ms >= throttle_ms:
                update_counter += 1
                debug_print(1, f"--- Processing update #{update_counter} ---")
                debug_print(1, f"Recognized: {recognized_counter}, Unrecognized: {unrecognized_counter}")
                
                # Get current parameter values
                current_values = {name: data["value"] for name, data in facial_params.items()}
                
                # Calculate emotion scores
                emotion_scores, dominant_emotion, dominant_score = calculate_emotion_scores(current_values)
                
                # Calculate hue based on emotion blend
                hue = calculate_emotion_hue(emotion_scores)
                
                # Smooth the hue value
                smoothed_hue = smooth_value(value_history, hue)
                
                # Log active parameters
                if debug_level >= 2:
                    debug_print(2, "Active parameters:")
                    for name, data in facial_params.items():
                        if data["value"] > 0.05:  # Only show non-trivial values
                            debug_print(2, f"  {name}: {data['value']:.3f}")
                
                # Log the emotion detection results
                debug_print(1, "Emotion Scores:")
                for emotion, score in emotion_scores.items():
                    if score > 0.05:  # Only show non-trivial emotions
                        debug_print(1, f"  {emotion}: {score:.3f}")
                
                debug_print(0, f"Dominant: {dominant_emotion} ({dominant_score:.2f}) → HueShift: {smoothed_hue:.3f}")
                
                # Send smoothed hue value
                send_hue_shift(smoothed_hue)
                
                # Update the last update time
                last_update_time = current_time
                
                # Periodically report any unrecognized parameters
                if update_counter % 10 == 0 and unrecognized_params:
                    debug_print(1, "Unrecognized parameters summary:")
                    for param, count in sorted(unrecognized_params.items(), key=lambda x: -x[1]):
                        debug_print(1, f"  {param}: {count} occurrences")
        
        except Exception as e:
            debug_print(0, f"ERROR: {str(e)}")
            if "Empty" in str(e):
                debug_print(0, "No OSC messages received in the last 5 seconds")
            time.sleep(1)  # Prevent rapid error logging

# Helper function to get parameter values more easily
def get_param_value(facial_params, param_name):
    return facial_params[param_name]["value"]