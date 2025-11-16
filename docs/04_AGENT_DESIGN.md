# Agent Design Specification

## Overview

This document details the AI agent design for interpreting emotion-transcription alignments. The agent uses LangGraph for orchestration and AWS Bedrock (Claude 3.5) for reasoning.

## Agent Architecture

### ReAct Pattern

The agent follows the **ReAct (Reasoning + Acting)** pattern:

```
Thought → Action → Observation → Thought → ... → Answer
```

**Applied to Emotion Interpretation**:
1. **Reason**: Analyze emotion-transcription correlations
2. **Act**: Use tools to detect patterns, anomalies, and context
3. **Observe**: Process tool outputs
4. **Repeat**: Build comprehensive interpretation
5. **Answer**: Generate final report

### Agent State

```python
from typing import TypedDict, Annotated, List, Dict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class InterpretationState(TypedDict):
    """State for emotion interpretation agent"""
    
    # Message history (for LLM context)
    messages: Annotated[List[AnyMessage], add_messages]
    
    # Input data
    transcription_data: List[TranscriptionEntry]
    emotion_data: List[EmotionEntry]
    
    # Processed data
    aligned_events: List[AlignedEvent]
    context_windows: List[ContextWindow]
    
    # Analysis results
    emotion_patterns: Dict[str, EmotionPattern]
    anomalies: List[Anomaly]
    key_moments: List[InterpretedMoment]
    
    # Speaker analysis
    speaker_baselines: Dict[str, EmotionBaseline]
    speaker_profiles: Dict[str, SpeakerProfile]
    
    # Insights
    behavioral_insights: List[Insight]
    relationship_dynamics: List[RelationshipInsight]
    
    # Report
    summary: Summary
    timeline: List[TimelineEvent]
    
    # Metadata
    session_id: str
    trace_id: str
    iteration_count: int
    is_last_step: bool
```

## Agent Graph

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Create graph
workflow = StateGraph(InterpretationState)

# Add nodes
workflow.add_node("validate_input", validate_input_data)
workflow.add_node("temporal_alignment", perform_temporal_alignment)
workflow.add_node("pattern_analysis", analyze_emotion_patterns)
workflow.add_node("anomaly_detection", detect_emotional_anomalies)
workflow.add_node("context_building", build_conversation_context)
workflow.add_node("interpret_moments", interpret_key_moments)
workflow.add_node("speaker_profiling", create_speaker_profiles)
workflow.add_node("insight_generation", generate_behavioral_insights)
workflow.add_node("report_synthesis", synthesize_final_report)

# Define edges (linear flow)
workflow.add_edge(START, "validate_input")
workflow.add_edge("validate_input", "temporal_alignment")
workflow.add_edge("temporal_alignment", "pattern_analysis")
workflow.add_edge("pattern_analysis", "anomaly_detection")
workflow.add_edge("anomaly_detection", "context_building")
workflow.add_edge("context_building", "interpret_moments")
workflow.add_edge("interpret_moments", "speaker_profiling")
workflow.add_edge("speaker_profiling", "insight_generation")
workflow.add_edge("insight_generation", "report_synthesis")
workflow.add_edge("report_synthesis", END)

# Compile with checkpointer for state persistence
memory = MemorySaver()
agent = workflow.compile(checkpointer=memory)
```

## Agent Nodes Implementation

### 1. Validate Input Node

```python
def validate_input_data(state: InterpretationState) -> InterpretationState:
    """
    Validates input data schemas and basic constraints
    """
    transcription = state["transcription_data"]
    emotions = state["emotion_data"]
    
    # Validate schemas
    validate_transcription_schema(transcription)
    validate_emotion_schema(emotions)
    
    # Check temporal coverage
    trans_start = min(t["startTime"] for t in transcription)
    trans_end = max(t["endTime"] for t in transcription)
    emot_start = min(e["timestamp"] for e in emotions)
    emot_end = max(e["timestamp"] for e in emotions)
    
    if emot_start > trans_start or emot_end < trans_end:
        logging.warning("Emotion data doesn't fully cover transcription timeline")
    
    return state
```

### 2. Temporal Alignment Node

```python
def perform_temporal_alignment(state: InterpretationState) -> InterpretationState:
    """
    Aligns emotion detections with transcription segments
    """
    transcription = state["transcription_data"]
    emotions = state["emotion_data"]
    
    # Use tool for alignment
    alignment_tool = TemporalAlignmentTool()
    aligned_events = alignment_tool.run(
        transcription=transcription,
        emotions=emotions
    )
    
    state["aligned_events"] = aligned_events
    
    # Log to observability
    log_metric("AlignedEvents", len(aligned_events))
    
    return state
```

### 3. Pattern Analysis Node

```python
def analyze_emotion_patterns(state: InterpretationState) -> InterpretationState:
    """
    Analyzes emotion patterns for each aligned event and speaker
    """
    aligned_events = state["aligned_events"]
    
    # Analyze patterns per event
    event_patterns = {}
    for event in aligned_events:
        pattern = compute_emotion_pattern(event.emotions)
        event_patterns[event.id] = pattern
    
    # Analyze patterns per speaker
    speakers = set(e.speaker for e in aligned_events)
    speaker_baselines = {}
    
    for speaker in speakers:
        speaker_events = [e for e in aligned_events if e.speaker == speaker]
        baseline = compute_speaker_baseline(speaker_events)
        speaker_baselines[speaker] = baseline
    
    state["emotion_patterns"] = event_patterns
    state["speaker_baselines"] = speaker_baselines
    
    return state
```

### 4. Anomaly Detection Node

```python
def detect_emotional_anomalies(state: InterpretationState) -> InterpretationState:
    """
    Detects anomalous emotional responses relative to baselines
    """
    aligned_events = state["aligned_events"]
    speaker_baselines = state["speaker_baselines"]
    
    anomalies = []
    
    for event in aligned_events:
        baseline = speaker_baselines[event.speaker]
        
        # Check for emotion spikes
        for emotion_det in event.emotions:
            if is_anomalous(emotion_det.emotion, baseline):
                anomaly = Anomaly(
                    event_id=event.id,
                    timestamp=emotion_det.timestamp,
                    emotion=emotion_det.emotion,
                    expected=baseline.dominant_emotion,
                    severity=compute_anomaly_severity(
                        emotion_det.emotion, 
                        baseline
                    ),
                    reason=generate_anomaly_reason(
                        emotion_det, 
                        baseline, 
                        event.transcript
                    )
                )
                anomalies.append(anomaly)
    
    state["anomalies"] = anomalies
    
    return state
```

### 5. Context Building Node

```python
def build_conversation_context(state: InterpretationState) -> InterpretationState:
    """
    Groups events into conversation windows with context
    """
    aligned_events = state["aligned_events"]
    
    # Define window size (e.g., 30 seconds)
    window_size_ms = 30000
    
    context_windows = []
    current_window = []
    window_start = aligned_events[0].startTime
    
    for event in aligned_events:
        if event.startTime - window_start > window_size_ms:
            # Create window from accumulated events
            window = ContextWindow(
                id=f"window_{len(context_windows)}",
                startTime=window_start,
                endTime=current_window[-1].endTime,
                events=current_window,
                conversationFlow=classify_conversation_stage(current_window),
                speakers=list(set(e.speaker for e in current_window)),
                emotionalTrend=compute_emotional_trend(current_window)
            )
            context_windows.append(window)
            
            # Start new window
            current_window = [event]
            window_start = event.startTime
        else:
            current_window.append(event)
    
    # Add final window
    if current_window:
        window = ContextWindow(
            id=f"window_{len(context_windows)}",
            startTime=window_start,
            endTime=current_window[-1].endTime,
            events=current_window,
            conversationFlow=classify_conversation_stage(current_window),
            speakers=list(set(e.speaker for e in current_window)),
            emotionalTrend=compute_emotional_trend(current_window)
        )
        context_windows.append(window)
    
    state["context_windows"] = context_windows
    
    return state
```

### 6. Interpret Moments Node (LLM-Powered)

```python
from langchain_core.prompts import ChatPromptTemplate

INTERPRETATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert behavioral analyst specializing in 
    emotion-speech correlation analysis. Analyze the provided moment and 
    generate a clear, evidence-based interpretation.
    
    Consider:
    - Emotion authenticity vs. deception
    - Micro-expressions and suppression
    - Context from surrounding conversation
    - Speaker behavioral patterns
    
    Provide:
    1. Natural language interpretation
    2. Significance level (critical/high/medium/low)
    3. Reasoning chain
    4. Related patterns or moments"""),
    
    ("human", """Analyze this moment:
    
    Timestamp: {timestamp}
    Speaker: {speaker}
    Transcript: "{transcript}"
    
    Emotions detected:
    {emotions}
    
    Emotion pattern:
    - Dominant: {dominant_emotion}
    - Sequence: {emotion_sequence}
    - Transitions: {transition_count}
    - Anomaly score: {anomaly_score}
    
    Speaker baseline: {speaker_baseline}
    
    Context (previous 3 events):
    {context}
    
    Related anomalies:
    {anomalies}
    
    Generate interpretation:""")
])

def interpret_key_moments(state: InterpretationState) -> InterpretationState:
    """
    Uses LLM to interpret significant moments
    """
    aligned_events = state["aligned_events"]
    anomalies = state["anomalies"]
    context_windows = state["context_windows"]
    speaker_baselines = state["speaker_baselines"]
    
    # Identify key moments (those with anomalies or high significance)
    key_event_ids = set(a.event_id for a in anomalies)
    
    # Also include events with high emotional volatility
    for event in aligned_events:
        if event.emotionPattern.transitionCount > 3:
            key_event_ids.add(event.id)
    
    # Interpret each key moment using LLM
    model = initialize_llm()
    chain = INTERPRETATION_PROMPT | model
    
    interpreted_moments = []
    
    for event_id in key_event_ids:
        event = next(e for e in aligned_events if e.id == event_id)
        
        # Get context
        context_events = get_context_events(event, aligned_events, n=3)
        related_anomalies = [a for a in anomalies if a.event_id == event_id]
        
        # Generate interpretation
        response = chain.invoke({
            "timestamp": milliseconds_to_timestamp(event.startTime),
            "speaker": event.speaker,
            "transcript": event.transcript,
            "emotions": format_emotions(event.emotions),
            "dominant_emotion": event.emotionPattern.dominantEmotion,
            "emotion_sequence": event.emotionPattern.emotionSequence,
            "transition_count": event.emotionPattern.transitionCount,
            "anomaly_score": event.emotionPattern.anomalyScore,
            "speaker_baseline": speaker_baselines[event.speaker],
            "context": format_context(context_events),
            "anomalies": format_anomalies(related_anomalies)
        })
        
        # Parse LLM response
        interpreted_moment = parse_interpretation_response(
            response, 
            event, 
            related_anomalies
        )
        
        interpreted_moments.append(interpreted_moment)
    
    state["key_moments"] = interpreted_moments
    
    return state
```

### 7. Speaker Profiling Node

```python
def create_speaker_profiles(state: InterpretationState) -> InterpretationState:
    """
    Creates comprehensive profiles for each speaker
    """
    aligned_events = state["aligned_events"]
    speaker_baselines = state["speaker_baselines"]
    key_moments = state["key_moments"]
    
    speakers = set(e.speaker for e in aligned_events)
    speaker_profiles = {}
    
    for speaker in speakers:
        speaker_events = [e for e in aligned_events if e.speaker == speaker]
        speaker_moments = [m for m in key_moments if m.speaker == speaker]
        
        # Collect all emotions
        all_emotions = []
        for event in speaker_events:
            all_emotions.extend([e.emotion for e in event.emotions])
        
        # Identify patterns
        patterns = identify_behavioral_patterns(speaker_events, speaker_moments)
        
        # Assess credibility (for deception detection)
        credibility = assess_speaker_credibility(
            speaker_events,
            speaker_moments,
            speaker_baselines[speaker]
        )
        
        profile = SpeakerProfile(
            speaker=speaker,
            emotionalBaseline=speaker_baselines[speaker].dominant_emotion,
            emotionalRange=list(set(all_emotions)),
            behavioralPatterns=patterns,
            credibility=credibility,
            keyCharacteristics=extract_characteristics(
                speaker_events, 
                speaker_moments
            )
        )
        
        speaker_profiles[speaker] = profile
    
    state["speaker_profiles"] = speaker_profiles
    
    return state
```

### 8. Insight Generation Node

```python
def generate_behavioral_insights(state: InterpretationState) -> InterpretationState:
    """
    Generates high-level behavioral insights
    """
    key_moments = state["key_moments"]
    speaker_profiles = state["speaker_profiles"]
    aligned_events = state["aligned_events"]
    
    insights = []
    
    # Deception insights
    for speaker, profile in speaker_profiles.items():
        if profile.credibility < 0.5:
            insight = Insight(
                type="deceptive",
                insight=f"{speaker} shows signs of deception: "
                        f"credibility score {profile.credibility:.2f}",
                evidence=[m.id for m in key_moments if m.speaker == speaker],
                confidence=1.0 - profile.credibility
            )
            insights.append(insight)
    
    # Relationship insights (multi-speaker)
    if len(speaker_profiles) >= 2:
        relationship_insight = analyze_relationship_dynamics(
            aligned_events,
            key_moments,
            speaker_profiles
        )
        if relationship_insight:
            insights.append(relationship_insight)
    
    # Emotional pattern insights
    pattern_insights = identify_emotional_themes(
        aligned_events,
        key_moments
    )
    insights.extend(pattern_insights)
    
    state["behavioral_insights"] = insights
    
    return state
```

### 9. Report Synthesis Node

```python
def synthesize_final_report(state: InterpretationState) -> InterpretationState:
    """
    Compiles all analysis into final report
    """
    # Generate summary
    summary = generate_summary(state)
    state["summary"] = summary
    
    # Generate timeline
    timeline = generate_timeline(
        state["aligned_events"],
        state["key_moments"],
        state["anomalies"]
    )
    state["timeline"] = timeline
    
    # Update iteration count
    state["iteration_count"] = state.get("iteration_count", 0) + 1
    state["is_last_step"] = True
    
    return state
```

## Agent Tools

### 1. Temporal Alignment Tool

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class TemporalAlignmentInput(BaseModel):
    transcription: List[dict] = Field(description="Transcription entries")
    emotions: List[dict] = Field(description="Emotion detections")

class TemporalAlignmentTool(BaseTool):
    name = "temporal_aligner"
    description = """Aligns emotion detection data with transcription segments.
    Returns aligned events with emotion patterns for each speech segment."""
    args_schema = TemporalAlignmentInput
    
    def _run(self, transcription: List[dict], emotions: List[dict]) -> List[AlignedEvent]:
        return align_emotion_with_transcript(transcription, emotions)
```

### 2. Emotion Pattern Detector Tool

```python
class EmotionPatternInput(BaseModel):
    emotions: List[dict] = Field(description="Sequence of emotion detections")

class EmotionPatternDetectorTool(BaseTool):
    name = "emotion_pattern_detector"
    description = """Analyzes emotion sequences to identify patterns.
    Returns pattern metrics: dominant emotion, transitions, volatility."""
    args_schema = EmotionPatternInput
    
    def _run(self, emotions: List[dict]) -> EmotionPattern:
        return compute_emotion_pattern(emotions)
```

### 3. Anomaly Detector Tool

```python
class AnomalyDetectorInput(BaseModel):
    event: dict = Field(description="Aligned event to analyze")
    baseline: dict = Field(description="Speaker's emotional baseline")

class AnomalyDetectorTool(BaseTool):
    name = "anomaly_detector"
    description = """Detects anomalous emotional responses.
    Compares event emotions against speaker baseline."""
    args_schema = AnomalyDetectorInput
    
    def _run(self, event: dict, baseline: dict) -> List[Anomaly]:
        return detect_event_anomalies(event, baseline)
```

## LLM Configuration

```python
from core.react_agent.holistic_ai_bedrock import HolisticAIBedrockChat
from langchain_core.language_models import BaseChatModel
from pydantic import SecretStr
import os

def initialize_llm() -> BaseChatModel:
    """Initialize LLM for interpretation using Holistic AI Bedrock proxy"""
    
    model = HolisticAIBedrockChat(
        team_id=os.getenv("HOLISTIC_AI_TEAM_ID"),
        api_token=SecretStr(os.getenv("HOLISTIC_AI_API_TOKEN")),
        model="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        temperature=0.3,
        max_tokens=4096,
        top_p=0.9
    )
    
    return model
```

**Note**: This uses the Holistic AI proxy to access AWS Bedrock, which simplifies authentication and provides additional monitoring capabilities.

## Agent Invocation

```python
async def run_interpretation_agent(
    session_id: str,
    transcription_data: List[dict],
    emotion_data: List[dict]
) -> InterpretationReport:
    """
    Run the interpretation agent
    """
    
    # Initialize state
    initial_state = {
        "transcription_data": transcription_data,
        "emotion_data": emotion_data,
        "session_id": session_id,
        "trace_id": generate_trace_id(),
        "iteration_count": 0,
        "is_last_step": False,
        "messages": []
    }
    
    # Run agent
    config = {
        "configurable": {
            "thread_id": session_id
        }
    }
    
    final_state = await agent.ainvoke(initial_state, config=config)
    
    # Compile report
    report = compile_interpretation_report(final_state)
    
    return report
```

## Observability Integration

```python
import os

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "emotion-interpretation"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

# All agent executions are automatically traced
# Access traces at: https://smith.langchain.com
```

## Error Handling

```python
from langgraph.errors import GraphInterrupt

try:
    result = await agent.ainvoke(state)
except GraphInterrupt as e:
    # Handle agent interruption
    logging.error(f"Agent interrupted: {e}")
    # Can resume from checkpoint
except Exception as e:
    # Handle other errors
    logging.error(f"Agent error: {e}")
    # Return partial results if available
```

## Testing

```python
def test_agent_with_example():
    """Test agent with Holmes example"""
    
    # Load example data
    with open("examples/transcription_holmes.json") as f:
        transcription = json.load(f)
    
    with open("examples/emotion_analysis_holmes.json") as f:
        emotions = json.load(f)
    
    # Run agent
    report = run_interpretation_agent(
        session_id="test_holmes",
        transcription_data=transcription,
        emotion_data=emotions
    )
    
    # Verify key moment detected
    assert any(
        "01:01" in m.timestampFormatted and m.significance == "critical"
        for m in report.keyMoments
    )
    
    # Verify deception insight
    assert any(
        i.type == "deceptive" and "Lord Alistair" in i.insight
        for i in report.insights
    )
```

## Next Steps

See:
- [05_TEMPORAL_ALIGNMENT.md](./05_TEMPORAL_ALIGNMENT.md) - Alignment algorithms
- [06_OBSERVABILITY.md](./06_OBSERVABILITY.md) - Monitoring and tracing
- [09_IMPLEMENTATION_GUIDE.md](./09_IMPLEMENTATION_GUIDE.md) - Implementation steps
