# AGENTS.md

If you are an agent reading this repo, start here.

## What this repo is
- A kit of method files (skills), prompts, scripts, and templates for improving an LLM product's accuracy with evidence.
- Three methods: build an eval, hillclimb an existing eval, red-team the product. Judges can run on the OpenAI API or on a ChatGPT subscription through `codex exec`.
- You do the grind. Your user keeps the final call: they approve the eval, the budget, and any merge or deploy.

## Step 1: ask your user two questions
1. Goal: build an eval, hillclimb an existing eval, or red-team the product?
2. Billing: is a ChatGPT subscription available for judges (judges run via `codex exec`), or is it API-only?

Do not guess. Wait for both answers.

## Step 2: pick the prompt and the skill

| Goal | Billing | Prompt to run | Skill it uses |
| --- | --- | --- | --- |
| Build an eval | API-only | `prompts/build-eval-api.md` | `skills/build-eval/SKILL.md` |
| Build an eval | Subscription | `prompts/build-eval-subscription.md` | `skills/build-eval/SKILL.md` |
| Hillclimb | API-only | `prompts/hillclimb-api.md` | `skills/hillclimb/SKILL.md` |
| Hillclimb | Subscription | `prompts/hillclimb-subscription.md` | `skills/hillclimb/SKILL.md` |
| Red-team | API-only | `prompts/red-team-api.md` | `skills/red-team/SKILL.md` |
| Red-team | Subscription | `prompts/red-team-subscription.md` | `skills/red-team/SKILL.md` |

Every skill sends you to `judges.md` for judge setup. Read the section for the chosen billing mode. Hillclimb needs a finished eval: if the user has none, run build-eval first.

## Prerequisites to check before any paid call
- The product can be called from a script (its real code path, not a copy of its prompt). If not, build a small adapter first.
- Claude judges only: `ANTHROPIC_API_KEY` is set. Check with `[ -n "$ANTHROPIC_API_KEY" ]`. A Claude subscription is never a substitute.
- An OpenAI API key is set for the product model. Check with `[ -n "$OPENAI_API_KEY" ]`. Never echo it.
- Subscription mode only: the `codex` CLI is installed and logged in with ChatGPT (`codex login status`). Your user must confirm their plan terms allow automated grading. Read `judges.md`.
- Python 3 is available. Run `python3 scripts/<name>.py --help` to see what each script does.
- A dollar cap from the user. If they gave none, ask.

## Which subscription may run judges
The rule depends on the company that makes the judge model. It does not depend on the product model.

| Judge model | Subscription allowed? | How to run it |
| --- | --- | --- |
| OpenAI (GPT) | Yes, a ChatGPT plan through `codex exec` | Subscription mode or API mode |
| Claude (Anthropic) | **No. Never.** | Anthropic API key only, billed at API prices |

- Never run a Claude judge through a Claude subscription: not `claude -p`, not Claude Code, not the Claude app, not any script that drives them. Anthropic does not allow automated use of a subscription, and it bans the account. This has already happened to one account.
- A Claude judge needs `ANTHROPIC_API_KEY` set (check with `[ -n "$ANTHROPIC_API_KEY" ]`). If it is not set, stop and ask. Do not fall back to a subscription.
- The product model always runs on its own provider's API key, in both modes.

## Hard rules
- Never run a Claude model through a Claude subscription for judging or any other automated call. Claude judges use an Anthropic API key. See the section above.
- Never print, log, or commit a secret, key, or login file.
- Enforce the dollar cap in code with `scripts/budget.py`. A cap in a prompt is not a cap.
- The held-out set gets one look. After it changes any decision it is no longer held out.
- Only regression versus production blocks a release. Old failures are known issues.
- Scores come from runner code, never from your own narrative.
- Infrastructure failures are ungraded and retried on the same saved answer. Never rerun the product to get a pass.
- Do not deploy, merge, or write to production. Leave that to your user.
- Do not put private cases or answer keys where the optimizer can read them.

## Commands
There is no build and no test suite. CI compiles every script and runs each with `--help`:
```sh
for f in scripts/*.py; do python3 -m py_compile "$f" && python3 "$f" --help > /dev/null || echo "FAIL $f"; done
```
Scripts use only the Python standard library. Do not add dependencies.

## Code map
- `skills/` method, billing-neutral. `judges.md` the two billing modes.
- `scripts/` shared code. `templates/` contract, schema, controls, macOS sandbox policy.
- `prompts/` the six copy-paste prompts. `SOURCES.md` references.
- `scripts/budget.py` dollar cap with reserve and settle. `scripts/classify.py` sorts attempts into pass, product failure, infrastructure failure, ungraded.
- `scripts/two_judges.py` template for two API judges. `scripts/grade_with_codex.py` one judge call through `codex exec`. `scripts/calibrate.py` calibration gate.
- `scripts/isolation_check.py` canary check for the grader. `scripts/allowlist_proxy.py` host allowlist proxy for the macOS sandbox.

## Conventions when editing this repo
- Match the surrounding code and wording. Short, plain sentences. No em dashes.
- Keep skills, prompts, `AGENTS.md`, and `judges.md` consistent with each other. If a rule changes in one, change it in all.
- Add a line under `[Unreleased]` in `CHANGELOG.md` for user-visible changes.
- Do not weaken a hard rule above. Do not add a path that drives a Claude subscription.
- See `CONTRIBUTING.md` for the pull request checklist.
