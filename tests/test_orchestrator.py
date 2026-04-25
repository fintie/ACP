"""Tests for taskflow-orchestrator."""

import pytest
from unittest.mock import Mock, patch
from taskflow_orchestrator import TaskflowOrchestrator, WorkflowState


@patch("taskflow_orchestrator.orchestrator.ACPConnector")
@patch("taskflow_orchestrator.orchestrator.GitHubSync")
def test_orchestrator_init(mock_github_sync, mock_acp_connector):
    """Test TaskflowOrchestrator initialization."""
    orchestrator = TaskflowOrchestrator(
        acp_api_key="test-key", github_token="test-token"
    )
    assert orchestrator.connector is not None
    assert orchestrator.syncer is not None


@patch("taskflow_orchestrator.orchestrator.ACPConnector")
@patch("taskflow_orchestrator.orchestrator.GitHubSync")
def test_process_pr(mock_github_sync_class, mock_acp_connector_class):
    """Test processing a PR."""
    # Setup mocks
    mock_acp_connector = Mock()
    mock_acp_connector_class.return_value = mock_acp_connector
    mock_acp_connector.submit_job.return_value = "job-123"

    mock_github_sync = Mock()
    mock_github_sync_class.return_value = mock_github_sync

    mock_pr_status = Mock()
    mock_pr_status.title = "Test Feature"
    mock_pr_status.author = "testuser"
    mock_github_sync.monitor_pr.return_value = mock_pr_status

    # Test
    orchestrator = TaskflowOrchestrator(
        acp_api_key="test-key", github_token="test-token"
    )
    result = orchestrator.process_pr("owner", "repo", 42)

    # Assertions
    assert result.job_id == "job-123"
    assert result.pr_number == 42
    assert result.status == WorkflowState.RUNNING


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
