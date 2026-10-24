# Security policy

## Supported versions

Summit has no tagged releases. Only the latest commit on the default branch gets security fixes.

| Version | Supported |
|---|---|
| `main` (latest) | Yes |
| Older commits | No |

## Reporting a vulnerability

Please report security problems privately, not in a public issue.

Use GitHub private vulnerability reporting: open the **Security** tab of this repository and choose **Report a vulnerability**. If that is not available to you, email tyler@szakacsmedia.com.

Please include:

- What you found and what an attacker could do with it.
- Steps to reproduce.
- Your OS, Python version, and Codex version if the issue involves `codex exec`.

You can expect a first reply within a few days. Summit is maintained by one person, so a fix may take longer, but you will get updates. Once a fix is released we will credit you in the changelog unless you prefer to stay anonymous.

## What counts

Summit's scripts handle API keys, a ChatGPT login, and private test cases. These areas matter most:

- Anything that prints, logs, or writes an API key or the Codex login files.
- A grader isolation gap: a judge that can read the answer key, private cases, or your repo (`scripts/grade_with_codex.py`, `scripts/isolation_check.py`, `templates/macos-grader-policy.sb.tmpl`).
- `scripts/allowlist_proxy.py` tunneling to a host that is not on its allowlist.
- A dollar cap in `scripts/budget.py` that can be bypassed or reset.
- Any path that drives a Claude subscription for automated judging.
