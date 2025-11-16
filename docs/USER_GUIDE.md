# User Guide

## Emotion Interpretation Machine - Quick Start Guide

This guide helps you get started with using the Emotion Interpretation Machine to analyze conversations.

---

## Table of Contents

1. [What is the Emotion Interpretation Machine?](#what-is-the-emotion-interpretation-machine)
2. [Quick Start](#quick-start)
3. [Input Data Format](#input-data-format)
4. [Understanding Reports](#understanding-reports)
5. [Use Cases](#use-cases)
6. [Best Practices](#best-practices)
7. [FAQ](#faq)

---

## What is the Emotion Interpretation Machine?

The Emotion Interpretation Machine is an AI-powered system that analyzes conversations by combining:

- **Transcription data**: What was said (speech-to-text)
- **Emotion data**: How it was said (facial emotion detection)

By matching emotional signals with spoken content, the system reveals:
- Emotional authenticity vs. deception
- Hidden feelings and unexpressed emotions
- Critical moments where verbal and emotional signals diverge
- Behavioral patterns and psychological tells

---

## Quick Start

### Step 1: Start the Server

```bash
python src/main.py
```

The API will be available at `http://localhost:3001`

### Step 2: Create a Session

```bash
curl -X POST http://localhost:3001/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"name": "My First Analysis"}'
```

Response:
```json
{
  "id": 1,
  "name": "My First Analysis",
  "status": "created",
  "created_at": "2025-11-16T10:00:00.000Z",
  "updated_at": "2025-11-16T10:00:00.000Z"
}
```

**Note the `id`** - you'll need it for subsequent steps.

### Step 3: Upload Transcription Data

Prepare your transcription file (`transcription.json`):

```json
{
  "entries": [
    {
      "startTime": "00:03.400",
      "endTime": "00:07.800",
      "speaker": "Alice",
      "transcript": "I was at home all evening."
    },
    {
      "startTime": "00:08.500",
      "endTime": "00:12.300",
      "speaker": "Bob",
      "transcript": "Are you sure about that?"
    }
  ]
}
```

Upload it:

```bash
curl -X POST http://localhost:3001/api/sessions/1/transcription \
  -H "Content-Type: application/json" \
  -d @transcription.json
```

### Step 4: Upload Emotion Data

Prepare your emotion file (`emotions.json`):

```json
{
  "detections": [
    {
      "timestamp": "00:03.500",
      "emotion": "Fear",
      "confidence": 0.85
    },
    {
      "timestamp": "00:08.600",
      "emotion": "Neutral",
      "confidence": 0.90
    }
  ]
}
```

Upload it:

```bash
curl -X POST http://localhost:3001/api/sessions/1/emotions \
  -H "Content-Type: application/json" \
  -d @emotions.json
```

### Step 5: Check Status

```bash
curl http://localhost:3001/api/sessions/1/status
```

Expected response:
```json
{
  "session_id": 1,
  "name": "My First Analysis",
  "status": "ready",
  "data": {
    "transcription_entries": 2,
    "emotion_detections": 2,
    "aligned_events": 0,
    "reports": 0
  }
}
```

**Status should be `ready`** before proceeding.

### Step 6: Run Analysis

```bash
curl -X POST http://localhost:3001/api/sessions/1/analyze
```

Response:
```json
{
  "message": "Analysis completed successfully",
  "session_id": 1,
  "report_id": 1,
  "critical_moments_found": 1,
  "steps_completed": [
    "temporal_alignment",
    "emotion_pattern_analysis",
    "anomaly_detection",
    "moment_interpretation",
    "speaker_profiling",
    "report_synthesis"
  ]
}
```

**Note**: Analysis may take 10-30 seconds depending on data size.

### Step 7: Download Report

**JSON Format** (structured data):
```bash
curl http://localhost:3001/api/sessions/1/report.json -o report.json
```

**Markdown Format** (human-readable):
```bash
curl http://localhost:3001/api/sessions/1/report.md -o report.md
```

---

## Input Data Format

### Transcription Format

Transcription data consists of time-segmented speech entries.

**Required Fields**:
- `startTime`: When the speech segment starts (format: `MM:SS.mmm`)
- `endTime`: When the speech segment ends (format: `MM:SS.mmm`)
- `speaker`: Name of the person speaking
- `transcript`: What was said

**Example**:
```json
{
  "entries": [
    {
      "startTime": "00:03.400",
      "endTime": "00:07.800",
      "speaker": "Detective",
      "transcript": "Where were you on the night of the 15th?"
    },
    {
      "startTime": "00:08.500",
      "endTime": "00:12.300",
      "speaker": "Suspect",
      "transcript": "I... I was at home. Watching TV."
    }
  ]
}
```

**Time Format Notes**:
- Format: `MM:SS.mmm` (minutes:seconds.milliseconds)
- Examples:
  - `00:03.400` = 3.4 seconds
  - `01:23.500` = 1 minute 23.5 seconds
  - `12:45.678` = 12 minutes 45.678 seconds

### Emotion Format

Emotion data consists of timestamped emotion detections.

**Required Fields**:
- `timestamp`: When the emotion was detected (format: `MM:SS.mmm`)
- `emotion`: The detected emotion (e.g., "Fear", "Neutral", "Surprise")
- `confidence`: Confidence score (0.0 to 1.0)

**Example**:
```json
{
  "detections": [
    {
      "timestamp": "00:03.500",
      "emotion": "Neutral",
      "confidence": 0.92
    },
    {
      "timestamp": "00:08.600",
      "emotion": "Fear",
      "confidence": 0.85
    },
    {
      "timestamp": "00:09.200",
      "emotion": "Anxiety",
      "confidence": 0.78
    }
  ]
}
```

**Supported Emotions**:
- Neutral
- Happy
- Sad
- Angry
- Fear
- Surprise
- Disgust
- Anxiety
- Contempt

---

## Understanding Reports

### Report Structure

Reports contain several key sections:

#### 1. Executive Summary
High-level overview of findings and key insights.

#### 2. Critical Moments
Significant moments requiring attention, typically where:
- Emotions contradict verbal content
- Unusual emotional spikes occur
- Potential deception indicators are detected

**Example**:
```markdown
### 1. 01:01.500 - Lord Alistair

**Quote:** "I... I never left the room."
**Emotions:** Fear (0.85)
**Analysis:** Fear spike during denial - potential deception indicator. 
The hesitation combined with fear suggests this statement may not be truthful.
```

#### 3. Speaker Profiles
Emotional baseline and behavioral patterns for each speaker.

**Example**:
```markdown
### Lord Alistair

**Baseline Emotions:**
- Neutral: 15 occurrences (avg confidence: 0.80)
- Fear: 8 occurrences (avg confidence: 0.82)

**Patterns:**
- Shows elevated fear levels when discussing his whereabouts
- Significantly deviates from baseline during key questions
```

#### 4. Emotion Patterns
Emotional transitions and sequences throughout the conversation.

**Example**:
```markdown
**Emotion Transitions:** 12
**Emotion Sequence:** Neutral → Fear → Anxiety → Fear → Neutral
```

#### 5. Behavioral Anomalies
Unexpected emotional responses or unusual patterns.

**Example**:
```markdown
1. **01:30.000 - Alice:** Sudden anger spike when asked about finances
2. **02:15.500 - Bob:** Inappropriate laughter during serious topic
```

#### 6. Timeline
Chronological view of critical moments and anomalies.

---

## Use Cases

### 1. Investigative Interviews

**Purpose**: Detect deception and assess credibility

**What to Look For**:
- Fear spikes during denials
- Emotional incongruence with statements
- Baseline deviations during critical questions

**Example**:
```
Critical Moment: "I wasn't there" + Fear (0.85)
Interpretation: High probability of deception
```

### 2. Relationship Analysis

**Purpose**: Understand romantic attraction and chemistry

**What to Look For**:
- Hidden positive emotions
- Emotional synchronization
- Unexpressed feelings

**Example**:
```
Critical Moment: "We're just friends" + Joy (0.92)
Interpretation: Verbal statement conflicts with positive emotions
```

### 3. Customer Service Quality

**Purpose**: Assess customer satisfaction and agent performance

**What to Look For**:
- Customer frustration patterns
- Agent empathy levels
- Satisfaction indicators

### 4. Negotiation Analysis

**Purpose**: Understand negotiation dynamics and leverage

**What to Look For**:
- Anxiety during price discussions
- Confidence levels
- Emotional pressure points

---

## Best Practices

### 1. Data Quality

✅ **Do**:
- Use high-quality transcription data
- Ensure accurate timestamps
- Include all speakers
- Capture complete conversations

❌ **Don't**:
- Use auto-generated transcripts without review
- Skip emotion data for key moments
- Mix different conversation sessions

### 2. Time Alignment

✅ **Do**:
- Ensure transcription and emotion timestamps match
- Use millisecond precision
- Verify timestamp accuracy

❌ **Don't**:
- Use different time bases
- Round timestamps excessively

### 3. Interpretation

✅ **Do**:
- Read the full report context
- Consider cultural factors
- Look for patterns, not isolated moments
- Combine with other evidence

❌ **Don't**:
- Rely solely on single critical moments
- Ignore cultural emotional expressions
- Make decisions based only on AI interpretation

### 4. Privacy and Ethics

✅ **Do**:
- Obtain consent for emotion analysis
- Anonymize data where possible
- Follow data protection regulations
- Use ethically and responsibly

❌ **Don't**:
- Analyze without consent
- Share reports without authorization
- Use for discriminatory purposes

---

## FAQ

### Q: How accurate is the emotion detection?

**A**: The system analyzes emotions based on the input data you provide. Accuracy depends on the quality of your emotion detection system. The interpretation is based on patterns, not single datapoints.

### Q: What if I don't have emotion data?

**A**: Both transcription and emotion data are required for analysis. The system cannot function with transcription alone.

### Q: Can I analyze real-time conversations?

**A**: Currently, the system processes pre-recorded data in batch mode. Real-time analysis is not supported in this version.

### Q: How long does analysis take?

**A**: Typical analysis takes 10-30 seconds depending on conversation length and complexity.

### Q: Can I reanalyze a session?

**A**: Yes, you can run analysis multiple times on the same session. Each analysis creates a new report.

### Q: What languages are supported?

**A**: The system works with any language in your transcription data. Emotion analysis is language-independent.

### Q: How much data can I analyze?

**A**: The system can handle conversations up to several hours long. For very long conversations, consider splitting into smaller sessions.

### Q: Can I delete my data?

**A**: Currently, there's no delete endpoint in the API. You can manually delete the SQLite database file to remove all data.

### Q: Is the analysis stored permanently?

**A**: Analysis results are stored in the SQLite database. Consider implementing data retention policies for production use.

### Q: Can I customize the analysis?

**A**: The current version uses predefined analysis logic. Customization requires code modifications.

---

## Examples

### Example 1: Holmes Investigation

See `examples/transcription_holmes.json` and `examples/emotion_analysis_holmes.json` for a complete deception detection example.

**Key Finding**: Fear spike at 01:01 during denial statement indicates potential deception.

### Example 2: Love Story

See `examples/transcription_love_story.json` and `examples/emotion_analysis_love_story.json` for relationship dynamics analysis.

**Key Finding**: Hidden positive emotions contradict "just friends" statements.

### Example 3: Extended Interview

See `examples/transcription_20min_lie.json` and `examples/emotion_analysis_20min_lie.json` for long-form analysis.

**Key Finding**: Consistent anxiety patterns during specific time periods reveal stress markers.

---

## Getting Help

- **API Documentation**: See `docs/API_DOCUMENTATION.md`
- **Deployment Guide**: See `docs/DEPLOYMENT_GUIDE.md`
- **Technical Docs**: See `docs/` folder
- **Issues**: Create an issue on GitHub

---

**Version**: 1.0.0  
**Last Updated**: November 16, 2025

Happy analyzing! 🎭
