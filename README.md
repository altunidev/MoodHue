# MoodHue
A listener that takes OSC input from various sources and outputs hue shift values based on mood.

## What's this?

This program listens for OSC messages from various biometric tracking sources and attempts to determine a mood to match. Currently this takes input from the following sources:

- [ ] Face and Eye (combined)
- [ ] Face (standalone)
- [ ] Eye (standalone)
- [ ] Heart Rate
- [ ] Brain (via [BrainFlowsIntoVRChat](https://github.com/ChilloutCharles/BrainflowsIntoVRChat))
- [ ] Custom sources (TouchOSC)

## Where does this go?

I eventually plan to integrate a sentiment analysis algorithm of some sort to collect biometric data from various sources (combined ideally for more datapoints) to provide a generally highly accurate emotional-state mood state and provide a float point output via OSC, easily integrated into a single hue shift parameter for a "mood stone" of some sort. This may take a little more time, and may be highly overengineered. Too bad.