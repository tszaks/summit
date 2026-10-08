# Prompt: hillclimb an existing eval, API billing

Copy this block into your agent. Fill in the placeholders in angle brackets.

---

Read these files in this repo, in this order:
1. `AGENTS.md`
2. `skills/hillclimb/SKILL.md`
3. `judges.md`. Read the "API mode" section.

Task: hillclimb an existing eval for my product. Judges use the OpenAI API. The product model uses the OpenAI API.

My inputs:
- Product: <what it is and what behavior to measure>
- How to call it from a script: <command, function, or endpoint>
- Eval location and run command: <path and command>
- Contract file: <path, or "none">
- Budget cap in dollars: <number>
- Product model: <model name>

Steps:
1. Check the preconditions: runner, calibrated judges, editable-file list, limits, acceptance rule. If one is missing, stop and tell me.
2. Measure a fresh baseline.
3. Run the loop: one hypothesis, one change, dev run, private validation, paired comparison.
4. Append one ledger row per trial.
5. Lock one candidate. Run the held-out set once.
6. Hand back the patch, ledger, commands, results, and cost. Do not merge or deploy.

Rules:
- Never print a secret. Check variables with `[ -n "$VAR" ]`.
- Enforce the dollar cap with `scripts/budget.py`.
- Do not deploy, merge, or write to production.

Stop and ask me if:
- The spend reaches the dollar cap or the round cap.
- Three trials in a row are not adopted.
- The held-out set was already used for a decision.
- A protected file changed, or a judge model changed.
- The baseline is about 95% or higher.
