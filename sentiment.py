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
    Enhanced emotion score calculation with improved neutral handling.
    
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
            # More aggressive parameter matching
            param_value = 0
            for key in current_values.keys():
                if param.lower() in key.lower():
                    param_value = current_values[key]
                    break
            
            # Normalize input values
            param_value = max(0, min(1, param_value))
            
            # Calculate contribution
            param_contribution = (param_value if weight > 0 else (1 - param_value)) * abs(weight)
            
            emotion_breakdown[param] = param_contribution
            score += param_contribution
        
        # Clip and store emotion scores
        emotion_scores[emotion] = max(0, min(1, score))
        detailed_scores[emotion] = emotion_breakdown
    
    # Normalize scores with a dynamic neutral calculation
    total_score = sum(emotion_scores.values())
    if total_score > 0:
        emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
        
        # Dynamic neutral calculation based on emotional intensity
        neutral_factor = 1 - sum(emotion_scores.values())
        emotion_scores["neutral"] = max(0, neutral_factor)
    
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
    Calculate hue with improved emotion representation and dynamic range.
    
    Args:
        emotion_scores (dict): Dictionary of emotion scores
    
    Returns:
        float: Calculated hue value
    """
    logger = logging.getLogger(__name__)
    
    # Filter out neutral and extract top emotions
    emotion_weights = {k: v for k, v in emotion_scores.items() 
                       if k != 'neutral' and v > 0}
    
    # If no significant emotions, return neutral hue
    if not emotion_weights:
        return EMOTION_HUES['neutral']
    
    # Sort emotions by score in descending order
    sorted_emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)
    
    logger.info("Top Emotions Breakdown:")
    
    # Primary and secondary emotion calculation
    primary_emotion, primary_score = sorted_emotions[0]
    secondary_emotion = sorted_emotions[1][0] if len(sorted_emotions) > 1 else primary_emotion
    
    # Calculate blended hue with bias towards extreme emotions
    primary_hue = EMOTION_HUES[primary_emotion]
    secondary_hue = EMOTION_HUES[secondary_emotion]
    
    # Exponential scoring to emphasize dominant emotions
    primary_weight = primary_score ** 3  # Cubic to really emphasize the top emotion
    secondary_weight = (1 - primary_score) ** 2
    
    # Blend hues with weighted average
    blended_hue = (primary_hue * primary_weight + secondary_hue * secondary_weight) / (primary_weight + secondary_weight)
    
    # Adjust for extreme emotions
    if primary_score > 0.7:  # If dominant emotion is very strong
        if primary_emotion in ['angry', 'excited']:
            blended_hue = EMOTION_HUES[primary_emotion]
        elif primary_emotion in ['surprised', 'happy']:
            blended_hue = EMOTION_HUES[primary_emotion]
    
    # Ensure hue is within 0-1 range
    blended_hue = max(0, min(1, blended_hue))
    
    logger.info(f"Primary Emotion: {primary_emotion} (score: {primary_score:.4f})")
    logger.info(f"Secondary Emotion: {secondary_emotion}")
    logger.info(f"Calculated Hue: {blended_hue:.4f}")
    logger.info(f"Color Description: {map_hue_to_color_description(blended_hue)}")
    
    return blended_hue

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