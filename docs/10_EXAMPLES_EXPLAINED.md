# Examples Explained

## Overview

This document provides detailed analysis of the example files in the `/examples` folder, explaining what the agent should detect and interpret in each case.

## Example 1: The Love Story (Office Romance)

**Files**: 
- `transcription_love_story.json`
- `emotion_analysis_love_story.json`
- `analysis_key_love_story.md`

### Scenario
Elias (team lead) meets Leo (new hire) for the first time. An instant attraction develops beneath professional conversation.

### Key Moments

#### Moment 1: First Sight (00:09.200 - 00:09.400)
**Transcription**: Elias walks in and greets Leo  
**Emotions**: Surprise → Joy → Neutral (rapid sequence)  
**Interpretation**: Elias is struck by Leo's appearance. The micro-expression reveals instant attraction he quickly suppresses.

#### Moment 2: Mutual Recognition (00:13.200 - 00:13.400)
**Transcription**: Leo responds to introduction  
**Emotions**: Surprise → Anxiety → Neutral  
**Interpretation**: Leo also feels the connection. Anxiety (butterflies) appears briefly before he composes himself.

#### Moment 3: Nervous Explanation (00:17.000)
**Transcription**: "I just wanted to check in..."  
**Emotion**: Anxiety  
**Interpretation**: Elias is flustered, trying to act professional but clearly nervous.

#### Moment 4: Genuine Enjoyment (00:21.400)
**Transcription**: Leo laughs  
**Emotion**: Joy  
**Interpretation**: Not polite laughter - genuine joy. He finds Elias endearing.

#### Moment 5: Pride and Connection (00:26.300)
**Transcription**: "That's my baby" (referring to code)  
**Emotion**: Satisfaction  
**Interpretation**: Elias is proud and happy to share his work with Leo specifically.

#### Moment 6: Self-Consciousness (00:34.200)
**Transcription**: "I'm rambling... Sorry."  
**Emotion**: Anxiety  
**Interpretation**: Worried about making a bad impression.

#### Moment 7: Reassurance (00:38.100)
**Transcription**: "No! Not at all."  
**Emotion**: Joy  
**Interpretation**: Leo isn't being polite - he genuinely enjoys the interaction.

#### Moment 8: Flustered Exit (00:48.800)
**Transcription**: "(Clears throat) Look, I... I should let you get back to it"  
**Emotion**: Anxiety  
**Interpretation**: Elias is so flustered by the connection that he abruptly ends the meeting.

#### Moment 9: Mutual Goodbye (00:56.000 & 00:58.500)
**Emotions**: Joy (both speakers)  
**Interpretation**: The conversation ends with both showing clear, unambiguous joy.

### Agent Should Detect:
- Micro-expressions revealing suppressed attraction
- Emotion-speech conflicts (saying one thing, feeling another)
- Bilateral emotional mirroring (mutual attraction)
- Pattern: Professional words + romantic emotions
- Relationship dynamic: Instant mutual attraction

## Example 2: The Case of the Stolen Attestation (Holmes)

**Files**:
- `transcription_holmes.json`
- `emotion_analysis_holmes.json`
- `analysis_key_holmes.md`

### Scenario
Sherlock Holmes interrogates Lord Alistair about a theft. Lord Alistair is guilty and lying about his alibi.

### Key Moments

#### Baseline: Controlled Liar (00:00 - 00:58)
**Pattern**: Concentration + Contempt  
**Interpretation**: Lord Alistair maintains emotional control. Shows contempt when blaming servants. This is a practiced, composed liar.

#### THE TELL: Billiards Question (01:01.300 - 01:01.700)
**Transcription**: "I... what? No. I haven't played in years."  
**Emotions**: Surprise → Fear → Neutral (0.4 second cascade)  
**Interpretation**: Holmes's seemingly random question triggers panic:
1. **Surprise** (01:01.300): "Why is he asking about billiards?"
2. **Fear** (01:01.500): "He knows! He knows about the chalk!"
3. **Neutral** (01:01.700): Conscious suppression, forced composure

This is the critical deception tell - an anomalous emotion spike that breaks his controlled baseline.

#### Confirmation: The Accusation (01:18.400)
**Transcription**: Holmes connects chalk to the document  
**Emotion**: Anger  
**Interpretation**: Not fear (which he's suppressing) but anger at being caught.

#### Holmes's Satisfaction (01:21.000)
**Emotion**: Satisfaction  
**Interpretation**: Holmes confirms his theory by observing the emotional spike at 01:01.500. The case is solved.

### Agent Should Detect:
- Emotional baseline (Concentration/Contempt) vs. anomaly (Fear spike)
- Deception pattern: Controlled emotions with sudden breakdown
- Critical trigger word identifying hidden guilt
- Rapid emotional suppression indicating practiced lying
- Credibility score: Very low due to anomalous response

## Example 3: 20-Minute Lie Detection

**Files**:
- `transcription_20min_lie.json`
- `emotion_analysis_20min_lie.json`
- `analysis_key_20min_lie` (directory)

### Scenario
Extended interview where subject is lying about parts of their story.

### Agent Should Detect:
- Anxiety spikes during specific questions
- Correlation between emotional stress and deceptive statements
- Pattern of emotional control with periodic breakdowns
- Baseline establishment over longer timeline
- Identification of truthful vs. deceptive segments

## Example 4: Double Agent Interview

**Files**:
- `transcription_double_agent.json`
- `emotion_analysis_double_agent.json`
- `analysis_key_double_agent.md`

### Scenario
Intelligence interview of a potential double agent.

### Agent Should Detect:
- Multiple emotional layers (truth, deception, loyalty conflicts)
- Internal conflict manifesting as emotional volatility
- Defensive patterns vs. genuine responses
- Trust indicators vs. deception signals

## Example 5: Office Lovers

**Files**:
- `transcription_office_lovers.json`
- `emotion_analysis_office_lovers.json`
- `analysis_key_lovers.md`

### Scenario
Two colleagues in a secret relationship trying to maintain professionalism.

### Agent Should Detect:
- Hidden affection beneath professional facade
- Mutual emotional mirroring
- Suppressed joy/satisfaction during interactions
- Conflict between public persona and private feelings

## Expected Agent Behavior

### For ALL Examples:

1. **Temporal Alignment**: Accurately match emotions to speech segments
2. **Pattern Recognition**: Identify emotional baselines and anomalies
3. **Micro-Expression Detection**: Catch rapid emotional transitions
4. **Contextual Interpretation**: Understand conversational flow
5. **Natural Language Output**: Generate clear, human-readable interpretations
6. **Evidence-Based Reasoning**: Reference specific timestamps and patterns
7. **Significance Ranking**: Identify critical moments vs. routine exchanges

### Interpretation Quality Criteria:

✅ **Good Interpretation**:
- "At 01:01.300, Lord Alistair experiences a rapid cascade of emotions (Surprise → Fear → Neutral) when Holmes mentions billiards. This 0.4-second emotional sequence breaks his controlled baseline and reveals his guilt about the chalk connection."

❌ **Poor Interpretation**:
- "Subject showed fear at 01:01."

### Testing Checklist

For each example, verify:
- [ ] All transcription segments aligned with emotions
- [ ] Emotional patterns computed correctly
- [ ] Baseline established for each speaker
- [ ] Anomalies detected at expected timestamps
- [ ] Key moments identified with significance levels
- [ ] Natural language interpretations generated
- [ ] Speaker profiles created
- [ ] Behavioral insights synthesized
- [ ] Timeline visualization complete
- [ ] Overall summary matches narrative

## Success Metrics

The agent successfully interprets examples if:
1. **Holmes Example**: Detects the 01:01.300 Fear spike as critical tell
2. **Love Story**: Identifies mutual attraction through micro-expressions
3. **20-Minute Lie**: Distinguishes truthful from deceptive segments
4. **Double Agent**: Reveals internal conflict and loyalty issues
5. **Office Lovers**: Detects hidden affection beneath professionalism

## Next Steps

Use these examples to:
1. Test temporal alignment algorithm
2. Validate agent interpretations
3. Refine LLM prompts
4. Benchmark performance
5. Demonstrate system capabilities

Return to [README.md](./README.md) for complete documentation index.
