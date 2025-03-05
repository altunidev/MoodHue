import numpy as np
import logging
#from collections import deque
from config import EMOTION_HUES, EMOTION_WEIGHTS, COLOR_RANGES
def calculate_emotion_scores(current_values):
    """
    Calculate emotion scores with advanced parameter matching and scoring.
    
    Args:
        current_values (dict): Dictionary of current facial parameter values
    
    Returns:
        tuple: Emotion scores, dominant emotion, and dominant score
    """
    logger = logging.getLogger(__name__)
    
    # EXTENSIVE LOGGING
    logger.setLevel(logging.DEBUG)
    
    logger.debug("Raw Input Facial Parameters:")
    for key, value in current_values.items():
        logger.debug(f"  Raw Key: {key}, Raw Value: {value}")
    
    # CASE-INSENSITIVE PARAMETER CONVERSION
    normalized_values = {
        k.lower().replace(' ', ''): (v, k) 
        for k, v in current_values.items()
    }
    
    logger.debug("Normalized Input Parameters:")
    for key, (value, original_key) in normalized_values.items():
        logger.debug(f"  Normalized Key: {key}, Original Key: {original_key}, Value: {value}")
    
    emotion_scores = {}
    detailed_scores = {}
    
    for emotion, weights in EMOTION_WEIGHTS.items():
        if emotion == "neutral":
            continue  # Skip explicit neutral computation
        
        score = 0
        emotion_breakdown = {}
        
        logger.debug(f"\n=== Processing {emotion} emotion ===")
        
        for param, weight in weights.items():
            # MORE FLEXIBLE PARAMETER MATCHING
            normalized_param = param.lower().replace(' ', '')
            
            # Try multiple matching strategies
            matching_strategies = [
                normalized_param,  # Exact normalized match
                normalized_param.replace('1', ''),  # Remove numeric suffixes
                normalized_param.replace('left', '').replace('right', '')  # Remove directional indicators
            ]
            
            matched_value = None
            matched_strategy = None
            
            for strategy in matching_strategies:
                if strategy in normalized_values:
                    matched_value = normalized_values[strategy][0]
                    matched_strategy = strategy
                    break
            
            # Safe type conversion and parameter matching logging
            try:
                param_value = float(matched_value) if matched_value is not None else 0
                logger.debug(f"  Param: {param}")
                logger.debug(f"    Weight: {weight}")
                logger.debug(f"    Matched Strategy: {matched_strategy}")
                logger.debug(f"    Matched Value: {param_value}")
            except (TypeError, ValueError):
                logger.warning(f"Invalid value for {param}: {matched_value}. Using 0.")
                param_value = 0
            
            # Normalize input values
            param_value = max(0, min(1, param_value))
            
            # Contribution calculation with nuanced weight handling
            param_contribution = (
                param_value * weight if weight > 0 
                else (1 - param_value) * abs(weight)
            )
            
            logger.debug(f"    Contribution: {param_contribution}")
            
            emotion_breakdown[param] = param_contribution
            score += param_contribution
        
        # Clip and store emotion scores
        emotion_scores[emotion] = max(0, min(1, score))
        detailed_scores[emotion] = emotion_breakdown
    
    # More robust score normalization
    total_score = sum(emotion_scores.values())
    logger.debug(f"\nBefore Normalization Scores: {emotion_scores}")
    logger.debug(f"Total Score: {total_score}")
    
    if total_score > 0:
        # Scale all emotions
        emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
    
    # More sophisticated neutral calculation
    neutral_factor = max(0, 1 - sum(emotion_scores.values()))
    
    # Only add neutral if it's significantly present
    if neutral_factor > 0.1:
        emotion_scores["neutral"] = neutral_factor
    
    # Dominant emotion detection
    if emotion_scores:
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        dominant_score = emotion_scores[dominant_emotion]
    else:
        dominant_emotion = "neutral"
        dominant_score = 1.0
    
    # Comprehensive result logging
    logger.info("\n=== Final Emotion Scores ===")
    for emotion, score in emotion_scores.items():
        logger.info(f"  {emotion}: {score:.4f}")
        if emotion in detailed_scores:
            for param, contrib in detailed_scores[emotion].items():
                logger.info(f"    {param}: {contrib:.4f}")
    
    return emotion_scores, dominant_emotion, dominant_score

# Recommended function for precise parameter matching
def find_matching_parameter(target_param, current_values, logger=None):
    """
    Enhanced parameter matching with multiple strategies.
    """
    normalized_target = target_param.lower().replace(' ', '')
    
    # Normalize input dictionary
    normalized_dict = {
        k.lower().replace(' ', ''): v 
        for k, v in current_values.items()
    }
    
    # Matching strategies
    strategies = [
        normalized_target,  # Exact match
        normalized_target.replace('1', ''),  # Remove numeric suffixes
        normalized_target.replace('left', '').replace('right', '')  # Remove directional indicators
    ]
    
    for strategy in strategies:
        if strategy in normalized_dict:
            return normalized_dict[strategy]
    
    return 0  # Default if no match found


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