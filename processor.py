from sender import send_hue_shift
import math
from collections import deque
import time
import datetime

def process_data(queue, debug_level=2, throttle_ms=500):  # Increased default debug level
    """
    Process facial data with configurable debugging and throttling
    
    Args:
        queue: The queue containing facial tracking data
        debug_level: 0=minimal, 1=normal, 2=verbose debugging
        throttle_ms: Minimum milliseconds between hue updates
    """
    # Initialize parameters dictionary
    facial_params = {
        # Basic eye parameters
        "eyeBlinkLeft": 0,
        "eyeBlinkRight": 0,
        "eyeOpenLeft": 0,
        "eyeOpenRight": 0,
        "eyeSquintLeft": 0,
        "eyeSquintRight": 0,
        
        # Eyebrow parameters
        "browDownLeft": 0,
        "browDownRight": 0,
        "browUpLeft": 0,
        "browUpRight": 0,
        
        # Mouth parameters
        "mouthOpen": 0,
        "jawOpen": 0,
        "mouthSmile": 0,
        "mouthFrown": 0,
        "mouthPucker": 0,
        "mouthShrugUpper": 0,
        "mouthShrugLower": 0,
        
        # Cheek parameters
        "cheekPuff": 0,
        "cheekSquintLeft": 0,
        "cheekSquintRight": 0,
        
        # Nose parameters
        "noseSneerLeft": 0,
        "noseSneerRight": 0
    }
    
    # Create a rolling window for smoothing output
    window_size = 10
    value_history = deque(maxlen=window_size)
    # Initialize with zeros to prevent empty calculation
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
    osc_message_counter = 0
    recognized_params_counter = 0
    
    def debug_print(level, message):
        """Print message only if debug level is sufficient"""
        if debug_level >= level:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {message}")
    
    debug_print(0, "=== STARTING PROCESSOR WITH TROUBLESHOOTING MODE ===")
    debug_print(0, f"Debug level: {debug_level}, Throttle: {throttle_ms}ms")
    debug_print(0, "Waiting for OSC messages...")
    
    while True:
        try:
            address, value = queue.get(timeout=5)  # 5 second timeout for diagnostics
            osc_message_counter += 1
            
            # Always print every OSC message in troubleshooting mode
            debug_print(1, f"OSC #{osc_message_counter}: {address} -> {value}")
            
            # Extract parameter name from address and handle potential format variations
            parts = address.split('/')
            param_name = parts[-1]  # Get the last part after splitting
            
            # Log full path breakdown for troubleshooting
            debug_print(2, f"Address parts: {parts}")
            debug_print(2, f"Extracted param: {param_name}")
            
            # Check if this is a parameter we recognize
            if param_name in facial_params:
                facial_params[param_name] = value
                recognized_params_counter += 1
                debug_print(1, f"✓ Recognized param #{recognized_params_counter}: {param_name} = {value:.3f}")
            else:
                debug_print(1, f"✗ Unrecognized param: {param_name}")
                # Attempt substring matching for more flexible parameter recognition
                matched = False
                for known_param in facial_params.keys():
                    if known_param.lower() in param_name.lower():
                        debug_print(1, f"  → Possible match with {known_param}?")
                        matched = True
                if not matched:
                    debug_print(1, f"  → No matches found. Consider adding this parameter.")
            
            # Only process and send updates at the throttled rate
            current_time = time.time()
            time_diff_ms = (current_time - last_update_time) * 1000
            
            if time_diff_ms >= throttle_ms:
                update_counter += 1
                debug_print(0, f"\n=== PROCESSING UPDATE #{update_counter} ===")
                debug_print(0, f"Received {osc_message_counter} OSC messages, {recognized_params_counter} recognized")
                
                # Show all non-zero parameters
                active_params = [p for p, v in facial_params.items() if v > 0.01]
                debug_print(0, f"Active parameters ({len(active_params)}): {', '.join(active_params)}")
                
                # Calculate which emotion parameters are present
                debug_print(0, "Checking emotion parameters:")
                for emotion, weights in emotion_weights.items():
                    present_params = [p for p in weights.keys() if facial_params.get(p, 0) > 0.01]
                    debug_print(0, f"  {emotion}: {len(present_params)}/{len(weights)} parameters present")
                    if present_params:
                        debug_print(1, f"    Present: {', '.join(present_params)}")
                    missing_params = [p for p in weights.keys() if facial_params.get(p, 0) <= 0.01]
                    if missing_params:
                        debug_print(1, f"    Missing: {', '.join(missing_params)}")
                
                # Calculate emotion scores
                emotion_scores = {}
                for emotion, weights in emotion_weights.items():
                    score = 0
                    for param, weight in weights.items():
                        param_value = facial_params.get(param, 0)
                        contribution = param_value * weight
                        score += contribution
                        if param_value > 0.01:
                            debug_print(2, f"  {emotion} += {param} ({param_value:.2f}) * {weight} = {contribution:.3f}")
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
                        emotion_contribution = emotion_hues[emotion] * score
                        hue += emotion_contribution
                        debug_print(2, f"Hue += {emotion} ({score:.3f}) * {emotion_hues[emotion]} = {emotion_contribution:.3f}")
                
                # Normalize in case scores add up to more than 1
                total_score = sum(emotion_scores.values())
                if total_score > 0:
                    hue = hue / total_score
                
                # Add value to rolling window
                value_history.append(hue)
                
                # Calculate smoothed value
                smoothed_hue = sum(value_history) / len(value_history)
                
                # Log the emotion detection results
                debug_print(0, "Emotion Scores:")
                for emotion, score in sorted(emotion_scores.items(), key=lambda x: -x[1]):
                    debug_print(0, f"  {emotion}: {score:.3f}")
                
                debug_print(0, f"Dominant: {dominant_emotion} ({dominant_score:.2f})")
                debug_print(0, f"Raw Hue: {hue:.3f}, Smoothed Hue: {smoothed_hue:.3f}")
                
                # Send smoothed hue value
                debug_print(0, f"Sending HueShift: {smoothed_hue:.3f}")
                send_hue_shift(smoothed_hue)
                
                # Update the last update time
                last_update_time = current_time
                
                # Insert a divider for readability
                debug_print(0, "=" * 50)
        
        except Exception as e:
            debug_print(0, f"ERROR: {str(e)}")
            # If queue.get times out, print a diagnostic message
            if "Empty" in str(e):
                debug_print(0, "No OSC messages received in the last 5 seconds")
                debug_print(0, "Possible issues:")
                debug_print(0, "1. VRCFT is not sending data to the correct port")
                debug_print(0, "2. Listener process is not receiving or forwarding OSC messages")
                debug_print(0, "3. OSC address format is different than expected")
                debug_print(0, f"Total messages received so far: {osc_message_counter}")
            time.sleep(1)  # Prevent rapid error logging