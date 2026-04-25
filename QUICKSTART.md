# Quick Start Guide

## 5-Minute Setup

### 1. Clone the Repository

```bash
git clone https://github.com/fintie/ACP.git
cd ACP
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Credentials

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
# - HARNESS_API_KEY: Get from your Harness Hub account
# - GITHUB_TOKEN: Generate at github.com/settings/tokens
```

### 4. Run a Quick Test

```python
# Test the orchestrator
from taskflow_orchestrator import TaskflowOrchestrator

orchestrator = TaskflowOrchestrator()

# Process a PR (requires real repo and PR)
result = orchestrator.process_pr(
    repo_owner="your-username",
    repo_name="your-repo",
    pr_number=1
)

print(f"Workflow ID: {result.workflow_id}")
print(f"Job ID: {result.job_id}")
print(f"Status: {result.status}")
```

## Project Structure

```
ACP/
├── acp-connector/          # Harness Hub integration
│   ├── __init__.py
│   ├── SKILL.md           # Skill documentation
│   └── connector.py       # Main API connector
│
├── github-sync/           # GitHub integration
│   ├── __init__.py
│   ├── SKILL.md          # Skill documentation
│   └── sync.py           # GitHub operations
│
├── taskflow-orchestrator/ # Workflow orchestration
│   ├── __init__.py
│   ├── SKILL.md         # Skill documentation
│   └── orchestrator.py   # Main orchestrator
│
├── tests/               # Test suite
│   ├── test_acp_connector.py
│   ├── test_github_sync.py
│   └── test_orchestrator.py
│
├── docs/               # Documentation
│   ├── ARCHITECTURE.md
│   ├── CONFIGURATION.md
│   └── API.md
│
├── README.md          # Project overview
├── setup.py          # Package setup
├── requirements.txt  # Dependencies
└── .env.example     # Example env vars
```

## Common Tasks

### Run Tests

```bash
pytest tests/ -v
```

### Format Code

```bash
black .
```

### Check Linting

```bash
flake8 .
```

### Type Checking

```bash
mypy .
```

### Run Full CI Pipeline

```bash
# Format
black .

# Lint
flake8 .

# Type check
mypy .

# Run tests
pytest tests/ -v --cov=.
```

## Workflow Example

```python
from taskflow_orchestrator import TaskflowOrchestrator

# Initialize orchestrator
orchestrator = TaskflowOrchestrator()

# Process a PR from GitHub
result = orchestrator.process_pr(
    repo_owner="fintie",
    repo_name="my-project",
    pr_number=42
)

print(f"Workflow started: {result.workflow_id}")
print(f"Harness Job ID: {result.job_id}")

# Monitor workflow
status = orchestrator.get_workflow_status(result.workflow_id)
print(f"Current Status: {status.state}")
print(f"Progress: {status.progress}%")

# Retry if needed
if status.state == "FAILED":
    retry_result = orchestrator.retry_workflow(result.workflow_id)
    print(f"Retry started with job: {retry_result.job_id}")
```

## Direct Component Usage

### Using ACP Connector

```python
from acp_connector import ACPConnector

connector = ACPConnector(api_key="your-key")

# Submit a job
job_id = connector.submit_job(
    goal="Deploy to staging",
    context={"branch": "feature/ui-redesign"}
)

# Check status
status = connector.get_harness_status(job_id)
print(f"Job Status: {status.state} ({status.progress}%)")

# List jobs
jobs = connector.list_jobs(filters={"state": "running"})
for job in jobs:
    print(f"Job {job.job_id}: {job.goal}")

# Cancel job
connector.cancel_job(job_id)
```

### Using GitHub Sync

```python
from github_sync import GitHubSync

syncer = GitHubSync(github_token="your-token")

# Monitor PR
pr_status = syncer.monitor_pr("fintie", "my-repo", 42)
print(f"PR #{pr_status.pr_number}: {pr_status.title} ({pr_status.state})")

# Update PR with status
syncer.update_pr_status(
    "fintie", "my-repo", 42,
    status="In Progress",
    comment="Connected to Harness Hub. Job ID: job-123"
)

# Create PR
new_pr = syncer.create_pr(
    "fintie", "my-repo",
    title="Feature: New Dashboard",
    body="Added new dashboard component",
    head="feature/dashboard",
    base="main"
)
print(f"Created PR: {new_pr.url}")
```

## Troubleshooting

### "API key not provided" Error

```bash
# Make sure .env file is set up
cat .env | grep HARNESS_API_KEY
```

### "GitHub token not provided" Error

```bash
# Verify GitHub token is set
cat .env | grep GITHUB_TOKEN
```

### Connection Errors

```python
# Test connection manually
from acp_connector import ACPConnector

try:
    connector = ACPConnector()
    jobs = connector.list_jobs()
    print(f"Connected! Found {len(jobs)} jobs")
except Exception as e:
    print(f"Connection failed: {e}")
```

### PR Not Found

```bash
# Verify repo owner, repo name, and PR number are correct
# Format: owner=github-username, repo=repo-name, pr_number=<number>
```

## Getting Help

- 📖 See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- ⚙️ See [CONFIGURATION.md](docs/CONFIGURATION.md) for setup details
- 📚 See [API.md](docs/API.md) for API reference
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

## Next Steps

1. Set up your `.env` file with valid credentials
2. Run the test suite: `pytest tests/ -v`
3. Try the examples above
4. Integrate with your CI/CD pipeline
5. Check out the docs for advanced usage

---

**Ready to get started?** Clone the repo, configure your credentials, and run your first workflow!
