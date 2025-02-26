from sender import send_hue_shift
import math
from collections import deque
import time
import datetime

def process_data(queue, debug_level, throttle_ms):
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
    
    def debug_print(level, message):
        """Print message only if debug level is sufficient"""
        if debug_level >= level:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {message}")
    
    debug_print(0, "Starting processor with debug level " + str(debug_level) + 
                " and throttle rate " + str(throttle_ms) + "ms")
    
    while True:
        address, value = queue.get()  # Get data from the queue
        
        # Extract parameter name from address
        param_name = address.split('/')[-1]
        
        # Update parameter value if it exists in our dictionary
        if param_name in facial_params:
            facial_params[param_name] = value
            debug_print(2, f"Updated {param_name}: {value:.3f}")
        
        # Only process and send updates at the throttled rate
        current_time = time.time()
        time_diff_ms = (current_time - last_update_time) * 1000
        
        if time_diff_ms >= throttle_ms:
            update_counter += 1
            debug_print(1, f"--- Processing update #{update_counter} ---")
            
            # Log current facial parameters at verbose level
            if debug_level >= 2:
                debug_print(2, "Current facial parameters:")
                for param, val in facial_params.items():
                    if val > 0.05:  # Only show non-zero parameters to reduce noise
                        debug_print(2, f"  {param}: {val:.3f}")
            
            # Calculate emotion scores
            emotion_scores = {}
            for emotion, weights in emotion_weights.items():
                score = 0
                for param, weight in weights.items():
                    score += facial_params.get(param, 0) * weight
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
            
            # Log the emotion detection results
            debug_print(1, "Emotion Scores:")
            for emotion, score in emotion_scores.items():
                if score > 0.05:  # Only show non-trivial emotions
                    debug_print(1, f"  {emotion}: {score:.3f}")
            
            debug_print(0, f"Dominant: {dominant_emotion} ({dominant_score:.2f}) → Hue: {smoothed_hue:.3f}")
            
            # Send smoothed hue value
            send_hue_shift(smoothed_hue)
            
            # Update the last update time
            last_update_time = current_time
            
            # Insert a delay for readability if in high debug mode
            if debug_level >= 2:
                time.sleep(0.5)  # Half second pause to make logs more readable

# Example usage in main.py:
# process_data(queue, debug_level=1, throttle_ms=500)