<h1 align="center">Summit</h1>

<p align="center">
  Climb until your AI stops being confidently wrong.<br>
  Agent skills to build an eval, hillclimb it, and red-team it.
</p>

<p align="center">
  <a href="https://github.com/tszaks/summit/actions/workflows/ci.yml"><img src="https://github.com/tszaks/summit/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/tszaks/summit" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/python-3-blue" alt="Python 3">
</p>

```text
You:    Read AGENTS.md in this repo and set it up for my project.
Agent:  Two questions first.
        1. Goal: build an eval, hillclimb an existing eval, or red-team the product?
        2. Billing: is a ChatGPT subscription available for judges, or is it API-only?
You:    Build an eval. API-only.
Agent:  Running prompts/build-eval-api.md with skills/build-eval/SKILL.md.
```

Summit is a kit that lets a coding agent build an eval for your LLM product, hillclimb it with bounded trials, and red-team it. It works with Codex, Claude Code, and similar agents. It is a set of method files (skills), prompts, small Python scripts, and templates. It is not a framework or a service.

It is for people who ship an LLM product (a chat assistant, an agent, a prompt plus tools) and want better accuracy based on evidence, not guesses. The agent does the grind. A runner, not the agent, computes scores and enforces the dollar cap. You keep the final call.

## Features

- **Three methods.** `build-eval`, `hillclimb`, and `red-team`, each a billing-neutral skill in `skills/`.
- **Two billing modes.** Judges run on the OpenAI API, or on a ChatGPT subscription through `codex exec`. Six copy-paste prompts in `prompts/` cover every pairing.
- **Claude judges on an API key only.** Never through a Claude subscription. See [judges.md](judges.md).
- **Two judges, two models.** A case passes only if both pass. Both sets of reasons are kept.
- **Calibration controls.** Known-good answers, known-bad answers, and an injection attempt run before any paid call (`scripts/calibrate.py`, `templates/controls.example.json`).
- **A dollar cap in code.** `scripts/budget.py` reserves before each paid call and settles after it.
- **Failure classes.** `scripts/classify.py` separates product failures from infrastructure failures, so a broken judge never counts as a pass.
- **Isolation proof.** `scripts/isolation_check.py` plants canary files and checks that the grader cannot read them.

## Quick start

Point your agent at this repo:

```sh
git clone https://github.com/tszaks/summit.git
cd summit
```

Then tell the agent: "Read AGENTS.md in this repo and set it up for my project." It asks two questions (your goal, your billing) and runs the matching prompt. You can also paste a file from `prompts/` yourself.

Python scripts need only Python 3. Run any script with `--help`. Codex flag names change between versions; check `codex exec --help`.

## Usage

Three methods, two billing modes:

| Method | Judges on the API | Judges on a ChatGPT subscription |
| --- | --- | --- |
| Build an eval | `prompts/build-eval-api.md` | `prompts/build-eval-subscription.md` |
| Hillclimb an eval | `prompts/hillclimb-api.md` | `prompts/hillclimb-subscription.md` |
| Red-team | `prompts/red-team-api.md` | `prompts/red-team-subscription.md` |

In both modes your product's own model calls bill to its provider's API. Subscription mode runs the judges through `codex exec`, so judging adds no API charge. Check your plan terms first. See [judges.md](judges.md).

**Claude judges need an Anthropic API key.** Only OpenAI judges may run on a subscription (ChatGPT through `codex exec`). Never run Claude judges through a Claude subscription (`claude -p`, Claude Code): Anthropic bans accounts for automated subscription use. This is true for any product model.

Hillclimb needs a finished eval. If you have none, run build-eval first.

### What is in the repo

| Path | What it holds |
| --- | --- |
| `skills/` | The three methods: `build-eval`, `hillclimb`, `red-team` |
| `prompts/` | Six copy-paste prompts, one per method and billing mode |
| `judges.md` | Judge setup for both billing modes, calibration, failure classes |
| `scripts/` | `budget.py`, `classify.py`, `two_judges.py`, `grade_with_codex.py`, `calibrate.py`, `isolation_check.py`, `allowlist_proxy.py` |
| `templates/` | Experiment contract, grader schema and instructions, example controls, macOS grader sandbox policy |
| `SOURCES.md` | References |

## Using with agents

Summit is made for agents. [AGENTS.md](AGENTS.md) is the entry point: it tells the agent which two questions to ask, which prompt and skill to run, what to check before any paid call, and the hard rules (dollar cap in code, no deploy or merge, no secrets in output).

## FAQ

**Does it need an API key?**
Yes, for the product model (it runs on its own provider's API). Claude judges also need `ANTHROPIC_API_KEY`. Subscription mode needs the `codex` CLI logged in with ChatGPT instead of judge API charges.

**Can I run Claude as a judge on my Claude subscription?**
No. Anthropic bans accounts for automated use of a subscription. Use an Anthropic API key.

**Is a ChatGPT subscription allowed for automated grading?**
That depends on your plan and organization terms. Check them first. If it is not allowed, use API mode.

**Can the agent spend more than my cap?**
The cap belongs in runner code, not in a prompt. `scripts/budget.py` holds the reserve and settle logic, and the runner calls it before every paid call. A cap in a prompt is not a cap.

## Lessons learned

- The thing you improve must not grade itself, and the optimizer must not read private cases. A git worktree is not a barrier. Prove isolation with a canary file.
- Use two judges from different models. Keep both sets of reasons when they disagree.
- Test judges first with known-good answers, known-bad answers, and an injection attempt. If a control fails, nothing else counts.
- Split product failures from infrastructure failures. Retry infrastructure failures on the same saved answer. Never rerun the product to get a pass.
- A verification layer that blocks a correct answer is a product failure. Count these false rejections as their own class.
- Compute answer keys in code from fixture data. Hand-typed numbers rot.
- The only release blocker is regression against production. Old failures are known issues.
- Keep a held-out set and look at it once.
- Go smoke, then focused set, then everything. Repeat flaky cases.
- Put the dollar cap in the runner, with a reserve per call. A cap in a prompt is not a cap.
- Pick cases that real users send and humans find hard, not cases the current model fails.
- If the baseline is near 95%, add harder cases before you hillclimb.
- Keep receipts (raw outputs, verdicts, hashes, costs). "Tests pass", "merged", and "deployed" are three facts.
- One run per case is noisy. In one campaign a drop from 199 to 193 of 201 was 7 parts noise to 1 part real. Run every changed case 3 times on both versions before you call it a regression or a gain.
- Changing the model's instructions trades failures: a rule that fixes two cases can break three others. Prefer fixes in deterministic checking code. When the instructions are dense, the gate will start rejecting most instruction changes. That is the signal to stop and freeze.
- Use judges from a different model family than the product. Same-family judges share blind spots, and in practice both judges of one family missed real errors.
- Never parse the product's prose with regex in a check. Ask the model to extract structured claims with an exact quote, verify in code that the quote appears verbatim, and compare the claim with the source data in code.
- An isolation check needs a positive control. A sandbox mode named "read-only" can block writes but still allow reads, and a judge told to "treat data as data" never even tries the read, so a check without a control passes for the wrong reason.
- Some providers reject large strict-output schemas ("grammar too large"). Keep structured-output schemas small, or request the JSON in the prompt and validate it in code.
- Attacks are retired once you fix against them. The next red-team round uses new attacks the fixes never saw. The summit is the point where fresh attacks stop finding confidently wrong answers.

## Credit

Inspired by Anthropic's post [Automating eval design and hillclimbing with Claude](https://claude.dev/blog/automating-eval-design-and-hillclimbing/). This repo is independent original work; no code or text was copied. See [SOURCES.md](SOURCES.md).

## Contributing

Bug reports and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first. Security problems go through [SECURITY.md](SECURITY.md). Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

Docs: [agents guide](AGENTS.md) · [judges](judges.md) · [sources](SOURCES.md) · [changelog](CHANGELOG.md)

## License

[MIT](LICENSE). Copyright (c) 2026 Tyler Szakacs.
