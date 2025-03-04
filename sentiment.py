import numpy as np
import logging
from collections import deque

# Common color ranges extracted to a single location
COLOR_RANGES = [
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

EMOTION_WEIGHTS = {
    "happy": {
        "mouthSmile": 0.6,
        "eyeLidLeft": -0.4,
        "eyeLidRight": -0.4,
    },
    "sad": {
        "mouthClosed": 0.5,
        "eyeLidLeft": 0.3,
        "eyeLidRight": 0.3,
    },
    "angry": {
        "EyeSquintLeft1": 0.4,
        "EyeSquintRight1": 0.4,
        "mouthPucker": 0.3,
    },
    "surprised": {
        "jawOpen": 0.6,
        "eyeLidLeft": -0.2,
        "eyeLidRight": -0.2,
    }
}

EMOTION_HUES = {
    "happy": 0.19,
    "sad": 0.58,
    "angry": 0.94,
    "surprised": 0.28,
    "neutral": 0.02,
    "calm": 0.45,
    "excited": 0.85,
    "scared": 0.69
}

def map_hue_to_color_description(hue_value):
    """
    Map a hue value to its closest color description.
    
    Args:
        hue_value (float): Hue value between 0 and 1
    
    Returns:
        str: Closest color description
    """
    # Find the closest color range using the global COLOR_RANGES
    closest_color = min(COLOR_RANGES, key=lambda x: abs(x[0] - hue_value))
    return closest_color[2]

def calculate_emotion_scores(current_values):
    """
    Calculate emotion scores with simplified parameter handling.
    
    Args:
        current_values (dict): Dictionary of current facial parameter values
    
    Returns:
        tuple: Emotion scores, dominant emotion, and dominant score
    """
    logger = logging.getLogger(__name__)
    
    # Simplified logging of input values
    logger.debug("Current facial parameter values: %s", current_values)
    
    emotion_scores = {}
    detailed_scores = {}
    
    for emotion, weights in EMOTION_WEIGHTS.items():
        score = 0
        emotion_breakdown = {}
        
        for param, weight in weights.items():
            # Simplified parameter lookup (case-sensitive)
            param_value = current_values.get(param, 0)
            
            # Normalize input values
            param_value = max(0, min(1, param_value))
            
            # Calculate contribution
            param_contribution = (param_value if weight > 0 else (1 - param_value)) * abs(weight)
            
            emotion_breakdown[param] = param_contribution
            score += param_contribution
        
        # Clip and store emotion scores
        emotion_scores[emotion] = max(0, min(1, score))
        detailed_scores[emotion] = emotion_breakdown
    
    # Normalize scores
    total_score = sum(emotion_scores.values())
    if total_score > 0:
        emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
    
    # Calculate neutral score
    emotion_scores["neutral"] = max(0, 1 - sum(emotion_scores.values()))
    
    # Find the dominant emotion
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    dominant_score = emotion_scores[dominant_emotion]
    
    # Logging of detailed emotion breakdown
    logger.info("Emotion Score Breakdown:")
    for emotion, score in emotion_scores.items():
        logger.info("  %s: %.4f", emotion, score)
        if emotion in detailed_scores:
            for param, contrib in detailed_scores[emotion].items():
                logger.info("    %s: %.4f", param, contrib)
    
    return emotion_scores, dominant_emotion, dominant_score

def calculate_emotion_hue(emotion_scores):
    """
    Calculate hue with emotion blending.
    
    Args:
        emotion_scores (dict): Dictionary of emotion scores
    
    Returns:
        float: Calculated hue value
    """
    logger = logging.getLogger(__name__)
    
    hue = 0
    total_weighted_score = 0
    
    logger.info("Hue Calculation Breakdown:")
    
    for emotion, score in emotion_scores.items():
        if score > 0 and emotion in EMOTION_HUES:
            # Exponential weighting to emphasize dominant emotions
            weighted_score = score ** 2
            emotion_hue = EMOTION_HUES[emotion]
            
            logger.info("  %s: score=%.4f, hue=%.4f, weighted_score=%.4f", 
                        emotion, score, emotion_hue, weighted_score)
            
            hue += emotion_hue * weighted_score
            total_weighted_score += weighted_score
    
    # Normalize hue
    hue = hue / total_weighted_score if total_weighted_score > 0 else 0
    
    # Ensure hue is within 0-1 range
    hue = max(0, min(1, hue))
    
    logger.info("Final Calculated Hue: %.4f", hue)
    
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
        # Weighted average where recent values have more impact
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