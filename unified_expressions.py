"""
FACIAL_PARAMS = {
    # Base VRC Eye params
    "eyesClosedAmount": {"value": 0, "alt_names": ["EyesClosedAmount", "EyeClosed", "EyeClosureAmount"]},
    "centerPitchYaw": {"value": 0, "alt_names": ["CenterPitchYaw", "EyePitchYaw", "EyeTracking"]},

    # Eye Expression Parameters
    "eyeLidRight": {"value": 0, "alt_names": ["EyeLidRight", "RightEyeOpenness", "RightEyeWiden"]},
    "eyeLidLeft": {"value": 0, "alt_names": ["EyeLidLeft", "LeftEyeOpenness", "LeftEyeWiden"]},
    "eyeLid": {"value": 0, "alt_names": ["EyeLid", "EyesOpenness", "EyesWiden"]},
    "eyeSquintRight": {"value": 0, "alt_names": ["EyeSquintRight"]},
    "eyeSquintLeft": {"value": 0, "alt_names": ["EyeSquintLeft"]},
    "eyeSquint": {"value": 0, "alt_names": ["EyeSquint"]},
    "pupilDilation": {"value": 0, "alt_names": ["PupilDilation"]},
    "pupilDiameterRight": {"value": 0, "alt_names": ["PupilDiameterRight"]},
    "pupilDiameterLeft": {"value": 0, "alt_names": ["PupilDiameterLeft"]},
    "pupilDiameter": {"value": 0, "alt_names": ["PupilDiameter"]},

    # Brow Parameters
    "browPinchRight": {"value": 0, "alt_names": ["BrowPinchRight"]},
    "browPinchLeft": {"value": 0, "alt_names": ["BrowPinchLeft"]},
    "browLowererRight": {"value": 0, "alt_names": ["BrowLowererRight"]},
    "browLowererLeft": {"value": 0, "alt_names": ["BrowLowererLeft"]},
    "browInnerUpRight": {"value": 0, "alt_names": ["BrowInnerUpRight"]},
    "browInnerUpLeft": {"value": 0, "alt_names": ["BrowInnerUpLeft"]},
    "browOuterUpRight": {"value": 0, "alt_names": ["BrowOuterUpRight"]},
    "browOuterUpLeft": {"value": 0, "alt_names": ["BrowOuterUpLeft"]},

    # Nose Parameters
    "noseSneerRight": {"value": 0, "alt_names": ["NoseSneerRight"]},
    "noseSneerLeft": {"value": 0, "alt_names": ["NoseSneerLeft"]},
    "nasalDilationRight": {"value": 0, "alt_names": ["NasalDilationRight"]},
    "nasalDilationLeft": {"value": 0, "alt_names": ["NasalDilationLeft"]},
    "nasalConstrictRight": {"value": 0, "alt_names": ["NasalConstrictRight"]},
    "nasalConstrictLeft": {"value": 0, "alt_names": ["NasalConstrictLeft"]},

    # Cheek Parameters
    "cheekSquintRight": {"value": 0, "alt_names": ["CheekSquintRight"]},
    "cheekSquintLeft": {"value": 0, "alt_names": ["CheekSquintLeft"]},
    "cheekPuffSuckRight": {"value": 0, "alt_names": ["CheekPuffSuckRight"]},
    "cheekPuffSuckLeft": {"value": 0, "alt_names": ["CheekPuffSuckLeft"]},

    # Jaw Parameters
    "jawOpen": {"value": 0, "alt_names": ["JawOpen", "JawDrop", "MouthOpen"]},
    "mouthClosed": {"value": 0, "alt_names": ["MouthClosed"]},
    "jawX": {"value": 0, "alt_names": ["JawRight", "JawLeft"]},
    "jawZ": {"value": 0, "alt_names": ["JawForward", "JawBackward"]},
    "jawClench": {"value": 0, "alt_names": ["JawClench"]},
    "jawMandibleRaise": {"value": 0, "alt_names": ["JawMandibleRaise"]},

    # Lip Parameters
    "lipSuckUpperRight": {"value": 0, "alt_names": ["LipSuckUpperRight"]},
    "lipSuckUpperLeft": {"value": 0, "alt_names": ["LipSuckUpperLeft"]},
    "lipSuckLowerRight": {"value": 0, "alt_names": ["LipSuckLowerRight"]},
    "lipSuckLowerLeft": {"value": 0, "alt_names": ["LipSuckLowerLeft"]},
    "lipSuckCornerRight": {"value": 0, "alt_names": ["LipSuckCornerRight"]},
    "lipSuckCornerLeft": {"value": 0, "alt_names": ["LipSuckCornerLeft"]},
    "lipFunnelUpperRight": {"value": 0, "alt_names": ["LipFunnelUpperRight"]},
    "lipFunnelUpperLeft": {"value": 0, "alt_names": ["LipFunnelUpperLeft"]},
    "lipFunnelLowerRight": {"value": 0, "alt_names": ["LipFunnelLowerRight"]},
    "lipFunnelLowerLeft": {"value": 0, "alt_names": ["LipFunnelLowerLeft"]},
    "lipPuckerUpperRight": {"value": 0, "alt_names": ["LipPuckerUpperRight"]},
    "lipPuckerUpperLeft": {"value": 0, "alt_names": ["LipPuckerUpperLeft"]},
    "lipPuckerLowerRight": {"value": 0, "alt_names": ["LipPuckerLowerRight"]},
    "lipPuckerLowerLeft": {"value": 0, "alt_names": ["LipPuckerLowerLeft"]},

    # Mouth Parameters
    "mouthUpperUpRight": {"value": 0, "alt_names": ["MouthUpperUpRight"]},
    "mouthUpperUpLeft": {"value": 0, "alt_names": ["MouthUpperUpLeft"]},
    "mouthLowerDownRight": {"value": 0, "alt_names": ["MouthLowerDownRight"]},
    "mouthLowerDownLeft": {"value": 0, "alt_names": ["MouthLowerDownLeft"]},
    "mouthUpperDeepenRight": {"value": 0, "alt_names": ["MouthUpperDeepenRight"]},
    "mouthUpperDeepenLeft": {"value": 0, "alt_names": ["MouthUpperDeepenLeft"]},
    "mouthUpperX": {"value": 0, "alt_names": ["MouthUpperRight", "MouthUpperLeft"]},
    "mouthLowerX": {"value": 0, "alt_names": ["MouthLowerRight", "MouthLowerLeft"]},
    "mouthCornerPullRight": {"value": 0, "alt_names": ["MouthCornerPullRight"]},
    "mouthCornerPullLeft": {"value": 0, "alt_names": ["MouthCornerPullLeft"]},
    "mouthCornerSlantRight": {"value": 0, "alt_names": ["MouthCornerSlantRight"]},
    "mouthCornerSlantLeft": {"value": 0, "alt_names": ["MouthCornerSlantLeft"]},
    "mouthDimpleRight": {"value": 0, "alt_names": ["MouthDimpleRight"]},
    "mouthDimpleLeft": {"value": 0, "alt_names": ["MouthDimpleLeft"]},
    "mouthFrownRight": {"value": 0, "alt_names": ["MouthFrownRight"]},
    "mouthFrownLeft": {"value": 0, "alt_names": ["MouthFrownLeft"]},
    "mouthStretchRight": {"value": 0, "alt_names": ["MouthStretchRight"]},
    "mouthStretchLeft": {"value": 0, "alt_names": ["MouthStretchLeft"]},
    "mouthRaiserUpper": {"value": 0, "alt_names": ["MouthRaiserUpper"]},
    "mouthRaiserLower": {"value": 0, "alt_names": ["MouthRaiserLower"]},
    "mouthPressRight": {"value": 0, "alt_names": ["MouthPressRight"]},
    "mouthPressLeft": {"value": 0, "alt_names": ["MouthPressLeft"]},
    "mouthTightenerRight": {"value": 0, "alt_names": ["MouthTightenerRight"]},
    "mouthTightenerLeft": {"value": 0, "alt_names": ["MouthTightenerLeft"]},

    # Simplified Tracking Parameters
    # Simplified Eye Parameters
    "EyeX": {"value": 0, "alt_names": ["EyeX"]},
    "EyeY": {"value": 0, "alt_names": ["EyeY"]},

    # Simplified Brow Parameters
    "BrowDownRight": {"value": 0, "alt_names": ["BrowDownRight"]},
    "BrowDownLeft": {"value": 0, "alt_names": ["BrowDownLeft"]},
    "BrowOuterUp": {"value": 0, "alt_names": ["BrowOuterUp"]},
    "BrowInnerUp": {"value": 0, "alt_names": ["BrowInnerUp"]},
    "BrowUp": {"value": 0, "alt_names": ["BrowUp"]},
    "BrowExpressionRight": {"value": 0, "alt_names": ["BrowExpressionRight"]},
    "BrowExpressionLeft": {"value": 0, "alt_names": ["BrowExpressionLeft"]},
    "BrowExpression": {"value": 0, "alt_names": ["BrowExpression"]},

    # Simplified Mouth Parameters
    "MouthX": {"value": 0, "alt_names": ["MouthX"]},
    "MouthUpperUp": {"value": 0, "alt_names": ["MouthUpperUp"]},
    "MouthLowerDown": {"value": 0, "alt_names": ["MouthLowerDown"]},
    #"MouthOpen": {"value": 0, "alt_names": ["MouthOpen"]},             # Substituted as alt name for JawOpen
    "MouthSmileRight": {"value": 0, "alt_names": ["MouthSmileRight"]},
    "MouthSmileLeft": {"value": 0, "alt_names": ["MouthSmileLeft"]},
    "MouthSadRight": {"value": 0, "alt_names": ["MouthSadRight"]},
    "MouthSadLeft": {"value": 0, "alt_names": ["MouthSadLeft"]},
    "SmileFrownRight": {"value": 0, "alt_names": ["SmileFrownRight"]},
    "SmileFrownLeft": {"value": 0, "alt_names": ["SmileFrownLeft"]},
    "SmileFrown": {"value": 0, "alt_names": ["SmileFrown"]},
    "SmileSadRight": {"value": 0, "alt_names": ["SmileSadRight"]},
    "SmileSadLeft": {"value": 0, "alt_names": ["SmileSadLeft"]},
    "SmileSad": {"value": 0, "alt_names": ["SmileSad"]},

    # Simplified Lip Parameters
    "LipSuckUpper": {"value": 0, "alt_names": ["LipSuckUpper"]},
    "LipSuckLower": {"value": 0, "alt_names": ["LipSuckLower"]},
    "LipSuck": {"value": 0, "alt_names": ["LipSuck"]},
    "LipFunnelUpper": {"value": 0, "alt_names": ["LipFunnelUpper"]},
    "LipFunnelLower": {"value": 0, "alt_names": ["LipFunnelLower"]},
    "LipFunnel": {"value": 0, "alt_names": ["LipFunnel"]},
    "LipPuckerUpper": {"value": 0, "alt_names": ["LipPuckerUpper"]},
    "LipPuckerLower": {"value": 0, "alt_names": ["LipPuckerLower"]},
    "LipPucker": {"value": 0, "alt_names": ["LipPucker"]},

    # Simplified Nose and Cheek Parameters
    "NoseSneer": {"value": 0, "alt_names": ["NoseSneer"]},
    "CheekSquint": {"value": 0, "alt_names": ["CheekSquint"]},
    "CheekPuffSuck": {"value": 0, "alt_names": ["CheekPuffSuck"]},
}
"""


FACIAL_PARAMS = {
    # Eye params
    "eyeX": {"value": 0, "alt_names": ["EyeX"]},                # -1 -> 0 look left; 0 -> 1 look right
    "eyeY": {"value": 0, "alt_names": ["EyeY"]},                # -1 -> 0 look down; 0 -> 1 look up
    
    "eyeLeftX": {"value": 0, "alt_names": ["EyeLeftX"]},
    "eyeLeftY": {"value": 0, "alt_names": ["EyeLeftY"]},
    "eyeBlinkLeft": {"value": 0, "alt_names": ["EyeBlinkLeft", "LeftEyeBlink", "LeftEyeLid"]},
    "eyeOpenLeft": {"value": 0, "alt_names": ["EyeOpenLeft", "LeftEyeOpen", "LeftEyeOpening"]},
    "eyeSquintLeft": {"value": 0, "alt_names": ["EyeSquintLeft", "LeftEyeSquint"]},
    
    "eyeRightX": {"value": 0, "alt_names": ["EyeRightX"]},
    "eyeRightY": {"value": 0, "alt_names": ["EyeRightY"]},
    "eyeBlinkRight": {"value": 0, "alt_names": ["EyeBlinkRight", "RightEyeBlink", "RightEyeLid"]},
    "eyeOpenRight": {"value": 0, "alt_names": ["EyeOpenRight", "RightEyeOpen", "RightEyeOpening"]},
    "eyeSquintRight": {"value": 0, "alt_names": ["EyeSquintRight", "RightEyeSquint"]},

    "eyeLidRight": {"value": 0, "alt_names": ["EyeLidRight", "RightEyeOpenness", "RightEyeWiden"]},
    "eyeLidLeft": {"value": 0, "alt_names": ["EyeLidLeft", "LeftEyeOpenness", "LeftEyeWiden"]},
    "eyeLid": {"value": 0, "alt_names": ["EyeLid", "EyesOpenness", "EyesWiden"]},
    "eyeSquintRight": {"value": 0, "alt_names": ["EyeSquintRight"]},
    "eyeSquintLeft": {"value": 0, "alt_names": ["EyeSquintLeft"]},
    "eyeSquint": {"value": 0, "alt_names": ["EyeSquint"]},
    "pupilDilation": {"value": 0, "alt_names": ["PupilDilation"]},
    "pupilDiameterRight": {"value": 0, "alt_names": ["PupilDiameterRight"]},
    "pupilDiameterLeft": {"value": 0, "alt_names": ["PupilDiameterLeft"]},
    "pupilDiameter": {"value": 0, "alt_names": ["PupilDiameter"]},

    # Additional Eye Squint parameters
    "EyeSquintLeft1": {"value": 0, "alt_names": ["EyeSquintLeft1"]},
    "EyeSquintLeft2": {"value": 0, "alt_names": ["EyeSquintLeft2"]},
    "EyeSquintLeft3": {"value": 0, "alt_names": ["EyeSquintLeft3"]},
    "EyeSquintLeft4": {"value": 0, "alt_names": ["EyeSquintLeft4"]},
    "EyeSquintRight1": {"value": 0, "alt_names": ["EyeSquintRight1"]},
    "EyeSquintRight2": {"value": 0, "alt_names": ["EyeSquintRight2"]},
    "EyeSquintRight3": {"value": 0, "alt_names": ["EyeSquintRight3"]},
    "EyeSquintRight4": {"value": 0, "alt_names": ["EyeSquintRight4"]},

    # Eyebrow parameters
    "browUp": {"value": 0, "alt_names": ["BrowUp"]},
    "browDownLeft": {"value": 0, "alt_names": ["BrowDownLeft", "LeftBrowDown", "BrowExpressionLeft"]},      # 0 -> 1 Brow Down
    "browUpLeft": {"value": 0, "alt_names": ["BrowUpLeft", "LeftBrowUp", "BrowRaiseLeft"]},
    "browUpRight": {"value": 0, "alt_names": ["BrowUpRight", "RightBrowUp", "BrowRaiseRight"]},
    
    "browPinchLeft1": {"value": 0, "alt_names": ["BrowPinchLeft1"]},
    "browPinchRight1": {"value": 0, "alt_names": ["BrowPinchRight1"]},
    "browPinchLeft2": {"value": 0, "alt_names": ["BrowPinchLeft2"]},
    "browPinchRight2": {"value": 0, "alt_names": ["BrowPinchRight2"]},
    "BrowPinchLeft4": {"value": 0, "alt_names": ["BrowPinchLeft4"]},
    "BrowPinchRight4": {"value": 0, "alt_names": ["BrowPinchRight4"]},
    "browInnerUp1": {"value": 0, "alt_names": ["BrowInnerUp1"]},
    "browInnerUp2": {"value": 0, "alt_names": ["BrowInnerUp2"]},
    "BrowInnerUp4": {"value": 0, "alt_names": ["BrowInnerUp4"]},
    "BrowExpressionLeft1": {"value": 0, "alt_names": ["BrowExpressionLeft1"]},
    "BrowExpressionRight1": {"value": 0, "alt_names": ["BrowExpressionRight1"]},
    "BrowExpressionLeft2": {"value": 0, "alt_names": ["BrowExpressionLeft2"]},
    "BrowExpressionRight2": {"value": 0, "alt_names": ["BrowExpressionRight2"]},
    "BrowExpressionLeft4": {"value": 0, "alt_names": ["BrowExpressionLeft4"]},
    "BrowExpressionRight4": {"value": 0, "alt_names": ["BrowExpressionRight4"]},

    "browPinchRight": {"value": 0, "alt_names": ["BrowPinchRight"]},
    "browPinchLeft": {"value": 0, "alt_names": ["BrowPinchLeft"]},
    "browLowererRight": {"value": 0, "alt_names": ["BrowLowererRight"]},
    "browLowererLeft": {"value": 0, "alt_names": ["BrowLowererLeft"]},
    "browInnerUpRight": {"value": 0, "alt_names": ["BrowInnerUpRight"]},
    "browInnerUpLeft": {"value": 0, "alt_names": ["BrowInnerUpLeft"]},
    "browOuterUpRight": {"value": 0, "alt_names": ["BrowOuterUpRight"]},
    "browOuterUpLeft": {"value": 0, "alt_names": ["BrowOuterUpLeft"]},
    
    # Mouth parameters
    "mouthOpen": {"value": 0, "alt_names": ["MouthOpen", "JawOpen", "JawDrop"]},
    "jawOpen": {"value": 0, "alt_names": ["JawOpen", "JawDrop", "MouthOpen"]},
    "mouthSmile": {"value": 0, "alt_names": ["MouthSmile", "Smile", "SmileLeft", "SmileRight", "MouthCornerPull"]},
    "mouthFrown": {"value": 0, "alt_names": ["MouthFrown", "Frown", "FrownLeft", "FrownRight", "MouthCornerDepressor"]},
    "mouthPucker": {"value": 0, "alt_names": ["MouthPucker", "Pucker", "LipPucker"]},
    "mouthClosed": {"value": 0, "alt_names": ["MouthClosed"]},
    "MouthClosed1": {"value": 0, "alt_names": ["MouthClosed1"]},
    "MouthClosed2": {"value": 0, "alt_names": ["MouthClosed2"]},
    "MouthClosed4": {"value": 0, "alt_names": ["MouthClosed4"]},
    "MouthClosed8": {"value": 0, "alt_names": ["MouthClosed8"]},
    "MouthDimple1": {"value": 0, "alt_names": ["MouthDimple1"]},
    "MouthDimple2": {"value": 0, "alt_names": ["MouthDimple2"]},
    "mouthShrugUpper": {"value": 0, "alt_names": ["MouthShrugUpper", "UpperLipRaise"]},
    "mouthShrugLower": {"value": 0, "alt_names": ["MouthShrugLower", "LowerLipDepress"]},
    "mouthUpperUp1": {"value": 0, "alt_names": ["MouthUpperUp1"]},
    "mouthUpperUp2": {"value": 0, "alt_names": ["MouthUpperUp2"]},
    "mouthLowerDown1": {"value": 0, "alt_names": ["MouthLowerDown1"]},
    "mouthLowerDown2": {"value": 0, "alt_names": ["MouthLowerDown2"]},
    "mouthPress1": {"value": 0, "alt_names": ["MouthPress1"]},
    "mouthPress2": {"value": 0, "alt_names": ["MouthPress2"]},
    
    # Mouth Raiser parameters
    "MouthRaiserLower1": {"value": 0, "alt_names": ["MouthRaiserLower1"]},
    "MouthRaiserLower2": {"value": 0, "alt_names": ["MouthRaiserLower2"]},
    "MouthRaiserLower4": {"value": 0, "alt_names": ["MouthRaiserLower4"]},
    "MouthRaiserUpper1": {"value": 0, "alt_names": ["MouthRaiserUpper1"]},
    "MouthRaiserUpper2": {"value": 0, "alt_names": ["MouthRaiserUpper2"]},
    "MouthUpperUp4": {"value": 0, "alt_names": ["MouthUpperUp4"]},
    "MouthUpperUp8": {"value": 0, "alt_names": ["MouthUpperUp8"]},
    "MouthLowerDown4": {"value": 0, "alt_names": ["MouthLowerDown4"]},

    # Mouth position parameters
    "MouthX1": {"value": 0, "alt_names": ["MouthX1"]},
    "MouthX2": {"value": 0, "alt_names": ["MouthX2"]},
    "MouthX4": {"value": 0, "alt_names": ["MouthX4"]},
    "MouthX8": {"value": 0, "alt_names": ["MouthX8"]},
    "MouthXNegative": {"value": 0, "alt_names": ["MouthXNegative"]},

    # Jaw parameters
    "JawZ1": {"value": 0, "alt_names": ["JawZ1"]},
    "JawZ2": {"value": 0, "alt_names": ["JawZ2"]},
    "JawZ4": {"value": 0, "alt_names": ["JawZ4"]},
    "JawX1": {"value": 0, "alt_names": ["JawX1"]},
    "JawX2": {"value": 0, "alt_names": ["JawX2"]},
    "JawX4": {"value": 0, "alt_names": ["JawX4"]},
    "JawXNegative": {"value": 0, "alt_names": ["JawXNegative"]},
    "JawForward1": {"value": 0, "alt_names": ["JawForward1"]},
    "JawForward2": {"value": 0, "alt_names": ["JawForward2"]},
    "JawForward4": {"value": 0, "alt_names": ["JawForward4"]},
    "JawOpen1": {"value": 0, "alt_names": ["JawOpen1"]},
    "JawOpen2": {"value": 0, "alt_names": ["JawOpen2"]},
    "JawOpen4": {"value": 0, "alt_names": ["JawOpen4"]},
    "JawOpen8": {"value": 0, "alt_names": ["JawOpen8"]},
    "JawOpen16": {"value": 0, "alt_names": ["JawOpen16"]},
    
    # Lip parameters
    "LipSuckLower1": {"value": 0, "alt_names": ["LipSuckLower1"]},
    "LipSuckLower2": {"value": 0, "alt_names": ["LipSuckLower2"]},
    "LipSuckLower4": {"value": 0, "alt_names": ["LipSuckLower4"]},
    "LipSuckUpper1": {"value": 0, "alt_names": ["LipSuckUpper1"]},
    "LipSuckUpper2": {"value": 0, "alt_names": ["LipSuckUpper2"]},
    "LipSuckUpper4": {"value": 0, "alt_names": ["LipSuckUpper4"]},
    "LipPucker1": {"value": 0, "alt_names": ["LipPucker1"]},
    "LipPucker2": {"value": 0, "alt_names": ["LipPucker2"]},
    "LipPucker4": {"value": 0, "alt_names": ["LipPucker4"]},
    "LipFunnel1": {"value": 0, "alt_names": ["LipFunnel1"]},
    "LipFunnel2": {"value": 0, "alt_names": ["LipFunnel2"]},
    "LipFunnel4": {"value": 0, "alt_names": ["LipFunnel4"]},

    # Tongue parameters
    "tongueOut": {"value": 0, "alt_names": ["TongueOut", "TongueOut1","TongueOut2", "TongueOut4", "TongueOut8"]},
    "TongueOut1": {"value": 0, "alt_names": ["TongueOut1"]},
    "TongueOut2": {"value": 0, "alt_names": ["TongueOut2"]},
    "TongueOut4": {"value": 0, "alt_names": ["TongueOut4"]},
    "TongueOut8": {"value": 0, "alt_names": ["TongueOut8"]},
    
    # Cheek parameters
    "cheekPuff": {"value": 0, "alt_names": ["CheekPuff", "CheekBlow"]},
    "cheekSquintLeft": {"value": 0, "alt_names": ["CheekSquintLeft", "LeftCheekSquint", "cheekPuffSuckLeft1", "CheekPuffSuckLeft2", "CheekPuffSuckLeft4"]},
    "cheekPuffSuckLeft1": {"value": 0, "alt_names": ["CheekPuffSuckLeft1"]},
    "CheekPuffSuckLeft2": {"value": 0, "alt_names": ["CheekPuffSuckLeft2"]},
    "CheekPuffSuckLeft4": {"value": 0, "alt_names": ["CheekPuffSuckLeft4"]},
    "cheekSquintRight": {"value": 0, "alt_names": ["CheekSquintRight", "RightCheekSquint", "cheekPuffSuckRight1", "CheekPuffSuckRight2", "CheekPuffSuckRight4"]},
    "cheekPuffSuckRight1": {"value": 0, "alt_names": ["CheekPuffSuckRight1"]},
    "CheekPuffSuckRight2": {"value": 0, "alt_names": ["CheekPuffSuckRight2"]},
    "CheekPuffSuckRight4": {"value": 0, "alt_names": ["CheekPuffSuckRight4"]},
    "CheekSquint1": {"value": 0, "alt_names": ["CheekSquint1"]},
    "CheekSquint2": {"value": 0, "alt_names": ["CheekSquint2"]},
    "CheekSquint4": {"value": 0, "alt_names": ["CheekSquint4"]},

    # Smile/Sad parameters with intensity levels
    "SmileSadLeft1": {"value": 0, "alt_names": ["SmileSadLeft1"]},
    "SmileSadRight1": {"value": 0, "alt_names": ["SmileSadRight1"]},
    "SmileSadLeft2": {"value": 0, "alt_names": ["SmileSadLeft2"]},
    "SmileSadRight2": {"value": 0, "alt_names": ["SmileSadRight2"]},
    "SmileSadLeft4": {"value": 0, "alt_names": ["SmileSadLeft4"]},
    "SmileSadRight4": {"value": 0, "alt_names": ["SmileSadRight4"]},
    "SmileSadLeft8": {"value": 0, "alt_names": ["SmileSadLeft8"]},
    "SmileSadRight8": {"value": 0, "alt_names": ["SmileSadRight8"]},
    "SmileSadLeftNegative": {"value": 0, "alt_names": ["SmileSadLeftNegative"]},
    "SmileSadRightNegative": {"value": 0, "alt_names": ["SmileSadRightNegative"]},
    
    # Smile/Frown parameters
    "SmileFrownLeft1": {"value": 0, "alt_names": ["SmileFrownLeft1"]},
    "SmileFrownRight1": {"value": 0, "alt_names": ["SmileFrownRight1"]},
    "SmileFrownLeft2": {"value": 0, "alt_names": ["SmileFrownLeft2"]},
    "SmileFrownRight2": {"value": 0, "alt_names": ["SmileFrownRight2"]},
    "SmileFrownLeft4": {"value": 0, "alt_names": ["SmileFrownLeft4"]},
    "SmileFrownRight4": {"value": 0, "alt_names": ["SmileFrownRight4"]},
    "SmileFrownLeft8": {"value": 0, "alt_names": ["SmileFrownLeft8"]},
    "SmileFrownRight8": {"value": 0, "alt_names": ["SmileFrownRight8"]},
    
    # Nose parameters
    "noseSneerLeft": {"value": 0, "alt_names": ["NoseSneerLeft", "LeftNoseSneer", "NoseWrinkleLeft"]},
    "noseSneerRight": {"value": 0, "alt_names": ["NoseSneerRight", "RightNoseSneer", "NoseWrinkleRight"]},
    "noseSneer1": {"value": 0, "alt_names": ["NoseSneer1"]},
    "noseSneer2": {"value": 0, "alt_names": ["NoseSneer2"]},
    "NoseSneer4": {"value": 0, "alt_names": ["NoseSneer4"]},
    "NoseSneerLeft1": {"value": 0, "alt_names": ["NoseSneerLeft1"]},
    "NoseSneerRight1": {"value": 0, "alt_names": ["NoseSneerRight1"]},
    "NoseSneerLeft2": {"value": 0, "alt_names": ["NoseSneerLeft2"]},
    "NoseSneerRight2": {"value": 0, "alt_names": ["NoseSneerRight2"]},
    "NoseSneerLeft4": {"value": 0, "alt_names": ["NoseSneerLeft4"]},
    "NoseSneerRight4": {"value": 0, "alt_names": ["NoseSneerRight4"]}
}
