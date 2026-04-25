# taskflow-orchestrator Skill

## Purpose
The central logic layer that chains the connection and execution steps.

## Functionality
Takes a developer request, sequences calls to `acp-connector` and `github-sync`, handles error routing, and manages the state of the build flow.

## Key Features

- **Workflow Orchestration:** Chains multiple skills in the right order
- **State Management:** Tracks the state of the entire build flow
- **Error Handling:** Graceful error recovery and routing
- **Async Support:** Handles long-running operations
- **Logging & Monitoring:** Comprehensive logging and monitoring

## API Reference

### TaskflowOrchestrator

Main class for orchestrating workflows.

#### Methods

- `process_pr(repo_owner: str, repo_name: str, pr_number: int) -> WorkflowResult`
  - Process a PR and trigger Harness Hub workflow
  - Returns: WorkflowResult with job ID and status

- `get_workflow_status(workflow_id: str) -> WorkflowStatus`
  - Get current status of a workflow
  - Returns: WorkflowStatus object

- `retry_workflow(workflow_id: str) -> WorkflowResult`
  - Retry a failed workflow
  - Returns: New WorkflowResult

## Workflow States

1. **IDLE:** No workflow active
2. **PR_DETECTED:** PR detected and validation started
3. **CONNECTING:** Connecting to Harness Hub
4. **JOB_SUBMITTED:** Job submitted to Harness Hub
5. **RUNNING:** Workflow actively running
6. **COMPLETED:** Workflow completed successfully
7. **FAILED:** Workflow failed
8. **CANCELLED:** Workflow was cancelled

## Configuration

```
TASKFLOW_LOG_LEVEL=INFO
TASKFLOW_RETRY_ATTEMPTS=3
TASKFLOW_TIMEOUT=3600
```

## Usage Example

```python
from taskflow_orchestrator import TaskflowOrchestrator

orchestrator = TaskflowOrchestrator()

# Process a PR
result = orchestrator.process_pr(
    repo_owner="fintie",
    repo_name="my-project",
    pr_number=42
)

print(f"Workflow ID: {result.workflow_id}")
print(f"Job ID: {result.job_id}")
print(f"Status: {result.status}")

# Check status later
status = orchestrator.get_workflow_status(result.workflow_id)
print(f"Current status: {status.state}")
```

## Error Routing

- Connection errors: Retry with exponential backoff
- Job submission errors: Log and notify developer
- Sync errors: Update PR with error details

## Dependencies

- acp-connector
- github-sync
- requests
- pydantic
