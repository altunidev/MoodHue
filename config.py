# config.py
from typing import Dict, Any

OSC_CONFIG = {
    'IP': '127.0.0.1',
    'LISTEN_PORT': 9002,
    'SEND_PORT': 9000,
}

LOGGING_CONFIG = {
    'DEFAULT_DEBUG_LEVEL': 1,
    'DEFAULT_THROTTLE_MS': 1000,
    'LOG_FORMAT': '%(asctime)s.%(msecs)03d | %(levelname)8s | %(message)s',
    'LOG_DATEFORMAT': '%H:%M:%S'
}

# Centralize all global constants from sentiment.py and processor.py
EMOTION_WEIGHTS: Dict[str, Dict[str, float]] = {
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

PROCESSING_CONFIG = {
    'SMOOTHING_WINDOW_SIZE': 10,
    'SMOOTHING_METHOD': 'simple_average'
}