# BLACKMIND-AI

A focused AI software-engineering assistant for planning, writing, explaining, refactoring, debugging, and reviewing code.

## Current capabilities

- FastAPI service with health and coding-task endpoints.
- OpenAI-compatible model adapter; provider and model are configurable.
- Multi-stage workflow: **Project Context → Planner → Engineer → Reviewer**.
- Accepts up to 30 virtual source files as project context, with path, secret-file, binary-content, and size validation.
- Structured output containing a plan, implementation, and independent review.
- Environment-based secrets; no credentials are committed.
- Generated code is returned as text and is never executed by this service.

> This is a software foundation, not a trained model or an autonomous software engineer. Configure a compatible model endpoint and API key before using code generation.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your provider's base URL, model ID, and API key.

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## API

`GET /health` reports service status and whether credentials are configured. It never returns the key.

`POST /v1/code`

```json
{
  "task": "Find why the login form validation is failing and propose a fix.",
  "language": "python",
  "context": "Keep the public API backwards compatible.",
  "project_files": [
    {
      "path": "app/validators.py",
      "content": "def validate_email(value):\n    return '@' in value\n"
    },
    {
      "path": "tests/test_validators.py",
      "content": "def test_email_validation():\n    assert validate_email('a@example.com')\n"
    }
  ]
}
```

Response fields: `plan`, `implementation`, and `review`.

Project context limits:
- Up to 30 files per request.
- Up to 16,000 characters per file.
- Up to 50,000 characters total across file paths and contents.
- Absolute paths, traversal paths, VCS/dependency folders, common secret files, private-key files, and binary content are rejected.

Only submit source files you are authorized to share. Do not include credentials, tokens, or private keys in source content.

## Configuration

| Variable | Purpose |
|---|---|
| `APP_NAME` | Service name |
| `MODEL_BASE_URL` | OpenAI-compatible API base URL |
| `MODEL_NAME` | Model identifier supported by your provider |
| `MODEL_API_KEY` | Secret API key |
| `MODEL_TIMEOUT_SECONDS` | Request timeout |
| `MODEL_MAX_TOKENS` | Maximum generated tokens |

## Tests

```bash
pytest
```

## Roadmap

1. Repository-aware context and file indexing.
2. Diff/patch generation with explicit user approval.
3. Isolated test execution with resource limits.
4. Project memory and retrieval with source references.
5. Specialist workflows and evaluation benchmarks.
6. Observability, budgets, cancellation, and deployment hardening.

## Safety

This project is for legitimate software development, education, and defensive security. It must not be used to create malware, steal credentials, evade detection, or compromise systems. Generated code is not executed by this service. Review and test outputs in an appropriate environment before use.
