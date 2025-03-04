FACIAL_PARAMS = {
    # Base VRC Eye params
    "eyesClosedAmount": {"value": 0, "alt_names": ["EyesClosedAmount", "EyeClosed", "EyeClosureAmount"]},
    "centerPitchYaw": {"value": 0, "alt_names": ["CenterPitchYaw", "EyePitchYaw", "EyeTracking"]},

    # Eye params
    "eyeX": {"value": 0, "alt_names": ["EyeX"]},                #  0 -> 1
    "eyeY": {"value": 0, "alt_names": ["EyeY"]},
    "eyeLeftX": {"value": 0, "alt_names": ["EyeLeftX"]},        # -1 -> 1
    "eyeLeftY": {"value": 0, "alt_names": ["EyeLeftY"]},
    "eyeSquint": {"value": 0, "alt_names": ["EyeSquint"]},
    "eyeLidLeft": {"value": 0, "alt_names": ["EyeLidLeft"]},    # 0 -> 0.75 close; 0.75 -> 1 widen
    "eyeBlinkLeft": {"value": 0, "alt_names": ["EyeBlinkLeft", "LeftEyeBlink", "LeftEyeLid"]},  # 
    "eyeOpenLeft": {"value": 0, "alt_names": ["EyeOpenLeft", "LeftEyeOpen", "LeftEyeOpening"]}, # 
    "eyeSquintLeft": {"value": 0, "alt_names": ["EyeSquintLeft", "LeftEyeSquint"]},             # 
    "eyeRightX": {"value": 0, "alt_names": ["EyeRightX"]},
    "eyeRightY": {"value": 0, "alt_names": ["EyeRightY"]},
    "eyeLidRight": {"value": 0, "alt_names": ["EyeLidRight"]},
    "eyeBlinkRight": {"value": 0, "alt_names": ["EyeBlinkRight", "RightEyeBlink", "RightEyeLid"]},
    "eyeOpenRight": {"value": 0, "alt_names": ["EyeOpenRight", "RightEyeOpen", "RightEyeOpening"]},
    "eyeSquintRight": {"value": 0, "alt_names": ["EyeSquintRight", "RightEyeSquint"]},

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
    "browDownLeft": {"value": 0, "alt_names": ["BrowDownLeft", "LeftBrowDown", "BrowExpressionLeft"]},
    "browDownRight": {"value": 0, "alt_names": ["BrowDownRight", "RightBrowDown", "BrowExpressionRight"]},
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
    "tongueOut": {"value": 0, "alt_names": ["TongueOut"]},
    "TongueOut1": {"value": 0, "alt_names": ["TongueOut1"]},
    "TongueOut2": {"value": 0, "alt_names": ["TongueOut2"]},
    "TongueOut4": {"value": 0, "alt_names": ["TongueOut4"]},
    "TongueOut8": {"value": 0, "alt_names": ["TongueOut8"]},
    
    # Cheek parameters
    "cheekPuff": {"value": 0, "alt_names": ["CheekPuff", "CheekBlow"]},
    "cheekSquintLeft": {"value": 0, "alt_names": ["CheekSquintLeft", "LeftCheekSquint"]},
    "cheekSquintRight": {"value": 0, "alt_names": ["CheekSquintRight", "RightCheekSquint"]},
    "cheekPuffSuckLeft1": {"value": 0, "alt_names": ["CheekPuffSuckLeft1"]},
    "cheekPuffSuckRight1": {"value": 0, "alt_names": ["CheekPuffSuckRight1"]},
    "CheekPuffSuckLeft2": {"value": 0, "alt_names": ["CheekPuffSuckLeft2"]},
    "CheekPuffSuckRight2": {"value": 0, "alt_names": ["CheekPuffSuckRight2"]},
    "CheekPuffSuckLeft4": {"value": 0, "alt_names": ["CheekPuffSuckLeft4"]},
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