# Contributing to ACP Harness Hub Connector Platform

Thank you for your interest in contributing to the ACP platform! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Assume good faith in discussions
- Focus on the code, not the person
- Help others succeed

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Write or update tests as needed
6. Ensure all tests pass: `pytest`
7. Format code: `black .`
8. Check linting: `flake8 .`
9. Run type checking: `mypy .`
10. Commit your changes: `git commit -m "Description of your changes"`
11. Push to your fork: `git push origin feature/your-feature-name`
12. Create a Pull Request

## Development Setup

```bash
# Clone and setup
git clone https://github.com/your-username/ACP.git
cd ACP
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

## Code Style

- Follow PEP 8
- Use type hints
- Keep functions focused and small
- Add docstrings to all public functions

## Testing

- Write tests for new features
- Maintain or improve code coverage
- Run `pytest` before submitting PR
- Use `pytest -v` for detailed output

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Refactor"
- Keep first line under 50 characters
- Add detailed description if needed

## Pull Request Process

1. Update the README if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Describe your changes clearly in the PR

## Reporting Issues

- Check if issue already exists
- Provide clear description
- Include steps to reproduce
- Add relevant logs or error messages
- Specify your environment (Python version, OS, etc.)

## Questions?

Feel free to open a discussion or issue!
