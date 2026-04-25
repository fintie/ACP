# Configuration Guide

## Environment Setup

### 1. Harness Hub Configuration

Set the following environment variables for ACP Connector:

```bash
export HARNESS_API_KEY="your-harness-hub-api-key"
export HARNESS_API_URL="https://api.harness.io"
```

**Getting your API Key:**
1. Log in to your Harness Hub account
2. Navigate to Settings → API Keys
3. Generate a new API key
4. Copy and store securely

### 2. GitHub Configuration

Set the following environment variables for GitHub Sync:

```bash
export GITHUB_TOKEN="your-github-personal-access-token"
export GITHUB_OWNER="your-github-username"
```

**Creating a GitHub Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Select scopes: `repo`, `read:org`
4. Copy and store securely

### 3. Orchestrator Configuration

Optional environment variables:

```bash
export TASKFLOW_LOG_LEVEL="INFO"
export TASKFLOW_RETRY_ATTEMPTS="3"
export TASKFLOW_TIMEOUT="3600"
```

## .env File Setup

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
HARNESS_API_KEY=your_key_here
HARNESS_API_URL=https://api.harness.io
GITHUB_TOKEN=your_token_here
GITHUB_OWNER=your_username
WEBHOOK_SECRET=random_secret_here
LOG_LEVEL=INFO
```

⚠️ **Never commit `.env` file to version control!**

## Docker Configuration

When running in Docker:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set environment variables
ENV HARNESS_API_KEY=${HARNESS_API_KEY}
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV HARNESS_API_URL=https://api.harness.io

CMD ["python", "-m", "taskflow_orchestrator"]
```

Run with:
```bash
docker run \
  -e HARNESS_API_KEY="your-key" \
  -e GITHUB_TOKEN="your-token" \
  acp-connector:latest
```

## Webhook Configuration

For automatic PR detection:

### GitHub Webhook Setup

1. Go to your repository
2. Settings → Webhooks → Add webhook
3. Set Payload URL: `https://your-domain.com/webhook/github`
4. Set Content type: `application/json`
5. Events: Select `Pull requests`
6. Add webhook

### Webhook Handler (Flask Example)

```python
from flask import Flask, request
from taskflow_orchestrator import TaskflowOrchestrator

app = Flask(__name__)

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    event = request.json
    
    if event['action'] == 'opened':
        pr = event['pull_request']
        orchestrator = TaskflowOrchestrator()
        
        result = orchestrator.process_pr(
            repo_owner=pr['head']['repo']['owner']['login'],
            repo_name=pr['head']['repo']['name'],
            pr_number=pr['number']
        )
        
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Logging Configuration

### Log Levels

```python
import logging
from taskflow_orchestrator import TaskflowOrchestrator

# Set log level
orchestrator = TaskflowOrchestrator(log_level="DEBUG")

# Or use environment variable
# export TASKFLOW_LOG_LEVEL=DEBUG
```

### Log File Output

```python
import logging

logging.basicConfig(
    filename='acp.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Security Best Practices

1. **Credentials:**
   - Never hardcode credentials
   - Use environment variables or `.env` file
   - Rotate API keys regularly
   - Use strong GitHub tokens with minimal scope

2. **Transport:**
   - Always use HTTPS
   - Validate SSL certificates
   - Use secure webhook URLs

3. **Logging:**
   - Never log credentials or tokens
   - Sanitize sensitive data
   - Rotate log files

4. **Access Control:**
   - Use strong authentication
   - Limit API scopes
   - Monitor API usage

## Troubleshooting

### Authentication Errors

```python
# Check if credentials are set correctly
import os
print(os.getenv('HARNESS_API_KEY'))  # Should not be None
print(os.getenv('GITHUB_TOKEN'))      # Should not be None
```

### Connection Errors

```python
# Test connection
from acp_connector import ACPConnector
connector = ACPConnector()
jobs = connector.list_jobs()
print(jobs)
```

### Webhook Issues

- Check webhook delivery in GitHub settings
- Verify URL is publicly accessible
- Check firewall rules
- Review application logs

## Production Checklist

- [ ] All credentials set via environment variables
- [ ] `.env` file excluded from version control
- [ ] HTTPS enabled for webhooks
- [ ] Logging configured and monitored
- [ ] Error alerting set up
- [ ] Database/persistence configured
- [ ] Rate limiting implemented
- [ ] Health checks in place
