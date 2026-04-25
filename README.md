# ACP Harness Hub Connector Platform

A comprehensive system designed to proactively connect developers with the ACP Harness Hub, enabling collaborative, traceable building workflows.

## 🚀 Goal

To create a system that seamlessly connects developers with the ACP Harness Hub, allowing for proactive integration of code, PRs, and development tasks into the Harness Hub workflow.

## 🛠️ Core Components & Skills

The platform is built around three core skills designed to orchestrate the connection and execution steps:

### 1. **`acp-connector` Skill**
- **Purpose:** Direct, secure communication with the ACP Harness Hub API.
- **Functionality:** Authenticates developer requests, translates high-level goals into Harness Hub jobs, and fetches real-time status.
- **Location:** [acp-connector/](acp-connector/)

### 2. **`github-sync` Skill**
- **Purpose:** Manages all version control interactions.
- **Functionality:** Monitors developer branches, handles PR creation/updates, and ensures code commits align with the Harness Hub workflow steps.
- **Location:** [github-sync/](github-sync/)

### 3. **`taskflow-orchestrator` Skill**
- **Purpose:** The central logic layer that chains the connection and execution steps.
- **Functionality:** Takes a developer request, sequences calls to `acp-connector` and `github-sync`, handles error routing, and manages the state of the build flow.
- **Location:** [taskflow-orchestrator/](taskflow-orchestrator/)

## 🔄 Workflow Example: Proactive Connection

This outlines how the system operates when a developer commits a feature branch and opens a Pull Request (PR):

1. **Developer Action:** A developer commits a feature branch to GitHub and opens a Pull Request (PR).
2. **Detection:** The system detects the new PR via a webhook or polling mechanism.
3. **Orchestration (`taskflow-orchestrator`):** The orchestrator is triggered.
4. **Connection (`acp-connector`):** It queries the Harness Hub to see if this PR aligns with any active development workflows.
5. **Synchronization (`github-sync`):** If a match is found, it pulls the relevant context and updates the Harness Hub status accordingly.
6. **Result:** Developers are proactively notified about the next required steps in the build process.

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/fintie/ACP.git
cd ACP
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## 🚀 Quick Start

### Using the Orchestrator

```python
from taskflow_orchestrator import TaskflowOrchestrator

orchestrator = TaskflowOrchestrator()
result = orchestrator.process_pr(
    repo_owner="fintie",
    repo_name="my-project",
    pr_number=42
)
print(result)
```

### Using the ACP Connector Directly

```python
from acp_connector import ACPConnector

connector = ACPConnector(api_key="your-api-key")
status = connector.get_harness_status(job_id="job-123")
print(status)
```

### Using GitHub Sync

```python
from github_sync import GitHubSync

syncer = GitHubSync(github_token="your-token")
syncer.monitor_pr("fintie", "my-project", 42)
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Configuration](docs/CONFIGURATION.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 💬 Support

For issues, questions, or suggestions, please open an issue on [GitHub](https://github.com/fintie/ACP/issues).

---

**Built with ❤️ for seamless developer collaboration**
