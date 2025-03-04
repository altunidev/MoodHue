from sender import send_hue_shift
import math
from collections import deque
import time
import datetime
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

        # Additional Eye Squint parameters
        "EyeSquintLeft1": {"value": 0, "alt_names": ["EyeSquintLeft1"]},
        "EyeSquintRight1": {"value": 0, "alt_names": ["EyeSquintRight1"]},
        "EyeSquintLeft2": {"value": 0, "alt_names": ["EyeSquintLeft2"]},
        "EyeSquintRight2": {"value": 0, "alt_names": ["EyeSquintRight2"]},
        
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
        "BrowPinchLeft4": {"value": 0, "alt_names": ["BrowPinchLeft4"]},
        "BrowPinchRight4": {"value": 0, "alt_names": ["BrowPinchRight4"]},
        "BrowInnerUp4": {"value": 0, "alt_names": ["BrowInnerUp4"]},
        "BrowExpressionLeft1": {"value": 0, "alt_names": ["BrowExpressionLeft1"]},
        "BrowExpressionRight1": {"value": 0, "alt_names": ["BrowExpressionRight1"]},
        "BrowExpressionLeft2": {"value": 0, "alt_names": ["BrowExpressionLeft2"]},
        "BrowExpressionRight2": {"value": 0, "alt_names": ["BrowExpressionRight2"]},
        "BrowExpressionLeft4": {"value": 0, "alt_names": ["BrowExpressionLeft4"]},
        "BrowExpressionRight4": {"value": 0, "alt_names": ["BrowExpressionRight4"]},
        
        # Mouth parameters
        "mouthOpen": {"value": 0, "alt_names": ["MouthOpen", "JawOpen", "JawDrop"]},
        "jawOpen": {"value": 0, "alt_names": ["JawOpen", "JawDrop", "MouthOpen"]},
        "mouthSmile": {"value": 0, "alt_names": ["MouthSmile", "Smile", "SmileLeft", "SmileRight", "MouthCornerPull"]},
        "mouthFrown": {"value": 0, "alt_names": ["MouthFrown", "Frown", "FrownLeft", "FrownRight", "MouthCornerDepressor"]},
        "mouthPucker": {"value": 0, "alt_names": ["MouthPucker", "Pucker", "LipPucker"]},
        "mouthClosed": {"value": 0, "alt_names": ["MouthClosed"]},
        "MouthClosed1": {"value": 0, "alt_names": ["MouthClosed1"]},
        "MouthClosed2": {"value": 0, "alt_names": ["MouthClosed2"]},
        "MouthClosed4": {"value": 0, "alt_names": ["MouthClosed4"]},
        "MouthClosed8": {"value": 0, "alt_names": ["MouthClosed8"]},
        "MouthDimple1": {"value": 0, "alt_names": ["MouthDimple1"]},
        "MouthDimple2": {"value": 0, "alt_names": ["MouthDimple2"]},
        "mouthShrugUpper": {"value": 0, "alt_names": ["MouthShrugUpper", "UpperLipRaise"]},
        "mouthShrugLower": {"value": 0, "alt_names": ["MouthShrugLower", "LowerLipDepress"]},
        "mouthUpperUp1": {"value": 0, "alt_names": ["MouthUpperUp1"]},
        "mouthUpperUp2": {"value": 0, "alt_names": ["MouthUpperUp2"]},
        "mouthLowerDown1": {"value": 0, "alt_names": ["MouthLowerDown1"]},
        "mouthLowerDown2": {"value": 0, "alt_names": ["MouthLowerDown2"]},
        "mouthPress1": {"value": 0, "alt_names": ["MouthPress1"]},
        "mouthPress2": {"value": 0, "alt_names": ["MouthPress2"]},
        
        # Mouth Raiser parameters
        "MouthRaiserLower1": {"value": 0, "alt_names": ["MouthRaiserLower1"]},
        "MouthRaiserLower2": {"value": 0, "alt_names": ["MouthRaiserLower2"]},
        "MouthRaiserLower4": {"value": 0, "alt_names": ["MouthRaiserLower4"]},
        "MouthRaiserUpper1": {"value": 0, "alt_names": ["MouthRaiserUpper1"]},
        "MouthRaiserUpper2": {"value": 0, "alt_names": ["MouthRaiserUpper2"]},
        "MouthUpperUp4": {"value": 0, "alt_names": ["MouthUpperUp4"]},
        "MouthUpperUp8": {"value": 0, "alt_names": ["MouthUpperUp8"]},
        "MouthLowerDown4": {"value": 0, "alt_names": ["MouthLowerDown4"]},

        # Mouth position parameters
        "MouthX1": {"value": 0, "alt_names": ["MouthX1"]},
        "MouthX2": {"value": 0, "alt_names": ["MouthX2"]},
        "MouthX4": {"value": 0, "alt_names": ["MouthX4"]},
        "MouthX8": {"value": 0, "alt_names": ["MouthX8"]},
        "MouthXNegative": {"value": 0, "alt_names": ["MouthXNegative"]},

        # Jaw parameters
        "JawZ1": {"value": 0, "alt_names": ["JawZ1"]},
        "JawZ2": {"value": 0, "alt_names": ["JawZ2"]},
        "JawZ4": {"value": 0, "alt_names": ["JawZ4"]},
        "JawX1": {"value": 0, "alt_names": ["JawX1"]},
        "JawX2": {"value": 0, "alt_names": ["JawX2"]},
        "JawX4": {"value": 0, "alt_names": ["JawX4"]},
        "JawXNegative": {"value": 0, "alt_names": ["JawXNegative"]},
        "JawForward1": {"value": 0, "alt_names": ["JawForward1"]},
        "JawForward2": {"value": 0, "alt_names": ["JawForward2"]},
        "JawForward4": {"value": 0, "alt_names": ["JawForward4"]},
        "JawOpen1": {"value": 0, "alt_names": ["JawOpen1"]},
        "JawOpen2": {"value": 0, "alt_names": ["JawOpen2"]},
        "JawOpen4": {"value": 0, "alt_names": ["JawOpen4"]},
        "JawOpen8": {"value": 0, "alt_names": ["JawOpen8"]},
        "JawOpen16": {"value": 0, "alt_names": ["JawOpen16"]},
        
        # Lip parameters
        "LipSuckLower1": {"value": 0, "alt_names": ["LipSuckLower1"]},
        "LipSuckLower2": {"value": 0, "alt_names": ["LipSuckLower2"]},
        "LipSuckLower4": {"value": 0, "alt_names": ["LipSuckLower4"]},
        "LipSuckUpper1": {"value": 0, "alt_names": ["LipSuckUpper1"]},
        "LipSuckUpper2": {"value": 0, "alt_names": ["LipSuckUpper2"]},
        "LipSuckUpper4": {"value": 0, "alt_names": ["LipSuckUpper4"]},
        "LipPucker1": {"value": 0, "alt_names": ["LipPucker1"]},
        "LipPucker2": {"value": 0, "alt_names": ["LipPucker2"]},
        "LipPucker4": {"value": 0, "alt_names": ["LipPucker4"]},
        "LipFunnel1": {"value": 0, "alt_names": ["LipFunnel1"]},
        "LipFunnel2": {"value": 0, "alt_names": ["LipFunnel2"]},
        "LipFunnel4": {"value": 0, "alt_names": ["LipFunnel4"]},

        # Tongue parameters
        "tongueOut": {"value": 0, "alt_names": ["TongueOut"]},
        "TongueOut1": {"value": 0, "alt_names": ["TongueOut1"]},
        "TongueOut2": {"value": 0, "alt_names": ["TongueOut2"]},
        "TongueOut4": {"value": 0, "alt_names": ["TongueOut4"]},
        "TongueOut8": {"value": 0, "alt_names": ["TongueOut8"]},
        
        # Cheek parameters
        "cheekPuff": {"value": 0, "alt_names": ["CheekPuff", "CheekBlow"]},
        "cheekSquintLeft": {"value": 0, "alt_names": ["CheekSquintLeft", "LeftCheekSquint"]},
        "cheekSquintRight": {"value": 0, "alt_names": ["CheekSquintRight", "RightCheekSquint"]},
        "cheekPuffSuckLeft1": {"value": 0, "alt_names": ["CheekPuffSuckLeft1"]},
        "cheekPuffSuckRight1": {"value": 0, "alt_names": ["CheekPuffSuckRight1"]},
        "CheekPuffSuckLeft2": {"value": 0, "alt_names": ["CheekPuffSuckLeft2"]},
        "CheekPuffSuckRight2": {"value": 0, "alt_names": ["CheekPuffSuckRight2"]},
        "CheekPuffSuckLeft4": {"value": 0, "alt_names": ["CheekPuffSuckLeft4"]},
        "CheekPuffSuckRight4": {"value": 0, "alt_names": ["CheekPuffSuckRight4"]},
        "CheekSquint1": {"value": 0, "alt_names": ["CheekSquint1"]},
        "CheekSquint2": {"value": 0, "alt_names": ["CheekSquint2"]},
        "CheekSquint4": {"value": 0, "alt_names": ["CheekSquint4"]},

        # Smile/Sad parameters with intensity levels
        "SmileSadLeft1": {"value": 0, "alt_names": ["SmileSadLeft1"]},
        "SmileSadRight1": {"value": 0, "alt_names": ["SmileSadRight1"]},
        "SmileSadLeft2": {"value": 0, "alt_names": ["SmileSadLeft2"]},
        "SmileSadRight2": {"value": 0, "alt_names": ["SmileSadRight2"]},
        "SmileSadLeft4": {"value": 0, "alt_names": ["SmileSadLeft4"]},
        "SmileSadRight4": {"value": 0, "alt_names": ["SmileSadRight4"]},
        "SmileSadLeft8": {"value": 0, "alt_names": ["SmileSadLeft8"]},
        "SmileSadRight8": {"value": 0, "alt_names": ["SmileSadRight8"]},
        "SmileSadLeftNegative": {"value": 0, "alt_names": ["SmileSadLeftNegative"]},
        "SmileSadRightNegative": {"value": 0, "alt_names": ["SmileSadRightNegative"]},
        
        # Smile/Frown parameters
        "SmileFrownLeft1": {"value": 0, "alt_names": ["SmileFrownLeft1"]},
        "SmileFrownRight1": {"value": 0, "alt_names": ["SmileFrownRight1"]},
        "SmileFrownLeft2": {"value": 0, "alt_names": ["SmileFrownLeft2"]},
        "SmileFrownRight2": {"value": 0, "alt_names": ["SmileFrownRight2"]},
        "SmileFrownLeft4": {"value": 0, "alt_names": ["SmileFrownLeft4"]},
        "SmileFrownRight4": {"value": 0, "alt_names": ["SmileFrownRight4"]},
        "SmileFrownLeft8": {"value": 0, "alt_names": ["SmileFrownLeft8"]},
        "SmileFrownRight8": {"value": 0, "alt_names": ["SmileFrownRight8"]},
        
        # Nose parameters
        "noseSneerLeft": {"value": 0, "alt_names": ["NoseSneerLeft", "LeftNoseSneer", "NoseWrinkleLeft"]},
        "noseSneerRight": {"value": 0, "alt_names": ["NoseSneerRight", "RightNoseSneer", "NoseWrinkleRight"]},
        "noseSneer1": {"value": 0, "alt_names": ["NoseSneer1"]},
        "noseSneer2": {"value": 0, "alt_names": ["NoseSneer2"]},
        "NoseSneer4": {"value": 0, "alt_names": ["NoseSneer4"]},
        "NoseSneerLeft1": {"value": 0, "alt_names": ["NoseSneerLeft1"]},
        "NoseSneerRight1": {"value": 0, "alt_names": ["NoseSneerRight1"]},
        "NoseSneerLeft2": {"value": 0, "alt_names": ["NoseSneerLeft2"]},
        "NoseSneerRight2": {"value": 0, "alt_names": ["NoseSneerRight2"]},
        "NoseSneerLeft4": {"value": 0, "alt_names": ["NoseSneerLeft4"]},
        "NoseSneerRight4": {"value": 0, "alt_names": ["NoseSneerRight4"]}
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