import numpy as np

# Emotion weight mappings
EMOTION_WEIGHTS = {
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
EMOTION_HUES = {
    "happy": 0.12,     # Yellow
    "sad": 0.65,       # Blue
    "angry": 0.95,     # Red
    "surprised": 0.3,  # Green
    "neutral": 0.0     # Red (baseline)
}

def calculate_emotion_scores(current_values):
    """
    Calculate emotion scores based on facial parameter values.
    
    Args:
        current_values (dict): Dictionary of current facial parameter values
    
    Returns:
        tuple: (emotion_scores, dominant_emotion, dominant_score)
    """
    # Calculate emotion scores
    emotion_scores = {}
    for emotion, weights in EMOTION_WEIGHTS.items():
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
    
    return emotion_scores, dominant_emotion, dominant_score

def calculate_emotion_hue(emotion_scores):
    """
    Calculate hue based on emotion blend.
    
    Args:
        emotion_scores (dict): Dictionary of emotion scores
    
    Returns:
        float: Calculated hue value
    """
    # Calculate hue based on emotion blend
    hue = 0
    for emotion, score in emotion_scores.items():
        if score > 0:
            hue += EMOTION_HUES[emotion] * score
    
    # Normalize in case scores add up to more than 1
    total_score = sum(emotion_scores.values())
    if total_score > 0:
        hue = hue / total_score
    
    return hue

def smooth_value(value_history, new_value):
    """
    Add new value to history and return smoothed average.
    
    Args:
        value_history (deque): Deque of previous values
        new_value (float): New value to add
    
    Returns:
        float: Smoothed average value
    """
    value_history.append(new_value)
    return sum(value_history) / len(value_history)