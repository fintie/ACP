# reward-validator Skill

## Purpose
Detect and mitigate reward hacking in job execution by validating that completed tasks genuinely fulfill intended objectives rather than exploiting reward function weaknesses.

## Functionality
Implements systematic reward hacking detection through iterative reward testing, human-in-the-loop feedback, adversarial validation, and safe RL practices.

## Key Features

- **Iterative Reward Testing:** Systematic evaluation of reward signals across multiple test scenarios
- **Feedback Integration:** Human-in-the-loop validation to verify genuine task completion
- **Adversarial Validation:** Identifies edge cases and unintended exploitation patterns
- **Behavioral Robustness:** Ensures tasks complete consistently across varied conditions
- **Ethical Compliance:** Validates outcomes meet ethical and business constraints
- **Generalization Testing:** Confirms solutions work beyond training scenarios

## API Reference

### RewardValidator

Main class for reward hacking detection.

#### Methods

- `validate_reward(job_result: JobResult, reward_signals: Dict) -> ValidationResult`
  - Comprehensive validation of reward signals
  - Returns: ValidationResult with safety score

- `iterative_test(baseline: JobResult, variants: List[JobResult]) -> TestReport`
  - Test reward consistency across variations
  - Returns: TestReport with findings

- `adversarial_check(job_result: JobResult) -> AdversarialReport`
  - Identify potential exploitation patterns
  - Returns: AdversarialReport with risks

- `behavioral_robustness_check(job_result: JobResult, scenarios: List[Dict]) -> RobustnessReport`
  - Test performance across conditions
  - Returns: RobustnessReport

- `human_feedback_loop(job_result: JobResult) -> FeedbackResult`
  - Collect and integrate human validation
  - Returns: FeedbackResult

- `ethical_compliance_check(job_result: JobResult, constraints: List[str]) -> ComplianceReport`
  - Verify ethical and business constraints
  - Returns: ComplianceReport
