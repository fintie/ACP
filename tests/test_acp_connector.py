"""Tests for acp-connector."""

import pytest
from unittest.mock import Mock, patch
from acp_connector import ACPConnector, ACPAuthenticationError, ACPConnectionError


def test_connector_init_with_api_key():
    """Test ACPConnector initialization with API key."""
    connector = ACPConnector(api_key="test-key", base_url="https://test.api.com")
    assert connector.api_key == "test-key"
    assert connector.base_url == "https://test.api.com"


def test_connector_init_without_api_key():
    """Test ACPConnector raises error without API key."""
    with pytest.raises(ACPAuthenticationError):
        ACPConnector(api_key=None)


@patch("acp_connector.connector.requests.Session.get")
def test_get_harness_status(mock_get):
    """Test getting job status."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "job_id": "job-123",
        "state": "running",
        "progress": 50,
        "created_at": "2026-04-25T10:00:00",
        "updated_at": "2026-04-25T10:05:00",
        "metadata": {},
    }
    mock_get.return_value = mock_response

    connector = ACPConnector(api_key="test-key")
    status = connector.get_harness_status("job-123")

    assert status.job_id == "job-123"
    assert status.state == "running"
    assert status.progress == 50


@patch("acp_connector.connector.requests.Session.post")
def test_submit_job(mock_post):
    """Test submitting a job."""
    mock_response = Mock()
    mock_response.json.return_value = {"job_id": "job-456"}
    mock_post.return_value = mock_response

    connector = ACPConnector(api_key="test-key")
    job_id = connector.submit_job("Deploy to staging", {"branch": "feature/new"})

    assert job_id == "job-456"


@patch("acp_connector.connector.requests.Session.post")
def test_cancel_job(mock_post):
    """Test cancelling a job."""
    mock_response = Mock()
    mock_response.return_value = True
    mock_post.return_value = mock_response

    connector = ACPConnector(api_key="test-key")
    result = connector.cancel_job("job-789")

    assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
