"""Tests for github-sync."""

import pytest
from unittest.mock import Mock, patch
from github_sync import GitHubSync, GitHubAuthenticationError, PRNotFoundError


def test_sync_init_with_token():
    """Test GitHubSync initialization with token."""
    with patch("github_sync.sync.Github") as mock_github:
        mock_client = Mock()
        mock_github.return_value = mock_client
        mock_client.get_user.return_value = Mock()

        syncer = GitHubSync(github_token="test-token")
        assert syncer.client is not None


def test_sync_init_without_token():
    """Test GitHubSync raises error without token."""
    with pytest.raises(GitHubAuthenticationError):
        GitHubSync(github_token=None)


@patch("github_sync.sync.Github")
def test_monitor_pr(mock_github_class):
    """Test monitoring a PR."""
    mock_client = Mock()
    mock_github_class.return_value = mock_client
    mock_client.get_user.return_value = Mock()

    mock_user = Mock()
    mock_repo = Mock()
    mock_pr = Mock()

    mock_client.get_user.return_value = mock_user
    mock_user.get_repo.return_value = mock_repo
    mock_repo.get_pull.return_value = mock_pr

    mock_pr.number = 42
    mock_pr.title = "Test PR"
    mock_pr.state = "open"
    mock_pr.user.login = "testuser"
    mock_pr.created_at = "2026-04-25T10:00:00"

    syncer = GitHubSync(github_token="test-token")
    status = syncer.monitor_pr("owner", "repo", 42)

    assert status.pr_number == 42
    assert status.title == "Test PR"
    assert status.state == "open"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
