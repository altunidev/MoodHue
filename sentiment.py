import numpy as np
import logging
from collections import deque
from config import EMOTION_HUES, EMOTION_WEIGHTS, COLOR_RANGES

def find_matching_parameter(target_param, current_values, logger=None):
    """
    Find a matching parameter key with flexible matching.
    
    Args:
        target_param (str): The parameter to find
        current_values (dict): Dictionary of current parameter values
        logger (logging.Logger, optional): Logger for warnings
    
    Returns:
        float: Matched parameter value or 0
    """
    # Default to root logger if no logger provided
    if logger is None:
        logger = logging.getLogger(__name__)
    
    # Direct exact match
    if target_param in current_values:
        return current_values[target_param]
    
    # Case-insensitive match
    case_insensitive = {k.lower(): k for k in current_values.keys()}
    if target_param.lower() in case_insensitive:
        return current_values[case_insensitive[target_param.lower()]]
    
    # Partial match with more sophisticated logic
    matches = [
        (k, v) for k, v in current_values.items() 
        if target_param.lower() in k.lower() or k.lower() in target_param.lower()
    ]
    
    if matches:
        # Prefer exact word matches over partial
        exact_word_matches = [
            (k, v) for k, v in matches 
            if any(word.lower() == target_param.lower() for word in k.split())
        ]
        
        if exact_word_matches:
            matches = exact_word_matches
        
        # If multiple matches, log all and use the first
        if len(matches) > 1:
            logger.warning(f"Multiple matches for {target_param}: {matches}")
        
        return matches[0][1]
    
    return 0  # Default to 0 if no match

def calculate_emotion_scores(current_values):
    """
    Calculate emotion scores with advanced parameter matching and scoring.
    
    Args:
        current_values (dict): Dictionary of current facial parameter values
    
    Returns:
        tuple: Emotion scores, dominant emotion, and dominant score
    """
    logger = logging.getLogger(__name__)
    
    # Log input values
    logger.debug("Input Facial Parameters:")
    for key, value in current_values.items():
        logger.debug(f"  {key}: {value}")
    
    emotion_scores = {}
    detailed_scores = {}
    
    for emotion, weights in EMOTION_WEIGHTS.items():
        score = 0
        emotion_breakdown = {}
        
        logger.debug(f"\nProcessing {emotion} emotion:")
        
        for param, weight in weights.items():
            # Flexible parameter matching
            param_value = find_matching_parameter(param, current_values, logger)
            
            # Safe type conversion
            try:
                param_value = float(param_value)
            except (TypeError, ValueError):
                logger.warning(f"Invalid value for {param}: {param_value}. Using 0.")
                param_value = 0
            
            # Normalize input values
            param_value = max(0, min(1, param_value))
            
            # Contribution calculation with nuanced weight handling
            param_contribution = (
                param_value * weight if weight > 0 
                else (1 - param_value) * abs(weight)
            )
            
            logger.debug(f"  {param}: value={param_value}, weight={weight}, contribution={param_contribution}")
            
            emotion_breakdown[param] = param_contribution
            score += param_contribution
        
        # Clip and store emotion scores
        emotion_scores[emotion] = max(0, min(1, score))
        detailed_scores[emotion] = emotion_breakdown
    
    # Advanced score normalization
    total_score = sum(emotion_scores.values())
    if total_score > 0:
        emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
    
    # Dynamic neutral calculation with intensity-based adjustment
    neutral_factor = max(0, 1 - sum(emotion_scores.values()))
    emotion_scores["neutral"] = neutral_factor
    
    # Dominant emotion detection
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    dominant_score = emotion_scores[dominant_emotion]
    
    # Comprehensive result logging
    logger.info("\nFinal Emotion Scores:")
    for emotion, score in emotion_scores.items():
        logger.info(f"  {emotion}: {score:.4f}")
        if emotion in detailed_scores:
            for param, contrib in detailed_scores[emotion].items():
                logger.info(f"    {param}: {contrib:.4f}")
    
    return emotion_scores, dominant_emotion, dominant_score


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


# You can keep other utility functions like smooth_value, etc. from the original code
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
        weights = [i+1 for i in range(len(value_history))]
        weighted_sum = sum(val * weight for val, weight in zip(value_history, weights))
        return weighted_sum / sum(weights)
    
    elif smoothing_method == 'exponential_smoothing':
        alpha = 0.3
        smoothed = value_history[0]
        for val in value_history[1:]:
            smoothed = alpha * val + (1 - alpha) * smoothed
        return smoothed
    
    else:
        raise ValueError(f"Unknown smoothing method: {smoothing_method}")