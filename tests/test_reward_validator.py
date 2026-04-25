"""Tests for reward-validator."""

import pytest
from datetime import datetime
from reward_validator import (
    RewardValidator,
    JobResult,
    RiskLevel,
    ValidationResult,
)


def test_validator_initialization():
    """Test RewardValidator initialization."""
    validator = RewardValidator(validation_threshold=0.85)
    assert validator.validation_threshold == 0.85


def test_validate_reward_safe_job():
    """Test validation of a safe job."""
    validator = RewardValidator()

    job_result = JobResult(
        job_id="job-safe-001",
        task_goal="Deploy to staging",
        completed_actions=[
            {"action": "build", "status": "success"},
            {"action": "test", "status": "success"},
            {"action": "deploy", "status": "success"},
        ],
        final_state={"deployment": "active", "status": "healthy"},
        metrics={"accuracy": 0.95, "latency": 120},
        execution_time=45.5,
    )

    result = validator.validate_reward(
        job_result=job_result, reward_signals={"accuracy": 0.95, "latency": 120}
    )

    assert isinstance(result, ValidationResult)
    assert result.safety_score >= 0.5
    assert isinstance(result.risk_level, RiskLevel)


def test_adversarial_check():
    """Test adversarial validation."""
    validator = RewardValidator()

    job_result = JobResult(
        job_id="job-adv-001",
        task_goal="Complex deployment",
        completed_actions=[{"action": f"action_{i}"} for i in range(200)],
        final_state={},
        metrics={"score": 0.99},
        execution_time=1.0,
    )

    report = validator.adversarial_check(job_result)
    assert 0 <= report.exploitation_risk <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
