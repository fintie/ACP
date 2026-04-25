# taskflow-orchestrator Skill

## Purpose
The central logic layer that chains the connection and execution steps, with integrated reward hacking mitigation.

## Functionality
Takes a developer request, sequences calls to `acp-connector`, `github-sync`, and `reward-validator`, handles error routing, manages workflow state, and validates reward signals for genuine task completion.

## Key Features

- **Workflow Orchestration:** Chains multiple skills in the right order
- **Reward Validation:** Detects and mitigates reward hacking attempts
- **State Management:** Tracks the state of the entire build flow
- **Error Handling:** Graceful error recovery and routing
- **Async Support:** Handles long-running operations
- **Logging & Monitoring:** Comprehensive logging and monitoring
- **Safety-First Design:** All completions validated before approval

## API Reference

### TaskflowOrchestrator

Main class for orchestrating workflows with reward validation.

#### Methods

- `process_pr(repo_owner: str, repo_name: str, pr_number: int) -> WorkflowResult`
  - Process a PR and trigger Harness Hub workflow with reward validation
  - Returns: WorkflowResult with job ID and status

- `validate_job_rewards(job_id: str, task_goal: str, completed_actions: list, final_state: dict, metrics: dict, execution_time: float) -> Dict`
  - Comprehensive reward hacking mitigation and validation
  - Returns: Validation result with safety assessment

- `get_workflow_status(workflow_id: str) -> WorkflowStatus`
  - Get current status of a workflow
  - Returns: WorkflowStatus object

- `retry_workflow(workflow_id: str) -> WorkflowResult`
  - Retry a failed workflow
  - Returns: New WorkflowResult

## Workflow States with Validation

```
IDLE 
  ↓
PR_DETECTED (github-sync monitors PR)
  ↓
CONNECTING (acp-connector prepares job)
  ↓
JOB_SUBMITTED (job sent to Harness Hub)
  ↓
RUNNING (job executes)
  ↓
VALIDATION (reward-validator checks for hacking)
  ↓
COMPLETED (✓ validated) or FAILED (✗ suspicious)
```

## Reward Hacking Mitigation

The orchestrator integrates four-pillar reward hacking defense:

1. **Iterative Reward Testing:** Validates consistency across scenarios
2. **Adversarial Validation:** Identifies exploitation patterns
3. **Behavioral Robustness:** Tests generalization
4. **Ethical Compliance:** Ensures constraint adherence

## Configuration

```
TASKFLOW_LOG_LEVEL=INFO
TASKFLOW_RETRY_ATTEMPTS=3
TASKFLOW_TIMEOUT=3600
REWARD_VALIDATION_ENABLED=true
REWARD_VALIDATOR_THRESHOLD=0.85
HUMAN_VALIDATION_REQUIRED=true
```

## Usage Example

```python
from taskflow_orchestrator import TaskflowOrchestrator

orchestrator = TaskflowOrchestrator(
    enable_reward_validation=True,
    validation_threshold=0.85
)

# Process a PR
result = orchestrator.process_pr(
    repo_owner="fintie",
    repo_name="my-project",
    pr_number=42
)

# After job completion, validate rewards
validation = orchestrator.validate_job_rewards(
    job_id=result.job_id,
    task_goal="Deploy to staging",
    completed_actions=[...],
    final_state={...},
    metrics={"accuracy": 0.95, "latency": 120},
    execution_time=45.5
)

if validation["approved"]:
    print(f"✓ Job approved (safety: {validation['safety_score']:.2f})")
else:
    print(f"✗ Suspicious patterns detected")
    for warning in validation["warnings"]:
        print(f"  - {warning}")
```

## Safety Guarantees

- **No Reward Inflation:** Detects high rewards with low task progress
- **Action Loop Detection:** Identifies spam or looping patterns
- **State Integrity:** Verifies genuine state changes
- **Constraint Compliance:** Ensures business rules followed
- **Generalization Testing:** Confirms solution robustness

## Metrics Tracked

- **Safety Score:** 0-1 confidence in genuine completion
- **Exploitation Risk:** Probability of reward hacking
- **Consistency Score:** Reward signal stability
- **Generalization Score:** Performance generalization
- **Compliance Score:** Constraint adherence

## Integration with Other Skills

```
GitHub PR Event
    ↓
github-sync (monitor PR)
    ↓
acp-connector (submit job to Harness)
    ↓
[Job Execution]
    ↓
reward-validator (check for hacking)
    ↓
Update PR with validated results
```

## Dependencies

- acp-connector
- github-sync
- reward-validator
- requests
- pydantic

