# Security Policy

## Intended use

BLACKMIND-AI supports legitimate software engineering, learning, debugging, code review, and defensive security on systems the user is authorized to assess.

## Current safeguards

- Model credentials are read from environment configuration.
- The health endpoint reports only whether a key is configured; it never returns the key.
- Generated code is returned as text and is not executed by the service.
- Request lengths and model timeout are bounded.
- Provider errors are normalized without returning response bodies that might contain sensitive data.

## Before production

- Put the service behind authentication and HTTPS.
- Add per-user rate limits, quotas, and request auditing with secret redaction.
- Store credentials in a secret manager.
- Add tenant isolation before storing project data.
- If code execution is introduced, use disposable isolated sandboxes with strict CPU, memory, filesystem, network, and time limits.
- Require explicit approval before applying patches, modifying repositories, or publishing changes.
- Add prompt-injection tests for repository files and retrieved content.

Report vulnerabilities privately to the repository maintainer. Avoid publishing exploit details before a fix is available.
