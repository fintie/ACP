"""Taskflow orchestrator module for central workflow orchestration."""

import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import sys

# Import the other skills
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from acp_connector import ACPConnector
from github_sync import GitHubSync


class WorkflowState(str, Enum):
    """Enumeration of workflow states."""

    IDLE = "IDLE"
    PR_DETECTED = "PR_DETECTED"
    CONNECTING = "CONNECTING"
    JOB_SUBMITTED = "JOB_SUBMITTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WorkflowResult(BaseModel):
    """Model for workflow execution result."""

    workflow_id: str
    job_id: str
    status: WorkflowState
    pr_number: int
    created_at: datetime
    message: Optional[str] = None


class WorkflowStatus(BaseModel):
    """Model for workflow status information."""

    workflow_id: str
    state: WorkflowState
    pr_number: int
    job_id: Optional[str] = None
    progress: int = 0
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class OrchestrationError(Exception):
    """Raised when orchestration fails."""

    pass


class TaskflowOrchestrator:
    """Main class for orchestrating workflows between ACP and GitHub."""

    def __init__(
        self,
        acp_api_key: Optional[str] = None,
        github_token: Optional[str] = None,
        log_level: str = "INFO",
    ):
        """
        Initialize the Taskflow Orchestrator.

        Args:
            acp_api_key: ACP API key. If not provided, reads from HARNESS_API_KEY.
            github_token: GitHub token. If not provided, reads from GITHUB_TOKEN.
            log_level: Logging level.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, log_level))

        self.connector = ACPConnector(api_key=acp_api_key)
        self.syncer = GitHubSync(github_token=github_token)

        # In-memory workflow state tracking
        self.workflows: Dict[str, WorkflowStatus] = {}

    def process_pr(
        self, repo_owner: str, repo_name: str, pr_number: int
    ) -> WorkflowResult:
        """
        Process a GitHub PR and trigger Harness Hub workflow.

        Args:
            repo_owner: Repository owner.
            repo_name: Repository name.
            pr_number: Pull request number.

        Returns:
            WorkflowResult: Result of the workflow execution.

        Raises:
            OrchestrationError: If orchestration fails.
        """
        workflow_id = f"{repo_owner}/{repo_name}/pr-{pr_number}"
        self.logger.info(f"Starting workflow {workflow_id}")

        try:
            # Step 1: Detect PR
            self.logger.debug(f"Detecting PR #{pr_number}")
            pr_status = self.syncer.monitor_pr(repo_owner, repo_name, pr_number)
            self._update_workflow_state(
                workflow_id, WorkflowState.PR_DETECTED, pr_number
            )

            # Step 2: Connect to Harness Hub
            self.logger.debug("Connecting to Harness Hub")
            self._update_workflow_state(
                workflow_id, WorkflowState.CONNECTING, pr_number
            )

            # Step 3: Submit job
            self.logger.debug("Submitting job to Harness Hub")
            job_id = self.connector.submit_job(
                goal=pr_status.title,
                context={
                    "repo_owner": repo_owner,
                    "repo_name": repo_name,
                    "pr_number": pr_number,
                    "author": pr_status.author,
                },
            )

            self._update_workflow_state(
                workflow_id, WorkflowState.JOB_SUBMITTED, pr_number, job_id
            )

            # Step 4: Update PR with status
            self.logger.debug(f"Updating PR with job ID {job_id}")
            self.syncer.update_pr_status(
                repo_owner,
                repo_name,
                pr_number,
                "Connected to Harness Hub",
                f"Job ID: {job_id}\nThis PR has been connected to the Harness Hub workflow.",
            )

            # Step 5: Mark as running
            self._update_workflow_state(workflow_id, WorkflowState.RUNNING, pr_number, job_id)

            result = WorkflowResult(
                workflow_id=workflow_id,
                job_id=job_id,
                status=WorkflowState.RUNNING,
                pr_number=pr_number,
                created_at=datetime.utcnow(),
                message="Workflow started successfully",
            )

            self.logger.info(f"Workflow {workflow_id} started with job {job_id}")
            return result

        except Exception as e:
            self.logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            self._update_workflow_state(
                workflow_id, WorkflowState.FAILED, pr_number, message=str(e)
            )
            raise OrchestrationError(f"Failed to process PR: {str(e)}")

    def get_workflow_status(self, workflow_id: str) -> WorkflowStatus:
        """
        Get the current status of a workflow.

        Args:
            workflow_id: The workflow ID.

        Returns:
            WorkflowStatus: The current status.

        Raises:
            OrchestrationError: If workflow not found.
        """
        if workflow_id not in self.workflows:
            raise OrchestrationError(f"Workflow {workflow_id} not found")

        status = self.workflows[workflow_id]

        # If job is submitted, fetch real-time status from Harness Hub
        if status.job_id and status.state in [
            WorkflowState.RUNNING,
            WorkflowState.JOB_SUBMITTED,
        ]:
            try:
                job_status = self.connector.get_harness_status(status.job_id)
                status.progress = job_status.progress

                # Update state based on job status
                if job_status.state == "completed":
                    status.state = WorkflowState.COMPLETED
                elif job_status.state == "failed":
                    status.state = WorkflowState.FAILED
                elif job_status.state == "running":
                    status.state = WorkflowState.RUNNING

                status.updated_at = datetime.utcnow()

            except Exception as e:
                self.logger.warning(f"Failed to fetch job status: {str(e)}")

        return status

    def retry_workflow(self, workflow_id: str) -> WorkflowResult:
        """
        Retry a failed workflow.

        Args:
            workflow_id: The workflow ID to retry.

        Returns:
            WorkflowResult: Result of the retry.

        Raises:
            OrchestrationError: If retry fails.
        """
        if workflow_id not in self.workflows:
            raise OrchestrationError(f"Workflow {workflow_id} not found")

        status = self.workflows[workflow_id]

        # Extract components from workflow_id
        parts = workflow_id.split("/")
        if len(parts) < 3:
            raise OrchestrationError(f"Invalid workflow ID format: {workflow_id}")

        repo_owner = parts[0]
        repo_name = parts[1]
        pr_number = int(parts[2].split("-")[1])

        self.logger.info(f"Retrying workflow {workflow_id}")
        return self.process_pr(repo_owner, repo_name, pr_number)

    def _update_workflow_state(
        self,
        workflow_id: str,
        state: WorkflowState,
        pr_number: int,
        job_id: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:
        """Update internal workflow state."""
        if workflow_id not in self.workflows:
            self.workflows[workflow_id] = WorkflowStatus(
                workflow_id=workflow_id,
                state=state,
                pr_number=pr_number,
                job_id=job_id,
                message=message,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        else:
            self.workflows[workflow_id].state = state
            self.workflows[workflow_id].job_id = job_id
            self.workflows[workflow_id].message = message
            self.workflows[workflow_id].updated_at = datetime.utcnow()
