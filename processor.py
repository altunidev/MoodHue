from sender import send_hue_shift
import math
from collections import deque
import time
import datetime

def process_data(queue, debug_level=1, throttle_ms=1000):
    """
    Process facial data with parameter name matching
    """
    # Initialize parameters dictionary with both standard and alternative naming
    facial_params = {
        # Eye params
        "eyeBlinkLeft": {"value": 0, "alt_names": ["EyeBlinkLeft", "LeftEyeBlink", "LeftEyeLid"]},
        "eyeBlinkRight": {"value": 0, "alt_names": ["EyeBlinkRight", "RightEyeBlink", "RightEyeLid"]},
        "eyeOpenLeft": {"value": 0, "alt_names": ["EyeOpenLeft", "LeftEyeOpen", "LeftEyeOpening"]},
        "eyeOpenRight": {"value": 0, "alt_names": ["EyeOpenRight", "RightEyeOpen", "RightEyeOpening"]},
        "eyeSquintLeft": {"value": 0, "alt_names": ["EyeSquintLeft", "LeftEyeSquint"]},
        "eyeSquintRight": {"value": 0, "alt_names": ["EyeSquintRight", "RightEyeSquint"]},
        "eyeY": {"value": 0, "alt_names": ["EyeY"]},
        "eyeLeftX": {"value": 0, "alt_names": ["EyeLeftX"]},
        "eyeRightX": {"value": 0, "alt_names": ["EyeRightX"]},
        "eyeLidLeft": {"value": 0, "alt_names": ["EyeLidLeft"]},
        "eyeLidRight": {"value": 0, "alt_names": ["EyeLidRight"]},
        
        # Eyebrow parameters
        "browDownLeft": {"value": 0, "alt_names": ["BrowDownLeft", "LeftBrowDown", "BrowExpressionLeft"]},
        "browDownRight": {"value": 0, "alt_names": ["BrowDownRight", "RightBrowDown", "BrowExpressionRight"]},
        "browUpLeft": {"value": 0, "alt_names": ["BrowUpLeft", "LeftBrowUp", "BrowRaiseLeft"]},
        "browUpRight": {"value": 0, "alt_names": ["BrowUpRight", "RightBrowUp", "BrowRaiseRight"]},
        "browPinchLeft1": {"value": 0, "alt_names": ["BrowPinchLeft1"]},
        "browPinchRight1": {"value": 0, "alt_names": ["BrowPinchRight1"]},
        "browPinchLeft2": {"value": 0, "alt_names": ["BrowPinchLeft2"]},
        "browPinchRight2": {"value": 0, "alt_names": ["BrowPinchRight2"]},
        "browInnerUp1": {"value": 0, "alt_names": ["BrowInnerUp1"]},
        "browInnerUp2": {"value": 0, "alt_names": ["BrowInnerUp2"]},
        
        # Mouth parameters
        "mouthOpen": {"value": 0, "alt_names": ["MouthOpen", "JawOpen", "JawDrop"]},
        "jawOpen": {"value": 0, "alt_names": ["JawOpen", "JawDrop", "MouthOpen"]},
        "mouthSmile": {"value": 0, "alt_names": ["MouthSmile", "Smile", "SmileLeft", "SmileRight", "MouthCornerPull"]},
        "mouthFrown": {"value": 0, "alt_names": ["MouthFrown", "Frown", "FrownLeft", "FrownRight", "MouthCornerDepressor"]},
        "mouthPucker": {"value": 0, "alt_names": ["MouthPucker", "Pucker", "LipPucker"]},
        "mouthClosed": {"value": 0, "alt_names": ["MouthClosed"]},
        "mouthShrugUpper": {"value": 0, "alt_names": ["MouthShrugUpper", "UpperLipRaise"]},
        "mouthShrugLower": {"value": 0, "alt_names": ["MouthShrugLower", "LowerLipDepress"]},
        "mouthUpperUp1": {"value": 0, "alt_names": ["MouthUpperUp1"]},
        "mouthUpperUp2": {"value": 0, "alt_names": ["MouthUpperUp2"]},
        "mouthLowerDown1": {"value": 0, "alt_names": ["MouthLowerDown1"]},
        "mouthLowerDown2": {"value": 0, "alt_names": ["MouthLowerDown2"]},
        "mouthPress1": {"value": 0, "alt_names": ["MouthPress1"]},
        "mouthPress2": {"value": 0, "alt_names": ["MouthPress2"]},
        "tongueOut": {"value": 0, "alt_names": ["TongueOut"]},
        
        # Cheek parameters
        "cheekPuff": {"value": 0, "alt_names": ["CheekPuff", "CheekBlow"]},
        "cheekSquintLeft": {"value": 0, "alt_names": ["CheekSquintLeft", "LeftCheekSquint"]},
        "cheekSquintRight": {"value": 0, "alt_names": ["CheekSquintRight", "RightCheekSquint"]},
        "cheekPuffSuckLeft1": {"value": 0, "alt_names": ["CheekPuffSuckLeft1"]},
        "cheekPuffSuckRight1": {"value": 0, "alt_names": ["CheekPuffSuckRight1"]},
        
        # Nose parameters
        "noseSneerLeft": {"value": 0, "alt_names": ["NoseSneerLeft", "LeftNoseSneer", "NoseWrinkleLeft"]},
        "noseSneerRight": {"value": 0, "alt_names": ["NoseSneerRight", "RightNoseSneer", "NoseWrinkleRight"]},
        "noseSneer1": {"value": 0, "alt_names": ["NoseSneer1"]},
        "noseSneer2": {"value": 0, "alt_names": ["NoseSneer2"]}
    }
    
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
    
    # Emotion weight mappings
    emotion_weights = {
        "happy": {
            "mouthSmile": 0.4,
            "eyeOpenLeft": 0.15,
            "eyeOpenRight": 0.15,
            "browUpLeft": 0.15,
            "browUpRight": 0.15
        },
        "sad": {
            "mouthFrown": 0.4,
            "browDownLeft": 0.2,
            "browDownRight": 0.2,
            "eyeSquintLeft": 0.1,
            "eyeSquintRight": 0.1
        },
        "angry": {
            "browDownLeft": 0.3,
            "browDownRight": 0.3,
            "noseSneerLeft": 0.15,
            "noseSneerRight": 0.15,
            "mouthFrown": 0.1
        },
        "surprised": {
            "eyeOpenLeft": 0.2,
            "eyeOpenRight": 0.2,
            "browUpLeft": 0.2,
            "browUpRight": 0.2,
            "mouthOpen": 0.2,
            "jawOpen": 0.2
        }
    }
    
    # Fallback parameters mapping (if standard params are missing)
    fallback_mappings = {
        # If BrowExpressionLeft/Right are used, map positive values to browUp, negative to browDown
        "BrowExpressionLeft": {"positive": "browUpLeft", "negative": "browDownLeft"},
        "BrowExpressionRight": {"positive": "browUpRight", "negative": "browDownRight"}
    }
    
    # Color mapping for emotions (hue values from 0-1)
    emotion_hues = {
        "happy": 0.12,     # Yellow
        "sad": 0.65,       # Blue
        "angry": 0.95,     # Red
        "surprised": 0.3,  # Green
        "neutral": 0.0     # Red (baseline)
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
                emotion_scores = {}
                for emotion, weights in emotion_weights.items():
                    score = 0
                    for param, weight in weights.items():
                        param_value = current_values.get(param, 0)
                        score += param_value * weight
                    emotion_scores[emotion] = score
                
                # Calculate neutral score based on absence of other emotions
                other_emotions_sum = sum(emotion_scores.values())
                emotion_scores["neutral"] = max(0, 1 - other_emotions_sum)
                
                # Find the dominant emotion
                dominant_emotion = max(emotion_scores, key=emotion_scores.get)
                dominant_score = emotion_scores[dominant_emotion]
                
                # Calculate hue based on emotion blend
                hue = 0
                for emotion, score in emotion_scores.items():
                    if score > 0:
                        hue += emotion_hues[emotion] * score
                
                # Normalize in case scores add up to more than 1
                total_score = sum(emotion_scores.values())
                if total_score > 0:
                    hue = hue / total_score
                
                # Add value to rolling window
                value_history.append(hue)
                
                # Calculate smoothed value
                smoothed_hue = sum(value_history) / len(value_history)
                
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