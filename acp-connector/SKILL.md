# acp-connector Skill

## Purpose
Direct, secure communication with the ACP Harness Hub API.

## Functionality
Authenticates developer requests, translates high-level goals into Harness Hub jobs, and fetches real-time status.

## Key Features

- **Secure Authentication:** Handles API key management and OAuth flows
- **Job Translation:** Converts developer requests into Harness Hub compatible jobs
- **Real-time Status:** Fetches and caches job status information
- **Error Handling:** Graceful error handling with retry logic
- **Async Support:** Supports both sync and async operations

## API Reference

### ACPConnector

Main class for interacting with the Harness Hub API.

#### Methods

- `get_harness_status(job_id: str) -> JobStatus`
  - Fetches the current status of a job
  - Returns: JobStatus object with state, progress, and metadata

- `submit_job(goal: str, context: Dict) -> str`
  - Submits a new job to the Harness Hub
  - Returns: Job ID for tracking

- `cancel_job(job_id: str) -> bool`
  - Cancels an active job
  - Returns: Success status

- `list_jobs(filters: Dict = None) -> List[JobSummary]`
  - Lists all jobs matching optional filters
  - Returns: List of JobSummary objects

## Configuration

Set the following environment variables:

```
HARNESS_API_KEY=your_api_key
HARNESS_API_URL=https://api.harness.io
```

## Usage Example

```python
from acp_connector import ACPConnector

connector = ACPConnector(api_key="your-key")

# Submit a job
job_id = connector.submit_job(
    goal="Build and deploy to staging",
    context={"branch": "feature/new-ui"}
)

# Check status
status = connector.get_harness_status(job_id)
print(f"Job {job_id} status: {status.state}")
```

## Error Handling

The connector raises specific exceptions:

- `ACPAuthenticationError`: Authentication failed
- `ACPConnectionError`: Connection to Harness Hub failed
- `ACPJobError`: Job execution failed

## Dependencies

- requests
- httpx
- pydantic