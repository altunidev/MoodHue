# config.py
from typing import Dict, Any

OSC_CONFIG = {
    'IP': '127.0.0.1',
    'LISTEN_PORT': 9002,
    'SEND_PORT': 9000,
}

'''
DEBUG_LEVEL
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG
'''

LOGGING_CONFIG = {
    'DEBUG_LEVEL': 1,
    'DEFAULT_THROTTLE_MS': 1000,
    'LOG_FORMAT': '%(asctime)s.%(msecs)03d | %(levelname)8s | %(message)s',
    'LOG_DATEFORMAT': '%H:%M:%S'
}

# Centralize all global constants from sentiment.py and processor.py
EMOTION_WEIGHTS: Dict[str, Dict[str, float]] = {
    "neutral": {
        "default": 0.0,
        "mouthClosed": 0.2,  # Slightly neutral mouth position
        "eyeLidLeft": 0.1,   # Neutral eye state
        "eyeLidRight": 0.1
    },
    "happy": {
        "mouthSmile": 1.0,      # Strong positive for smiling
        "eyeLidLeft": -0.3,     # Slight negative for droopy eyes
        "eyeLidRight": -0.3,
    }
}
''',
    "sad": {
        "mouthClosed": -0.7,    # Strong negative for closed mouth
        "eyeLidLeft": 0.5,      # Strong positive for droopy eyes
        "eyeLidRight": 0.5,
    },
    "angry": {
        "EyeSquintLeft1": 0.6,  # Strong positive for squinted eyes
        "EyeSquintRight1": 0.6,
        "mouthPucker": 0.4,
    },
    "surprised": {
        "jawOpen": 0.8,          # Strong positive for open jaw
        "eyeLidLeft": -0.3,      # Slight negative for wide eyes
        "eyeLidRight": -0.3,
    }
}'''

EMOTION_HUES: Dict[str, float] = {
    "neutral": 0.00,    # Red (low end)
    "happy": 0.70,      # Not red
}

'''
EMOTION_HUES: Dict[str, float] = {
    "happy": 0.19,      # Yellow
    "sad": 0.58,        # Ocean blue
    "angry": 0.94,      # Red (high end)
    "surprised": 0.28,  # Green
    "neutral": 0.02,    # Red (low end)
    "calm": 0.45,       # Cyan
    "excited": 0.85,    # Electric pink
    "scared": 0.69      # Purple
}
'''

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

PROCESSING_CONFIG = {
    'SMOOTHING_WINDOW_SIZE': 10,
    'SMOOTHING_METHOD': 'simple_average'
}