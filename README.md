# Summit

**Climb until your AI stops being confidently wrong.**

A kit that lets a coding agent build an eval for your LLM product, hillclimb it with bounded trials, and red-team it. It works with Codex, Claude Code, and similar agents.

## What and why

You have an LLM product (a chat assistant, an agent, a prompt plus tools) and you want better accuracy based on evidence, not guesses. The agent does the grind. A runner, not the agent, computes scores and enforces the dollar cap. You keep the final call.

## Three methods, two billing modes

| Method | Judges on the API | Judges on a ChatGPT subscription |
| --- | --- | --- |
| Build an eval | `prompts/build-eval-api.md` | `prompts/build-eval-subscription.md` |
| Hillclimb an eval | `prompts/hillclimb-api.md` | `prompts/hillclimb-subscription.md` |
| Red-team | `prompts/red-team-api.md` | `prompts/red-team-subscription.md` |

In both modes your product's own model calls bill to its provider's API. Subscription mode runs the judges through `codex exec`, so judging adds no API charge. Check your plan terms first. See `judges.md`.

## How to use it

Point your agent at this repo and say: "Read AGENTS.md in this repo and set it up for my project." The agent asks you two questions (your goal, your billing) and runs the matching prompt. You can also paste a file from `prompts/` yourself.

Python scripts need only Python 3. Run any script with `--help`. Codex flag names change between versions; check `codex exec --help`.

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

Inspired by Anthropic's post [Automating eval design and hillclimbing with Claude](https://claude.dev/blog/automating-eval-design-and-hillclimbing/). This repo is independent original work; no code or text was copied. See `SOURCES.md`.

## License

MIT. See `LICENSE`.
