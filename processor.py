from sender import send_hue_shift
import math
from collections import deque

def process_data(queue):
    # Initialize parameters with default values
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
    
    # Create a rolling window for smoothing output (prevents flickering)
    window_size = 10
    value_history = deque(maxlen=window_size)
    
    # Emotion weight mappings (these values can be adjusted based on observation)
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
        },
        "neutral": {
            # Neutral is calculated based on the absence of other emotions
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
    
    while True:
        address, value = queue.get()  # Get data from the queue
        # Strip the prefix to get the parameter name
        param_name = address.split('/')[-1]
        
        # Update the parameter in our dictionary if it exists
        if param_name in facial_params:
            facial_params[param_name] = value
            print(f"Updated {param_name}: {value}")
        
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
        # This creates a weighted average of the emotions
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
        print(f"Emotion Scores: {emotion_scores}")
        print(f"Dominant Emotion: {dominant_emotion} ({dominant_score:.2f})")
        print(f"Calculated Hue: {hue:.2f}, Smoothed Hue: {smoothed_hue:.2f}")
        
        # Send smoothed hue value
        send_hue_shift(smoothed_hue)
