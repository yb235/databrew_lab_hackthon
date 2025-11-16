# Observability Specification

## Overview

This document describes the observability strategy for the Emotion Interpretation Machine, focusing on Track B (Glass Box) requirements from the Holistic AI hackathon. **LangSmith serves as the complete observability platform**, providing all necessary tracing, metrics, monitoring, and debugging capabilities.

## Observability Goals

1. **Complete Traceability**: Track every agent decision and reasoning step
2. **Human-Interpretable**: Clear visualizations and explanations
3. **Failure Analysis**: Identify exactly where and why issues occur
4. **Performance Monitoring**: Track metrics, costs, and bottlenecks
5. **Actionable Insights**: Use observability data to improve the system

## Observability Stack

### LangSmith - Complete Observability Platform

**Purpose**: Single, comprehensive platform for all observability needs

**Setup**:
```python
import os

# Enable LangSmith as the complete observability solution
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "emotion-interpretation-machine"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
```

**Complete Feature Set**:

1. **Execution Tracing**
   - Agent graph execution (all nodes)
   - LLM prompts and responses
   - Tool calls and results
   - State transitions
   - Nested operation tracking

2. **Performance Metrics**
   - Timing information for each operation
   - Latency analysis and bottleneck identification
   - Operation duration tracking
   - Throughput metrics

3. **Cost Tracking**
   - Token usage per LLM call
   - Cumulative token counts
   - Cost estimation and forecasting
   - Budget monitoring

4. **Error Tracking & Debugging**
   - Complete error traces with stack traces
   - Failed operation identification
   - Error pattern analysis
   - Root cause investigation tools

5. **Analytics & Insights**
   - Usage patterns over time
   - Performance trends
   - Success/failure rates
   - Optimization opportunities

6. **Custom Metadata**
   - Decision logging
   - Business metrics
   - Custom annotations
   - Audit trails

**Accessing Traces**:
```python
# Traces automatically available at:
# https://smith.langchain.com/projects/emotion-interpretation-machine

# Get trace URL programmatically
from langsmith import Client

client = Client()
trace_url = f"https://smith.langchain.com/traces/{trace_id}"
print(f"View trace at: {trace_url}")
```

## LangSmith Integration Patterns

### Decision Logging with LangSmith

```python
from langsmith import traceable
from datetime import datetime
import logging

# Standard Python logging (also captured in LangSmith)
logger = logging.getLogger(__name__)

class DecisionLogger:
    """Logs agent decisions for transparency"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.decisions = []
    
    @traceable(run_type="decision", name="log_decision")
    def log_decision(self, 
                     stage: str, 
                     input_data: dict, 
                     output_data: dict,
                     reasoning: str):
        """Log a decision point - automatically traced in LangSmith"""
        decision = {
            'timestamp': datetime.utcnow().isoformat(),
            'stage': stage,
            'input': input_data,
            'output': output_data,
            'reasoning': reasoning
        }
        self.decisions.append(decision)
        
        # Also log with Python logger
        logger.info(f"Decision: {stage}", extra=decision)
        
        return decision
    
    def get_decision_trail(self) -> List[dict]:
        """Get complete decision trail"""
        return self.decisions

# Usage in agent
decision_logger = DecisionLogger(session_id)

decision_logger.log_decision(
    stage='anomaly_detection',
    input_data={'event_id': event.id, 'emotions': event.emotions},
    output_data={'anomalies': anomalies},
    reasoning='Detected Fear spike at 01:01.300, deviates from Neutral baseline'
)
```

### Performance Profiling with LangSmith

```python
import time
from contextlib import contextmanager
from langsmith import traceable

class PerformanceProfiler:
    """Profile performance of each stage - integrated with LangSmith"""
    
    def __init__(self):
        self.timings = {}
    
    @contextmanager
    @traceable(run_type="performance", name="profile_operation")
    def profile(self, stage: str):
        """Context manager for profiling - automatically traced"""
        start = time.time()
        try:
            yield
        finally:
            duration = (time.time() - start) * 1000  # ms
            self.timings[stage] = duration
            
            # Automatically captured in LangSmith trace
            logger.info(f"{stage}: {duration:.2f}ms")
    
    def get_report(self) -> dict:
        """Get performance report"""
        return {
            'timings': self.timings,
            'total': sum(self.timings.values()),
            'bottleneck': max(self.timings.items(), key=lambda x: x[1])
        }

# Usage
profiler = PerformanceProfiler()

with profiler.profile('temporal_alignment'):
    aligned_events = align_emotion_with_transcript(transcription, emotions)

with profiler.profile('pattern_analysis'):
    patterns = analyze_emotion_patterns(aligned_events)

with profiler.profile('agent_interpretation'):
    report = await agent.ainvoke(state)

# Get report
perf_report = profiler.get_report()
print(f"Total time: {perf_report['total']:.2f}ms")
print(f"Bottleneck: {perf_report['bottleneck']}")
```

### Custom Metrics Tracking

```python
from langsmith import Client
from datetime import datetime

class MetricsTracker:
    """Track custom business metrics in LangSmith"""
    
    def __init__(self, project_name: str):
        self.client = Client()
        self.project_name = project_name
        self.metrics = {}
    
    def track_metric(self, name: str, value: float, unit: str = None, tags: dict = None):
        """Track a custom metric"""
        metric = {
            'name': name,
            'value': value,
            'unit': unit,
            'timestamp': datetime.utcnow().isoformat(),
            'tags': tags or {}
        }
        
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(metric)
        
        # Log for visibility
        logger.info(f"Metric: {name}={value} {unit or ''}", extra=metric)
    
    def get_metrics_summary(self) -> dict:
        """Get summary of all tracked metrics"""
        summary = {}
        for name, values in self.metrics.items():
            summary[name] = {
                'count': len(values),
                'latest': values[-1]['value'] if values else None,
                'average': sum(v['value'] for v in values) / len(values) if values else 0
            }
        return summary

# Usage
metrics = MetricsTracker('emotion-interpretation-machine')

# Track various metrics
metrics.track_metric('analysis_duration', duration_ms, 'milliseconds', 
                     {'session_id': session_id})
metrics.track_metric('aligned_events', len(aligned_events), 'count')
metrics.track_metric('anomalies_detected', len(anomalies), 'count')
metrics.track_metric('llm_tokens', token_count, 'tokens')
metrics.track_metric('estimated_cost', cost_usd, 'usd')

# Get summary
summary = metrics.get_metrics_summary()
```

## Visualization and Monitoring

### LangSmith Dashboard Features

LangSmith provides comprehensive built-in dashboards:

1. **Trace Explorer**
   - Visual execution graph
   - Node-by-node breakdown
   - Timing waterfall charts
   - Input/output inspection

2. **Runs Table**
   - List all executions
   - Filter by status, date, tags
   - Search capabilities
   - Export functionality

3. **Analytics Dashboard**
   - Success/failure rates
   - Performance trends over time
   - Cost tracking and forecasting
   - Token usage patterns

4. **Monitoring Alerts**
   - Error rate thresholds
   - Performance degradation
   - Cost budget alerts
   - Custom metric alerts

### Custom Dashboard Creation

```python
def create_interpretation_dashboard(session_id: str, report: InterpretationReport):
    """Create custom visualization dashboard data"""
    
    dashboard_data = {
        'session_id': session_id,
        'summary': {
            'title': report.summary.title,
            'confidence': report.summary.confidence,
            'main_themes': report.summary.mainThemes
        },
        'timeline': [
            {
                'timestamp': event.timestampFormatted,
                'type': event.type,
                'importance': event.importance,
                'description': event.description
            }
            for event in report.timeline
        ],
        'key_moments': [
            {
                'timestamp': moment.timestampFormatted,
                'speaker': moment.speaker,
                'emotion': moment.emotionDetected,
                'significance': moment.significance,
                'interpretation': moment.interpretation
            }
            for moment in report.keyMoments
        ],
        'speaker_profiles': {
            speaker: {
                'baseline': profile.emotionalBaseline,
                'credibility': profile.credibility,
                'patterns': profile.behavioralPatterns
            }
            for speaker, profile in report.speakerProfiles.items()
        },
        'observability': {
            'trace_url': report.observability.traceUrl,
            'metrics': report.observability.metrics
        }
    }
    
    return dashboard_data
```

## Debugging and Error Handling

### Error Tracing with LangSmith

```python
from langsmith import traceable
import logging

logger = logging.getLogger(__name__)

@traceable(run_type="chain", name="interpret_moment")
async def interpret_moment(moment: dict, context: dict):
    """Traceable interpretation function - errors automatically captured"""
    try:
        result = await llm.ainvoke(prompt)
        return result
    except Exception as e:
        # Error automatically captured in LangSmith trace with full context
        logger.error(f"Interpretation failed: {e}", extra={
            'moment': moment,
            'context': context,
            'error': str(e),
            'error_type': type(e).__name__
        })
        raise

# All exceptions are automatically captured in LangSmith traces
# with full stack traces and context
```

### Failure Analysis

```python
from langsmith import Client

class FailureAnalyzer:
    """Analyze failures for debugging using LangSmith"""
    
    def __init__(self):
        self.client = Client()
    
    def analyze_failure(self, trace_id: str):
        """Analyze what went wrong using LangSmith API"""
        
        # Get trace from LangSmith
        trace = self.client.read_run(trace_id)
        
        # Analyze failure
        context = {
            'run_id': trace.id,
            'status': trace.status,
            'error': trace.error,
            'inputs': trace.inputs,
            'outputs': trace.outputs,
            'duration_ms': trace.latency,
            'trace_url': f"https://smith.langchain.com/traces/{trace_id}"
        }
        
        # Log for review
        logger.error("Analysis failed", extra=context)
        
        return context
    
    def get_recent_failures(self, project_name: str, limit: int = 10):
        """Get recent failed runs from LangSmith"""
        runs = self.client.list_runs(
            project_name=project_name,
            filter='eq(status, "error")',
            limit=limit
        )
        
        failures = []
        for run in runs:
            failures.append({
                'id': run.id,
                'name': run.name,
                'error': run.error,
                'start_time': run.start_time,
                'trace_url': f"https://smith.langchain.com/traces/{run.id}"
            })
        
        return failures

# Usage
analyzer = FailureAnalyzer()

# Analyze specific failure
failure_context = analyzer.analyze_failure(trace_id)
print(f"Failure details: {failure_context}")
print(f"View trace at: {failure_context['trace_url']}")

# Get recent failures
recent_failures = analyzer.get_recent_failures('emotion-interpretation-machine')
for failure in recent_failures:
    print(f"Failed run: {failure['name']} - {failure['error']}")
    print(f"  View at: {failure['trace_url']}")
```

## Metrics Summary

### Key Metrics Tracked in LangSmith

All metrics are automatically captured and available in LangSmith:

| Metric | Type | Purpose | Auto-tracked |
|--------|------|---------|--------------|
| `ExecutionDuration` | Duration | Overall processing time | ✅ |
| `NodeDuration` | Duration | Per-node execution time | ✅ |
| `LLMCalls` | Count | Number of LLM invocations | ✅ |
| `LLMTokens` | Count | Total tokens used | ✅ |
| `LLMCost` | Cost | Estimated cost in USD | ✅ |
| `SuccessRate` | Percentage | Successful executions | ✅ |
| `ErrorRate` | Percentage | Failed executions | ✅ |
| `AlignedEvents` | Count | Custom: matched events | Manual |
| `AnomaliesDetected` | Count | Custom: unusual responses | Manual |
| `KeyMomentsIdentified` | Count | Custom: critical points | Manual |

### Alerting with LangSmith

LangSmith provides built-in monitoring and alerting:

```python
# Configure alerts in LangSmith UI:
# 1. Go to Project Settings > Monitoring
# 2. Set up alerts for:
#    - High error rate (>5%)
#    - Slow execution (>2 minutes)
#    - High cost (>$X per day)
#    - Custom metric thresholds

# Alerts can be delivered via:
# - Email
# - Slack
# - Webhook
# - PagerDuty
```

### Programmatic Monitoring

```python
from langsmith import Client
from datetime import datetime, timedelta

class SystemMonitor:
    """Monitor system health using LangSmith"""
    
    def __init__(self, project_name: str):
        self.client = Client()
        self.project_name = project_name
    
    def get_health_metrics(self, hours: int = 24):
        """Get system health metrics from last N hours"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Get all runs from last N hours
        runs = list(self.client.list_runs(
            project_name=self.project_name,
            start_time=since
        ))
        
        total_runs = len(runs)
        successful = sum(1 for r in runs if r.status == 'success')
        failed = sum(1 for r in runs if r.status == 'error')
        
        total_tokens = sum(
            (r.outputs or {}).get('token_usage', {}).get('total_tokens', 0)
            for r in runs
        )
        
        avg_duration = sum(
            r.latency for r in runs if r.latency
        ) / total_runs if total_runs > 0 else 0
        
        return {
            'period_hours': hours,
            'total_runs': total_runs,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total_runs if total_runs > 0 else 0,
            'error_rate': failed / total_runs if total_runs > 0 else 0,
            'total_tokens': total_tokens,
            'avg_duration_ms': avg_duration,
            'status': 'healthy' if failed / total_runs < 0.05 else 'degraded' if total_runs > 0 else 'unknown'
        }
    
    def check_health(self):
        """Quick health check"""
        metrics = self.get_health_metrics(hours=1)
        
        if metrics['error_rate'] > 0.1:
            logger.warning(f"High error rate: {metrics['error_rate']:.2%}")
        
        if metrics['avg_duration_ms'] > 120000:
            logger.warning(f"Slow execution: {metrics['avg_duration_ms']:.0f}ms average")
        
        return metrics

# Usage
monitor = SystemMonitor('emotion-interpretation-machine')
health = monitor.check_health()
print(f"System status: {health['status']}")
print(f"Success rate: {health['success_rate']:.2%}")
print(f"Error rate: {health['error_rate']:.2%}")
```

## Best Practices

1. **Always Enable Tracing**: Keep LangSmith enabled in all environments
2. **Log Decisions**: Every agent decision should be logged with reasoning using `@traceable`
3. **Track Performance**: Use context managers to profile each stage
4. **Monitor Costs**: Track token usage and costs via LangSmith dashboards
5. **Set Up Alerts**: Configure LangSmith monitoring alerts for critical thresholds
6. **Regular Reviews**: Review LangSmith traces weekly to improve prompts and logic
7. **User Feedback Loop**: Correlate user feedback with trace data for continuous improvement
8. **Tag Runs**: Use metadata and tags to categorize and filter runs
9. **Export Data**: Periodically export metrics for long-term analysis
10. **Document Patterns**: Document common failure patterns found in traces

## Integration with Report

```python
def add_observability_to_report(report: InterpretationReport, 
                                 trace_id: str,
                                 performance: PerformanceProfiler,
                                 decisions: DecisionLogger):
    """Add observability metadata to report"""
    
    # Get trace information from LangSmith
    client = Client()
    trace = client.read_run(trace_id)
    
    # Extract metrics from trace
    token_usage = trace.outputs.get('token_usage', {}) if trace.outputs else {}
    
    report.observability = ObservabilityMetrics(
        traceId=trace_id,
        traceUrl=f"https://smith.langchain.com/traces/{trace_id}",
        totalEvents=len(report.timeline),
        processedEvents=len(report.keyMoments),
        agentIterations=len(decisions.decisions),
        processingTime=performance.get_report(),
        decisionTrail=decisions.get_decision_trail(),
        metrics={
            'execution_duration_ms': trace.latency,
            'total_tokens': token_usage.get('total_tokens', 0),
            'prompt_tokens': token_usage.get('prompt_tokens', 0),
            'completion_tokens': token_usage.get('completion_tokens', 0),
            'estimated_cost_usd': estimate_cost(token_usage),
            'status': trace.status
        }
    )
    
    return report

def estimate_cost(token_usage: dict) -> float:
    """Estimate cost based on token usage"""
    # Claude 3.5 Sonnet pricing (example)
    input_cost_per_1k = 0.003  # $3 per 1M tokens
    output_cost_per_1k = 0.015  # $15 per 1M tokens
    
    prompt_tokens = token_usage.get('prompt_tokens', 0)
    completion_tokens = token_usage.get('completion_tokens', 0)
    
    cost = (prompt_tokens / 1000 * input_cost_per_1k + 
            completion_tokens / 1000 * output_cost_per_1k)
    
    return round(cost, 4)
```

## LangSmith API Reference

### Common Operations

```python
from langsmith import Client

client = Client()

# List runs with filters
runs = client.list_runs(
    project_name="emotion-interpretation-machine",
    filter='eq(status, "success")',  # or "error"
    limit=100
)

# Read specific run
run = client.read_run(run_id)

# Get run statistics
stats = client.get_run_stats(
    project_name="emotion-interpretation-machine",
    start_time=datetime.utcnow() - timedelta(days=7)
)

# Share trace publicly
shared_url = client.share_run(run_id)

# Add feedback to run
client.create_feedback(
    run_id=run_id,
    key="accuracy",
    score=0.9,
    comment="Excellent interpretation"
)
```

## Cost Optimization

### Token Usage Optimization

```python
@traceable(run_type="llm", name="optimized_llm_call")
async def call_llm_efficiently(prompt: str, context: str, max_tokens: int = 2000):
    """Optimized LLM call with token management"""
    
    # Truncate context if too long
    max_context_length = 1000
    if len(context) > max_context_length:
        context = context[:max_context_length] + "..."
    
    # Use shorter prompt when possible
    optimized_prompt = optimize_prompt(prompt)
    
    # Call LLM with conservative max_tokens
    response = await llm.ainvoke(
        optimized_prompt,
        max_tokens=max_tokens
    )
    
    return response

def optimize_prompt(prompt: str) -> str:
    """Remove unnecessary verbosity from prompt"""
    # Remove extra whitespace
    prompt = ' '.join(prompt.split())
    # Remove redundant instructions
    # ... other optimizations
    return prompt
```

### Monitoring Cost in Real-Time

```python
class CostMonitor:
    """Monitor and limit costs in real-time"""
    
    def __init__(self, daily_budget_usd: float = 10.0):
        self.daily_budget = daily_budget_usd
        self.client = Client()
    
    def check_budget(self, project_name: str) -> dict:
        """Check if within budget"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        
        runs = list(self.client.list_runs(
            project_name=project_name,
            start_time=today_start
        ))
        
        total_cost = sum(
            estimate_cost(r.outputs.get('token_usage', {}) if r.outputs else {})
            for r in runs
        )
        
        remaining = self.daily_budget - total_cost
        
        return {
            'budget': self.daily_budget,
            'spent': total_cost,
            'remaining': remaining,
            'within_budget': remaining > 0,
            'usage_percent': (total_cost / self.daily_budget * 100)
        }
    
    def should_proceed(self, project_name: str) -> bool:
        """Check if should proceed with operation"""
        budget_status = self.check_budget(project_name)
        
        if not budget_status['within_budget']:
            logger.warning(f"Budget exceeded: ${budget_status['spent']:.2f} / ${budget_status['budget']:.2f}")
            return False
        
        if budget_status['usage_percent'] > 90:
            logger.warning(f"Budget almost exceeded: {budget_status['usage_percent']:.1f}%")
        
        return True

# Usage
cost_monitor = CostMonitor(daily_budget_usd=10.0)

if cost_monitor.should_proceed('emotion-interpretation-machine'):
    # Proceed with analysis
    result = await agent.ainvoke(state)
else:
    # Budget exceeded
    raise Exception("Daily budget exceeded")
```

## Summary

**LangSmith provides everything needed for comprehensive observability:**
- ✅ Complete execution tracing
- ✅ Performance metrics and profiling
- ✅ Cost tracking and optimization
- ✅ Error debugging and analysis
- ✅ Custom metrics and logging
- ✅ Alerting and monitoring
- ✅ Analytics and insights
- ✅ Team collaboration features

**No additional observability tools required** - LangSmith is the single source of truth for all monitoring, debugging, and optimization needs.

## Next Steps

See:
- [07_DATA_FLOW.md](./07_DATA_FLOW.md) - End-to-end data flow
- [08_DEPLOYMENT.md](./08_DEPLOYMENT.md) - Production deployment
- [09_IMPLEMENTATION_GUIDE.md](./09_IMPLEMENTATION_GUIDE.md) - Implementation steps
