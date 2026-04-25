# ACP Architecture

## System Overview

The ACP Harness Hub Connector Platform is built on a modular, three-tier architecture that seamlessly connects GitHub development workflows with the ACP Harness Hub.

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Actions                         │
│              (Commits, PRs, Branch Updates)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │  GitHub (Version Control)     │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │  taskflow-orchestrator        │
         │  (Central Logic & Routing)    │
         └──┬──────────────────────────┬─┘
            │                          │
    ┌───────▼──────────┐   ┌──────────▼─────────┐
    │ acp-connector    │   │   github-sync      │
    │ (Harness Hub)    │   │ (Version Control)  │
    └──────────────────┘   └────────────────────┘
            │                          │
    ┌───────▼──────────┐   ┌──────────▼─────────┐
    │ Harness Hub API  │   │   GitHub API       │
    │ (Build/Deploy)   │   │ (PR/Branch Mgmt)   │
    └──────────────────┘   └────────────────────┘
```

## Component Architecture

### 1. acp-connector

**Responsibility:** Direct communication with ACP Harness Hub

**Key Classes:**
- `ACPConnector`: Main interface for Harness Hub interactions
- `JobStatus`: Represents job execution state
- `JobSummary`: Summary information for jobs

**Capabilities:**
- Authentication and API key management
- Job submission and tracking
- Status monitoring
- Error handling with retry logic

**Exception Hierarchy:**
- `ACPAuthenticationError`: Auth failures
- `ACPConnectionError`: Network issues
- `ACPJobError`: Job-specific errors

### 2. github-sync

**Responsibility:** GitHub version control synchronization

**Key Classes:**
- `GitHubSync`: Main interface for GitHub operations
- `PRStatus`: Pull request status information
- `PR`: Pull request details

**Capabilities:**
- PR monitoring and creation
- Branch tracking
- Status updates and comments
- Webhook support (extensible)

**Exception Hierarchy:**
- `GitHubAuthenticationError`: Auth failures
- `GitHubConnectionError`: Network issues
- `PRNotFoundError`: PR lookup failures
- `BranchNotFoundError`: Branch lookup failures

### 3. taskflow-orchestrator

**Responsibility:** Central orchestration and workflow management

**Key Classes:**
- `TaskflowOrchestrator`: Main orchestration engine
- `WorkflowStatus`: Workflow execution state
- `WorkflowResult`: Workflow execution result

**Workflow States:**
```
IDLE → PR_DETECTED → CONNECTING → JOB_SUBMITTED → RUNNING → COMPLETED
                                                              ↓
                                                           FAILED
                                                             ↓
                                                          CANCELLED
```

**Capabilities:**
- Workflow orchestration between skills
- State management and persistence
- Error routing and recovery
- Logging and monitoring
- Retry mechanisms

## Data Flow

### Proactive PR Connection Workflow

```
1. Developer commits and opens PR
   ↓
2. GitHub webhook triggers (or polling detects)
   ↓
3. taskflow-orchestrator receives event
   ↓
4. github-sync validates PR details
   ↓
5. acp-connector submits job to Harness Hub
   ↓
6. github-sync updates PR with job status
   ↓
7. taskflow-orchestrator monitors both systems
   ↓
8. Results synchronized back to GitHub
```

## Communication Patterns

### Synchronous Flow
- PR is detected
- Job is immediately submitted
- Status is immediately available

### Asynchronous Monitoring
- Workflow state is tracked
- Job status is polled periodically
- PR is updated with progress

## Error Recovery

1. **Connection Errors:** Exponential backoff retry
2. **Authentication Errors:** Logged and escalated
3. **Job Submission Errors:** Logged to PR with details
4. **Sync Errors:** Graceful degradation, retry on next cycle

## Extensibility

The architecture supports:
- Custom workflow steps
- Additional skill modules
- Webhook handlers
- Custom status reporters
- Integration with other systems

## Configuration Management

Environment variables control:
- API credentials
- Endpoint URLs
- Logging levels
- Retry policies
- Timeouts

## Security Considerations

- API keys stored in environment variables
- No credentials in logs or version control
- All communications use HTTPS
- Token-based authentication
- Input validation on all API endpoints
