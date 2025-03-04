import numpy as np
import logging

# Emotion weight mappings
EMOTION_WEIGHTS = {
    "happy": {
        "mouthSmile": 1.0,
        "eyeOpenLeft": 0.4,
        "eyeOpenRight": 0.4,
        "browUpLeft": 0.3,
        "browUpRight": 0.3,
    },
    "sad": {
        "mouthFrown": 1.0,
        "browDownLeft": 0.5,
        "browDownRight": 0.5,
        "eyeSquintLeft": 0.3,
        "eyeSquintRight": 0.3,
    },
    "angry": {
        "browDownLeft": 0.8,
        "browDownRight": 0.8,
        "noseSneerLeft": 0.5,
        "noseSneerRight": 0.5,
        "mouthFrown": 0.4,
    },
    "surprised": {
        "eyeOpenLeft": 0.6,
        "eyeOpenRight": 0.6,
        "browUpLeft": 0.4,
        "browUpRight": 0.4,
        "mouthOpen": 0.5,
        "jawOpen": 0.5,
    }
}

# Color mapping for emotions (hue values from 0-1)
EMOTION_HUES = {
    "happy": 0.19,      # Yellow
    "sad": 0.58,        # Ocean blue
    "angry": 0.94,      # Red (high end)
    "surprised": 0.28,  # Green
    "neutral": 0.02,    # Red (low end)
    "calm": 0.45,       # Cyan
    "excited": 0.85,    # Electric pink
    "scared": 0.69      # Purple
}

def map_emotion_to_color_description(hue_value):
    """
    Map a hue value to its color description.
    
    Args:
        hue_value (float): Hue value between 0 and 1
    
    Returns:
        str: Closest color description
    """
    color_ranges = [
        (0.00, 0.02, "Red (low)"),
        (0.19, 0.19, "Yellow"),
        (0.28, 0.28, "Green"),
        (0.45, 0.45, "Cyan"),
        (0.58, 0.58, "Ocean Blue"),
        (0.69, 0.69, "Purple"),
        (0.75, 0.75, "Dark Pink"),
        (0.85, 0.85, "Electric Pink"),
        (0.94, 1.00, "Red (high)")
    ]
    
    # Find the closest color range
    closest_color = min(color_ranges, key=lambda x: abs(x[0] - hue_value))
    return closest_color[2]

def calculate_emotion_scores(current_values):
    """
    Calculate emotion scores with more aggressive and dynamic scoring.
    
    Args:
        current_values (dict): Dictionary of current facial parameter values
    
    Returns:
        tuple: (emotion_scores, dominant_emotion, dominant_score)
    """
    # Calculate emotion scores with exponential scaling
    emotion_scores = {}
    for emotion, weights in EMOTION_WEIGHTS.items():
        score = 0
        for param, weight in weights.items():
            param_value = current_values.get(param, 0)
            # Use exponential scaling to emphasize strong expressions
            score += (param_value ** 3) * weight
        
        # Ensure score is between 0 and 1
        emotion_scores[emotion] = min(1, max(0, score))
    
    # Normalize scores
    total_score = sum(emotion_scores.values())
    if total_score > 0:
        emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
    
    # Calculate neutral score
    emotion_scores["neutral"] = max(0, 1 - sum(emotion_scores.values()))
    
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

def smooth_value(value_history, new_value, smoothing_method='simple_average'):
    """
    Smooth a new value using various methods.
    
    Args:
        value_history (deque): Deque of previous values
        new_value (float): New value to add
        smoothing_method (str): Method of smoothing to apply
    
    Returns:
        float: Smoothed value
    """
    value_history.append(new_value)
    
    if smoothing_method == 'simple_average':
        return sum(value_history) / len(value_history)
    
    elif smoothing_method == 'weighted_average':
        # Example of a weighted average where recent values have more impact
        weights = [i+1 for i in range(len(value_history))]
        weighted_sum = sum(val * weight for val, weight in zip(value_history, weights))
        return weighted_sum / sum(weights)
    
    elif smoothing_method == 'exponential_smoothing':
        # Simple exponential smoothing with a fixed alpha
        alpha = 0.3
        smoothed = value_history[0]
        for val in value_history[1:]:
            smoothed = alpha * val + (1 - alpha) * smoothed
        return smoothed
    
    else:
        raise ValueError(f"Unknown smoothing method: {smoothing_method}")