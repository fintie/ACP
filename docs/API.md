# API Reference

## acp-connector API

### ACPConnector Class

```python
from acp_connector import ACPConnector

connector = ACPConnector(api_key="key", base_url="https://api.harness.io")
```

#### Methods

##### get_harness_status(job_id: str) -> JobStatus

Fetch the current status of a job from Harness Hub.

**Parameters:**
- `job_id` (str): The ID of the job to check

**Returns:**
- `JobStatus`: Object with job state, progress, and metadata

**Raises:**
- `ACPConnectionError`: If connection fails
- `ACPJobError`: If job not found

**Example:**
```python
status = connector.get_harness_status("job-123")
print(f"State: {status.state}")
print(f"Progress: {status.progress}%")
```

##### submit_job(goal: str, context: Dict) -> str

Submit a new job to the Harness Hub.

**Parameters:**
- `goal` (str): High-level goal for the job
- `context` (Dict): Additional context information

**Returns:**
- `str`: The submitted job ID

**Raises:**
- `ACPConnectionError`: If connection fails

**Example:**
```python
job_id = connector.submit_job(
    goal="Deploy to staging",
    context={"branch": "feature/new"}
)
```

##### cancel_job(job_id: str) -> bool

Cancel an active job.

**Parameters:**
- `job_id` (str): The job to cancel

**Returns:**
- `bool`: True if cancellation successful

##### list_jobs(filters: Dict = None) -> List[JobSummary]

List jobs with optional filtering.

**Parameters:**
- `filters` (Dict, optional): Filter criteria

**Returns:**
- `List[JobSummary]`: Matching jobs

---

## github-sync API

### GitHubSync Class

```python
from github_sync import GitHubSync

syncer = GitHubSync(github_token="token")
```

#### Methods

##### monitor_pr(owner: str, repo: str, pr_number: int) -> PRStatus

Monitor a specific pull request.

**Parameters:**
- `owner` (str): Repository owner
- `repo` (str): Repository name
- `pr_number` (int): PR number

**Returns:**
- `PRStatus`: Current PR status

**Example:**
```python
status = syncer.monitor_pr("fintie", "my-repo", 42)
print(f"PR #{status.pr_number}: {status.state}")
```

##### update_pr_status(owner: str, repo: str, pr_number: int, status: str, comment: str = None) -> bool

Update PR with status comment.

**Parameters:**
- `owner` (str): Repository owner
- `repo` (str): Repository name
- `pr_number` (int): PR number
- `status` (str): Status message
- `comment` (str, optional): Detailed comment

**Returns:**
- `bool`: True if update successful

##### create_pr(owner: str, repo: str, title: str, body: str, head: str, base: str = "main") -> PR

Create a new pull request.

**Parameters:**
- `owner` (str): Repository owner
- `repo` (str): Repository name
- `title` (str): PR title
- `body` (str): PR description
- `head` (str): Head branch
- `base` (str): Base branch (default: main)

**Returns:**
- `PR`: Created PR object

##### sync_branch(owner: str, repo: str, branch: str) -> bool

Sync a branch with latest changes.

**Parameters:**
- `owner` (str): Repository owner
- `repo` (str): Repository name
- `branch` (str): Branch to sync

**Returns:**
- `bool`: True if sync successful

---

## taskflow-orchestrator API

### TaskflowOrchestrator Class

```python
from taskflow_orchestrator import TaskflowOrchestrator

orchestrator = TaskflowOrchestrator()
```

#### Methods

##### process_pr(repo_owner: str, repo_name: str, pr_number: int) -> WorkflowResult

Process a GitHub PR and trigger Harness Hub workflow.

**Parameters:**
- `repo_owner` (str): Repository owner
- `repo_name` (str): Repository name
- `pr_number` (int): PR number

**Returns:**
- `WorkflowResult`: Workflow execution result

**Raises:**
- `OrchestrationError`: If orchestration fails

**Example:**
```python
result = orchestrator.process_pr("fintie", "my-repo", 42)
print(f"Workflow ID: {result.workflow_id}")
print(f"Job ID: {result.job_id}")
print(f"Status: {result.status}")
```

##### get_workflow_status(workflow_id: str) -> WorkflowStatus

Get current status of a workflow.

**Parameters:**
- `workflow_id` (str): The workflow ID

**Returns:**
- `WorkflowStatus`: Current workflow status

**Example:**
```python
status = orchestrator.get_workflow_status("repo/my-repo/pr-42")
print(f"State: {status.state}")
print(f"Progress: {status.progress}%")
```

##### retry_workflow(workflow_id: str) -> WorkflowResult

Retry a failed workflow.

**Parameters:**
- `workflow_id` (str): The workflow ID to retry

**Returns:**
- `WorkflowResult`: New workflow execution result

---

## Data Models

### JobStatus
```python
class JobStatus(BaseModel):
    job_id: str
    state: str
    progress: int  # 0-100
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
```

### PRStatus
```python
class PRStatus(BaseModel):
    pr_number: int
    title: str
    state: str
    author: str
    created_at: datetime
    harness_job_id: Optional[str]
    workflow_status: Optional[str]
```

### WorkflowStatus
```python
class WorkflowStatus(BaseModel):
    workflow_id: str
    state: WorkflowState
    pr_number: int
    job_id: Optional[str]
    progress: int
    message: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### WorkflowResult
```python
class WorkflowResult(BaseModel):
    workflow_id: str
    job_id: str
    status: WorkflowState
    pr_number: int
    created_at: datetime
    message: Optional[str]
```

---

## Error Handling

### Exception Hierarchy

```
Exception
├── ACPAuthenticationError
├── ACPConnectionError
├── ACPJobError
├── GitHubAuthenticationError
├── GitHubConnectionError
├── PRNotFoundError
├── BranchNotFoundError
└── OrchestrationError
```

### Error Example

```python
try:
    status = connector.get_harness_status("invalid-id")
except ACPJobError as e:
    print(f"Job error: {e}")
except ACPConnectionError as e:
    print(f"Connection error: {e}")
except ACPAuthenticationError as e:
    print(f"Auth error: {e}")
```

---

## Rate Limiting

All APIs are rate-limited. Check headers for:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

Implement backoff when approaching limits:

```python
import time
import requests

def make_request_with_backoff(url, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url)
        
        if response.status_code == 429:  # Too Many Requests
            wait_time = int(response.headers.get('Retry-After', 60))
            time.sleep(wait_time)
            continue
            
        return response
    
    raise Exception("Max retries exceeded")
```
