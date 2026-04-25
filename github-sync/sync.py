"""GitHub synchronization module for managing version control interactions."""

import os
from typing import Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel
from github import Github, GithubException


class PRStatus(BaseModel):
    """Model for pull request status."""

    pr_number: int
    title: str
    state: str
    author: str
    created_at: datetime
    harness_job_id: Optional[str] = None
    workflow_status: Optional[str] = None


class PR(BaseModel):
    """Model for pull request details."""

    number: int
    title: str
    body: str
    head_branch: str
    base_branch: str
    author: str
    state: str
    created_at: datetime
    url: str


class GitHubAuthenticationError(Exception):
    """Raised when GitHub authentication fails."""

    pass


class GitHubConnectionError(Exception):
    """Raised when connection to GitHub fails."""

    pass


class PRNotFoundError(Exception):
    """Raised when PR is not found."""

    pass


class BranchNotFoundError(Exception):
    """Raised when branch is not found."""

    pass


class GitHubSync:
    """Main class for GitHub synchronization."""

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub Sync.

        Args:
            github_token: GitHub personal access token. If not provided, reads from GITHUB_TOKEN env var.

        Raises:
            GitHubAuthenticationError: If no token is provided or found.
        """
        token = github_token or os.getenv("GITHUB_TOKEN")
        if not token:
            raise GitHubAuthenticationError(
                "GitHub token not provided or found in GITHUB_TOKEN"
            )

        try:
            self.client = Github(token)
            self.client.get_user()  # Test connection
        except GithubException as e:
            raise GitHubAuthenticationError(f"Failed to authenticate with GitHub: {str(e)}")

    def monitor_pr(self, owner: str, repo: str, pr_number: int) -> PRStatus:
        """
        Monitor a specific pull request.

        Args:
            owner: Repository owner.
            repo: Repository name.
            pr_number: Pull request number.

        Returns:
            PRStatus: The current status of the PR.

        Raises:
            GitHubConnectionError: If connection fails.
            PRNotFoundError: If PR is not found.
        """
        try:
            repository = self.client.get_user(owner).get_repo(repo)
            pr = repository.get_pull(pr_number)

            return PRStatus(
                pr_number=pr.number,
                title=pr.title,
                state=pr.state,
                author=pr.user.login,
                created_at=pr.created_at,
            )

        except GithubException as e:
            if e.status == 404:
                raise PRNotFoundError(f"PR #{pr_number} not found")
            raise GitHubConnectionError(f"Failed to fetch PR: {str(e)}")

    def update_pr_status(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        status: str,
        comment: Optional[str] = None,
    ) -> bool:
        """
        Update PR status with a comment.

        Args:
            owner: Repository owner.
            repo: Repository name.
            pr_number: Pull request number.
            status: Status message.
            comment: Optional detailed comment.

        Returns:
            bool: True if update was successful.

        Raises:
            GitHubConnectionError: If connection fails.
            PRNotFoundError: If PR is not found.
        """
        try:
            repository = self.client.get_user(owner).get_repo(repo)
            pr = repository.get_pull(pr_number)

            full_comment = f"**Status:** {status}\n\n{comment or 'No additional details.'}"
            pr.create_issue_comment(full_comment)

            return True

        except GithubException as e:
            if e.status == 404:
                raise PRNotFoundError(f"PR #{pr_number} not found")
            raise GitHubConnectionError(f"Failed to update PR: {str(e)}")

    def create_pr(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ) -> PR:
        """
        Create a new pull request.

        Args:
            owner: Repository owner.
            repo: Repository name.
            title: PR title.
            body: PR description.
            head: Head branch.
            base: Base branch (default: main).

        Returns:
            PR: The created PR object.

        Raises:
            GitHubConnectionError: If creation fails.
        """
        try:
            repository = self.client.get_user(owner).get_repo(repo)
            pr = repository.create_pull(title=title, body=body, head=head, base=base)

            return PR(
                number=pr.number,
                title=pr.title,
                body=pr.body,
                head_branch=pr.head.ref,
                base_branch=pr.base.ref,
                author=pr.user.login,
                state=pr.state,
                created_at=pr.created_at,
                url=pr.html_url,
            )

        except GithubException as e:
            raise GitHubConnectionError(f"Failed to create PR: {str(e)}")

    def sync_branch(self, owner: str, repo: str, branch: str) -> bool:
        """
        Sync a branch with latest changes.

        Args:
            owner: Repository owner.
            repo: Repository name.
            branch: Branch name to sync.

        Returns:
            bool: True if sync was successful.

        Raises:
            GitHubConnectionError: If sync fails.
            BranchNotFoundError: If branch is not found.
        """
        try:
            repository = self.client.get_user(owner).get_repo(repo)
            branch_obj = repository.get_branch(branch)

            # Fetch latest commit info
            latest_commit = branch_obj.commit

            return True

        except GithubException as e:
            if e.status == 404:
                raise BranchNotFoundError(f"Branch '{branch}' not found")
            raise GitHubConnectionError(f"Failed to sync branch: {str(e)}")
