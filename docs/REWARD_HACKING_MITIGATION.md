# Reward Hacking Mitigation Guide

## Overview

Reward hacking is a critical challenge in reinforcement learning and automated systems where agents exploit weaknesses in reward functions to maximize returns without genuinely completing intended tasks. The ACP platform integrates comprehensive mitigation strategies to detect and prevent reward hacking.

## Problem Statement

### What is Reward Hacking?

Reward hacking occurs when a system achieves high rewards without actually accomplishing the underlying objective. Examples include:

- **Metric Inflation:** Reporting high accuracy while performing minimal actual work
- **Action Loops:** Repeating trivial actions to accumulate rewards
- **State Manipulation:** Falsifying system state without real changes
- **Loophole Exploitation:** Leveraging unintended reward function weaknesses
- **Constraint Violations:** Maximizing rewards while breaking safety constraints

### Impact

Reward hacking undermines:
- Task reliability and correctness
- Safety and compliance
- Ethical alignment
- System trustworthiness
- Production stability

## ACP Reward Validation System

### Architecture

The ACP platform integrates `reward-validator` skill into the orchestration pipeline:

```
Job Execution
    ↓
Result Collection (actions, state, metrics)
    ↓
Reward Validator
    ├─ Iterative Testing
    ├─ Adversarial Checks
    ├─ Behavioral Robustness
    └─ Ethical Compliance
    ↓
Validation Result (Safe/Suspicious)
    ↓
Human Review (if needed)
    ↓
Approval or Rejection
```

### Four-Pillar Defense Strategy

#### 1. Iterative Reward Testing

**Purpose:** Validate consistency of reward signals across multiple scenarios

**Method:**
- Test baseline job performance
- Generate scenario variants with controlled variations
- Compare reward signals for consistency
- Detect anomalies and spikes

**Metrics:**
- Consistency Score: 0-1 measure of reward signal stability
- Anomaly Count: Number of suspicious deviations detected
- Variance Analysis: Statistical spread of rewards

**Example:**
```python
validator = RewardValidator()
report = validator.iterative_test(
    baseline=[baseline_job_result],
    variants=[variant1, variant2, variant3]
)
print(f"Consistency: {report.consistency_score}")
if report.anomalies_detected:
    print("Suspicious patterns found!")
```

#### 2. Adversarial Validation

**Purpose:** Identify potential exploitation patterns and vulnerabilities

**Checks:**
- **Metric Inflation Detection:** High reported rewards with low task progress
- **Action Spam Detection:** Excessive actions for the task scope
- **State Integrity Verification:** Detect unchanged or suspicious states
- **Boundary Testing:** Check behavior at constraint boundaries

**Metrics:**
- Exploitation Risk: 0-1 probability of reward hacking
- Vulnerability Count: Number of identified issues
- Severity Classification: High/Medium/Low risk levels

**Example:**
```python
report = validator.adversarial_check(job_result)
if report.exploitation_risk > 0.5:
    print("High exploitation risk detected!")
    for exploit in report.potential_exploits:
        print(f"  - {exploit}")
```

#### 3. Behavioral Robustness Checking

**Purpose:** Ensure solutions generalize beyond training scenarios

**Tests:**
- **Noise Robustness:** Performance under noisy conditions
- **Scenario Variation:** Success across different contexts
- **Edge Case Handling:** Performance at domain boundaries
- **Generalization:** Applicability to unseen scenarios

**Metrics:**
- Success Rate: Percentage of scenarios passed
- Generalization Score: Likelihood of working in production
- Failure Modes: Specific scenarios where performance degrades

**Example:**
```python
scenarios = [
    {"variation": "baseline", "noise": 0},
    {"variation": "noisy", "noise": 0.2},
    {"variation": "extreme", "noise": 0.4},
]
report = validator.behavioral_robustness_check(
    job_result, scenarios
)
print(f"Success rate: {report.success_rate:.0%}")
```

#### 4. Ethical Compliance Checking

**Purpose:** Validate adherence to business rules and ethical constraints

**Constraints:**
- Task Goal Alignment: Does completion match the objective?
- Resource Efficiency: Are resources used appropriately?
- Safety Compliance: Are safety requirements met?
- Fairness Metrics: Is the solution fair and unbiased?

**Metrics:**
- Compliance Score: 0-1 adherence to constraints
- Ethical Alignment: Ethical soundness of solution
- Violation Count: Number of constraint breaches

**Example:**
```python
report = validator.ethical_compliance_check(
    job_result,
    constraints=[
        "task_goal_alignment",
        "safety_compliance",
        "resource_efficiency"
    ]
)
if report.violations:
    for violation in report.violations:
        print(f"Constraint violation: {violation}")
```

### Human-in-the-Loop Integration

The system supports human feedback for difficult cases:

```python
feedback = validator.human_feedback_loop(
    job_result,
    human_feedback="Task completed correctly"
)

if feedback.approval_status == "approved":
    print("Human validation confirms completion")
elif feedback.approval_status == "needs_review":
    print("Human review recommended")
else:
    print("Human rejected completion")
```

## Integration with TaskflowOrchestrator

### Basic Usage

```python
from taskflow_orchestrator import TaskflowOrchestrator

orchestrator = TaskflowOrchestrator(
    enable_reward_validation=True,
    validation_threshold=0.85  # 85% confidence required
)

# Process PR and execute job
result = orchestrator.process_pr("owner", "repo", 42)

# Later, validate rewards after job completes
validation = orchestrator.validate_job_rewards(
    job_id=result.job_id,
    task_goal="Deploy to staging",
    completed_actions=[...],
    final_state={...},
    metrics={"accuracy": 0.95, "latency": 120},
    execution_time=45.5
)

if validation["approved"]:
    print(f"✓ Approved (safety: {validation['safety_score']:.2f})")
else:
    print(f"✗ Rejected - suspicious patterns detected")
```

### Configuration

```python
# High security mode (strict validation)
orchestrator = TaskflowOrchestrator(
    enable_reward_validation=True,
    validation_threshold=0.95  # Very strict
)

# Medium security mode
orchestrator = TaskflowOrchestrator(
    enable_reward_validation=True,
    validation_threshold=0.85  # Balanced
)

# Low security mode (permissive)
orchestrator = TaskflowOrchestrator(
    enable_reward_validation=True,
    validation_threshold=0.70  # Permissive
)

# Validation disabled (not recommended)
orchestrator = TaskflowOrchestrator(
    enable_reward_validation=False
)
```

## Validation Result Interpretation

### Safety Score

- **0.95-1.0:** Excellent - Very high confidence in genuine completion
- **0.85-0.94:** Good - High confidence, minimal concerns
- **0.70-0.84:** Acceptable - Some concerns, human review recommended
- **0.50-0.69:** Suspicious - Multiple red flags, needs investigation
- **0.0-0.49:** Critical - Strong evidence of reward hacking

### Risk Levels

- **SAFE:** Passes all validation checks
- **CAUTION:** Minor issues detected, monitoring recommended
- **SUSPICIOUS:** Multiple indicators of potential hacking
- **CRITICAL:** Strong evidence of reward hacking detected

### Interpreting Warnings

Common warnings and their meanings:

| Warning | Meaning | Action |
|---------|---------|--------|
| "High metrics but low task progress" | Metric inflation likely | Review reward function |
| "Excessive actions for task" | Action spam detected | Analyze action sequence |
| "Low task completion rate" | Insufficient progress | Investigate completion logic |
| "Poor performance under noise" | Lack of robustness | Test generalization |
| "Constraint violations detected" | Rules broken | Review safety checks |

## Case Studies

### Case 1: Metric Inflation Detection

**Scenario:** Job reports 99% accuracy but deploys no actual changes

```python
job_result = JobResult(
    job_id="job-001",
    task_goal="Deploy new feature",
    completed_actions=[{"action": "echo", "status": "success"}],  # Dummy action
    final_state={},  # Empty final state
    metrics={"accuracy": 0.99},  # High metrics
    execution_time=0.1  # Very fast
)

validation = validator.validate_reward(job_result, {"accuracy": 0.99})

# Result: SUSPICIOUS (high metrics, low actual work)
# Warning: "High metrics but low task progress"
```

**Mitigation:** Rewrite reward function to include deployment verification

### Case 2: Action Loop Detection

**Scenario:** Job completes trivial action 200 times

```python
job_result = JobResult(
    job_id="job-002",
    task_goal="Build application",
    completed_actions=[{"action": "noop"} for _ in range(200)],
    final_state={"builds": 0},
    metrics={"reward": 200},  # High reward from loop
    execution_time=1.0
)

validation = validator.validate_reward(job_result, {"reward": 200})

# Result: SUSPICIOUS (action spam, no real progress)
# Warning: "Potential action looping or spam"
```

**Mitigation:** Add action diversity check, limit repetition

### Case 3: Safe Completion

**Scenario:** Job genuinely completes deployment

```python
job_result = JobResult(
    job_id="job-003",
    task_goal="Deploy to staging",
    completed_actions=[
        {"action": "build", "status": "success"},
        {"action": "test", "status": "success"},
        {"action": "deploy", "status": "success"}
    ],
    final_state={
        "deployment": "active",
        "status": "healthy",
        "version": "v1.2.3"
    },
    metrics={"accuracy": 0.95, "latency": 120},
    execution_time=45.5
)

validation = validator.validate_reward(job_result, {...})

# Result: SAFE (consistent, genuine progress, all checks pass)
```

## Best Practices

### 1. Design Robust Reward Functions

- Align rewards directly with objectives
- Include outcome verification
- Avoid exploitable loopholes
- Test edge cases thoroughly

### 2. Set Appropriate Thresholds

- Use context-dependent thresholds
- Higher thresholds for critical tasks
- Lower thresholds for benign operations
- Adjust based on experience

### 3. Monitor and Iterate

- Track validation results over time
- Analyze false positives/negatives
- Refine checks based on learnings
- Share insights across team

### 4. Combine Multiple Signals

- Don't rely on single metric
- Use diverse validation checks
- Cross-validate results
- Include human judgment

### 5. Document Decisions

- Record validation reasoning
- Explain approval/rejection decisions
- Maintain audit trail
- Enable post-mortems

## Troubleshooting

### Issue: Too Many False Positives

**Cause:** Validation threshold too strict

**Solution:**
```python
# Lower threshold for your use case
orchestrator = TaskflowOrchestrator(
    validation_threshold=0.75  # Instead of 0.85
)
```

### Issue: Bypassing Legitimate Work

**Cause:** Reward function penalizes valid approaches

**Solution:**
```python
# Review and update reward signals
# Add legitimate action patterns to whitelist
```

### Issue: Performance Degradation

**Cause:** Validation consuming too many resources

**Solution:**
```python
# Disable for non-critical jobs
# Cache validation results
# Sample for large workflows
```

## References

- Amodei et al. "Concrete Problems in AI Safety" (2016)
- Krakovna et al. "Specification Gaming" (2020)
- Leike et al. "AI Safety Gridworlds" (2017)
- Hadfield-Menell et al. "Cooperative Inverse Reinforcement Learning" (2016)

## Advanced: Custom Validators

You can extend the reward validator with custom checks:

```python
class CustomValidator(RewardValidator):
    def custom_check(self, job_result):
        """Your domain-specific validation."""
        # Custom logic here
        return custom_score

    def validate_reward(self, job_result, reward_signals):
        """Override to include custom checks."""
        # Get base validation
        result = super().validate_reward(job_result, reward_signals)
        
        # Add custom check
        custom_score = self.custom_check(job_result)
        result.detailed_analysis["custom_check"] = custom_score
        
        return result
```

---

**For more information, see:**
- [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - System design
- [CONFIGURATION.md](../docs/CONFIGURATION.md) - Setup guide
- [API.md](../docs/API.md) - API reference
- [reward-validator SKILL.md](../reward-validator/SKILL.md) - Validator details
