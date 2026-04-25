# github-sync Skill

## Purpose
Manages all version control interactions.

## Functionality
Monitors developer branches, handles PR creation/updates, and ensures code commits align with the Harness Hub workflow steps.

## Key Features

- **PR Monitoring:** Watches for new and updated pull requests
- **Automated Updates:** Updates PR status based on Harness Hub workflow
- **Branch Tracking:** Monitors development branches for changes
- **Commit Alignment:** Ensures commits align with workflow steps
- **Webhook Support:** Listens to GitHub webhooks for real-time updates

## API Reference

### GitHubSync

Main class for GitHub synchronization.

#### Methods

- `monitor_pr(owner: str, repo: str, pr_number: int) -> PRStatus`
  - Monitors a specific PR
  - Returns: PRStatus with current state and linked workflow

- `update_pr_status(owner: str, repo: str, pr_number: int, status: str, comment: str = None) -> bool`
  - Updates PR status comment
  - Returns: Success status

- `create_pr(owner: str, repo: str, title: str, body: str, head: str, base: str = "main") -> PR`
  - Creates a new PR
  - Returns: PR object with details

- `sync_branch(owner: str, repo: str, branch: str) -> bool`
  - Syncs a branch with latest changes
  - Returns: Success status

## Configuration

Set the following environment variables:

```
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=your_github_username
```

## Usage Example

```python
from github_sync import GitHubSync

syncer = GitHubSync(github_token="your-token")

# Monitor PR
status = syncer.monitor_pr("fintie", "my-project", 42)
print(f"PR status: {status.state}")

# Update PR status
syncer.update_pr_status(
    "fintie", "my-project", 42,
    status="In Progress",
    comment="Connected to Harness Hub job #123"
)
```

## Error Handling

- `GitHubAuthenticationError`: Authentication failed
- `GitHubConnectionError`: Connection failed
- `PRNotFoundError`: PR not found
- `BranchNotFoundError`: Branch not found

## Dependencies

- PyGithub
- requests
- pydantic
