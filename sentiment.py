import numpy as np
import logging

EMOTION_WEIGHTS = {
    "happy": {
        "mouthSmile": 0.6,
        "eyeLidLeft": -0.4,  # Negative weight for open eyes
        "eyeLidRight": -0.4,
    },
    "sad": {
        "mouthClosed": 0.5,
        "eyeLidLeft": 0.3,   # Positive weight for closed eyes
        "eyeLidRight": 0.3,
    },
    "angry": {
        "EyeSquintLeft1": 0.4,
        "EyeSquintRight1": 0.4,
        "mouthPucker": 0.3,
    },
    "surprised": {
        "jawOpen": 0.6,
        "eyeLidLeft": -0.2,  # Open eyes
        "eyeLidRight": -0.2,
    }
}

# Color mapping for emotions (hue float values from 0-1)
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
    Calculate emotion scores with enhanced parameter handling
    """
    logger = logging.getLogger(__name__)
    
    # Log all current values for debugging
    logger.debug("Current facial parameter values:")
    for param, value in current_values.items():
        logger.debug(f"  {param}: {value}")
    
    # Calculate emotion scores
    emotion_scores = {}
    detailed_scores = {}
    
    for emotion, weights in EMOTION_WEIGHTS.items():
        score = 0
        emotion_breakdown = {}
        
        for param, weight in weights.items():
            # Try direct match, then try case-insensitive match
            param_value = current_values.get(param, 
                next((current_values.get(k, 0) for k in current_values.keys() if k.lower() == param.lower()), 0)
            )
            
            # Normalize input values
            param_value = max(0, min(1, param_value))
            
            # Calculate contribution with special handling for negative weights
            if weight > 0:
                param_contribution = param_value * weight
            else:
                # For negative weights, invert the value
                param_contribution = (1 - param_value) * abs(weight)
            
            emotion_breakdown[param] = param_contribution
            score += param_contribution
        
        # Clip total score
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
    
    # Extensive logging for debugging
    logger.info("Detailed Emotion Score Breakdown:")
    for emotion, score in emotion_scores.items():
        logger.info(f"  {emotion}: {score:.4f}")
        if emotion in detailed_scores:
            for param, contrib in detailed_scores[emotion].items():
                logger.info(f"    {param}: {contrib:.4f}")
    
    return emotion_scores, dominant_emotion, dominant_score

def calculate_emotion_hue(emotion_scores):
    """
    Calculate hue with precise emotion blending and logging
    
    Args:
        emotion_scores (dict): Dictionary of emotion scores
    
    Returns:
        float: Calculated hue value
    """
    logger = logging.getLogger(__name__)
    
    # Calculate hue with precise blending
    hue = 0
    total_weighted_score = 0
    
    # Log individual emotion contributions
    logger.info("Hue Calculation Breakdown:")
    
    for emotion, score in emotion_scores.items():
        if score > 0 and emotion in EMOTION_HUES:
            # Exponential weighting to emphasize dominant emotions
            weighted_score = score ** 2
            emotion_hue = EMOTION_HUES[emotion]
            
            logger.info(f"  {emotion}: score={score:.4f}, hue={emotion_hue:.4f}, weighted_score={weighted_score:.4f}")
            
            hue += emotion_hue * weighted_score
            total_weighted_score += weighted_score
    
    # Normalize hue
    if total_weighted_score > 0:
        hue = hue / total_weighted_score
    
    # Ensure hue is within 0-1 range
    hue = max(0, min(1, hue))
    
    logger.info(f"Final Calculated Hue: {hue:.4f}")
    
    return hue

def map_hue_to_color_description(hue_value):
    """
    Map a hue value to its closest color description
    
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