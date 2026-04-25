"""ACP Connector module for communicating with Harness Hub API."""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from pydantic import BaseModel, Field


class JobStatus(BaseModel):
    """Model for job status information."""

    job_id: str
    state: str
    progress: int = Field(ge=0, le=100)
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = {}


class JobSummary(BaseModel):
    """Model for job summary information."""

    job_id: str
    goal: str
    state: str
    created_at: datetime


class ACPAuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class ACPConnectionError(Exception):
    """Raised when connection to Harness Hub fails."""

    pass


class ACPJobError(Exception):
    """Raised when job execution fails."""

    pass


class ACPConnector:
    """Main class for interacting with the ACP Harness Hub API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the ACP Connector.

        Args:
            api_key: Harness Hub API key. If not provided, reads from HARNESS_API_KEY env var.
            base_url: Base URL for Harness Hub API. If not provided, reads from HARNESS_API_URL env var.

        Raises:
            ACPAuthenticationError: If no API key is provided or found.
        """
        self.api_key = api_key or os.getenv("HARNESS_API_KEY")
        if not self.api_key:
            raise ACPAuthenticationError("API key not provided or found in HARNESS_API_KEY")

        self.base_url = base_url or os.getenv(
            "HARNESS_API_URL", "https://api.harness.io"
        )
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )

    def get_harness_status(self, job_id: str) -> JobStatus:
        """
        Fetch the current status of a job from Harness Hub.

        Args:
            job_id: The ID of the job to check.

        Returns:
            JobStatus: The current status of the job.

        Raises:
            ACPConnectionError: If connection to Harness Hub fails.
            ACPJobError: If the job is not found.
        """
        try:
            response = self.session.get(f"{self.base_url}/jobs/{job_id}")
            response.raise_for_status()

            data = response.json()
            return JobStatus(**data)

        except requests.exceptions.RequestException as e:
            raise ACPConnectionError(f"Failed to connect to Harness Hub: {str(e)}")
        except Exception as e:
            raise ACPJobError(f"Failed to fetch job status: {str(e)}")

    def submit_job(self, goal: str, context: Dict[str, Any]) -> str:
        """
        Submit a new job to the Harness Hub.

        Args:
            goal: The high-level goal for the job.
            context: Additional context dictionary.

        Returns:
            str: The ID of the submitted job.

        Raises:
            ACPConnectionError: If connection to Harness Hub fails.
        """
        try:
            payload = {"goal": goal, "context": context, "created_at": datetime.utcnow()}

            response = self.session.post(f"{self.base_url}/jobs", json=payload)
            response.raise_for_status()

            data = response.json()
            return data.get("job_id")

        except requests.exceptions.RequestException as e:
            raise ACPConnectionError(f"Failed to submit job to Harness Hub: {str(e)}")

    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel an active job.

        Args:
            job_id: The ID of the job to cancel.

        Returns:
            bool: True if cancellation was successful.

        Raises:
            ACPConnectionError: If connection to Harness Hub fails.
        """
        try:
            response = self.session.post(f"{self.base_url}/jobs/{job_id}/cancel")
            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
            raise ACPConnectionError(f"Failed to cancel job: {str(e)}")

    def list_jobs(self, filters: Optional[Dict[str, Any]] = None) -> List[JobSummary]:
        """
        List all jobs matching optional filters.

        Args:
            filters: Optional dictionary of filters.

        Returns:
            List[JobSummary]: List of matching jobs.

        Raises:
            ACPConnectionError: If connection to Harness Hub fails.
        """
        try:
            response = self.session.get(
                f"{self.base_url}/jobs", params=filters or {}
            )
            response.raise_for_status()

            data = response.json()
            return [JobSummary(**job) for job in data.get("jobs", [])]

        except requests.exceptions.RequestException as e:
            raise ACPConnectionError(f"Failed to list jobs: {str(e)}")
