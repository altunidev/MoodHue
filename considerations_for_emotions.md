Question to ChatGPT:
> What is your understanding of human emotion with regards to face expression? Know anywhere to start for which face expressions should be biased to provide a more accurate end-value for emotional value on a 0-1 scale?

Answer:
> Facial expressions are one of the strongest indicators of human emotion, with certain muscle movements reliably mapping to emotional states. A good starting point is **Paul Ekman’s Facial Action Coding System (FACS)**, which categorizes facial muscle movements (action units, or AUs) and their associated emotions.  
> 
> ### **Key Facial Expressions & Their Emotional Weights**
> 1. **Happiness (Positive Bias)**
>    - **AU6 (Cheek Raiser)** → Raised cheeks, squinting eyes (genuine smile)
>    - **AU12 (Lip Corner Puller)** → Upturned mouth (smiling)
>    - **AU25 (Lips Parting)** → Open-mouth smiles  
>       - *🡆 These should heavily contribute to positive values (0.7 - 1.0 range).*
> 
> 2. **Sadness (Negative Bias)**
>    - **AU1 (Inner Brow Raiser)** → Inner eyebrows up
>    - **AU4 (Brow Lowerer)** → Eyebrows pulled together
>    - **AU15 (Lip Corner Depressor)** → Downturned lips
>    - **AU17 (Chin Raiser)** → Tensed chin
>       - *🡆 These should bias toward a lower emotional value (0.0 - 0.3 range).*
> 
> 3. **Anger (Negative Bias)**
>    - **AU4 (Brow Lowerer)** → Furrowed brows
>    - **AU5 (Upper Lid Raiser)** → Wide eyes
>    - **AU7 (Lid Tightener)** → Squinting
>    - **AU23 (Lip Tightener)** → Pressed lips  
>       - *🡆 Could bias negatively (-1.0 if we considered a range, but in a 0-1 system, closer to 0.2).*
> 
> 4. **Surprise (Neutral to Positive)**
>    - **AU1 + AU2 (Inner + Outer Brow Raiser)** → High eyebrows
>    - **AU5 (Upper Lid Raiser)** → Wide-open eyes
>    - **AU26 (Jaw Drop)** → Open mouth  
>       - *🡆 Surprise can be neutral or positive depending on context (0.5 - 0.8 range).*
> 
> 5. **Fear (Negative Bias)**
>    - **AU1 + AU2 + AU5 (Brow + Lid Raiser)** → Eyebrows high, wide-open eyes
>    - **AU20 (Lip Stretcher)** → Lips pulled sideways  
>       - *🡆 Biases towards negative (0.1 - 0.3 range).*
> 
> 6. **Disgust (Negative Bias)**
>    - **AU9 (Nose Wrinkler)** → Scrunched nose
>    - **AU10 (Upper Lip Raiser)** → Upper lip curled  
>       - *🡆 Should bias towards lower values (0.1 - 0.4 range).*
> 
> ---
> 
> ### **How to Implement Biases in Your Model**
> - **Weighted Sum of Parameters**: Assign higher weights to the most expressive AUs, e.g., `Happiness = (AU6 * 0.4) + (AU12 * 0.6)`.
> - **Normalization**: Ensure that total expression weight stays within the 0-1 range.
> - **Contextual Adjustments**: Some emotions may need adjustments based on combinations (e.g., raised brows with a smile vs. furrowed brows with a smile).

---

That's something I didn't think about before. How do we assign emotion a value? What emotions do we assign, and what granularity or accuracy should we portray?

Since emotion is generally a very subjective thing, what we could try and do instead is ensure we go more-so with measurable aspects of brain processes and make inferences from measurements (i.e. eye tracking, lower face expression, and even brain tracked values, etc.).

So BrainFlowsIntoVRChat already has a pretty neat breakdown into various different things, and puts them into a neat output value of `HueShift`. I believe this is by taking the average of left and right brain focus into one focus parameter value, and then taking the average of left and right brain relax states, putting that into one focus parameter. By taking the average of both average focus and average relax states, it outputs a `HueShift` value.

However, the human emotional state is far more complex than this. So outputting to one value may be a little more tricky. I think we should still strive to go with one simple output value (`HueShift`), but also provide breakouts to other values as well. For instance, happiness, sadness, anger, stress, etc., and provide spectrums for these. By providing one single value, it may lack granularity overall, or assign all emotional state to one parameter when it may be a mix of multiple emotions at the same time. So the goal may shift from providing just one `HueShift` value to multiple, including `HueShift`, but others too.