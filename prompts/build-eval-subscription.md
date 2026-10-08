# Prompt: build an eval, subscription billing

Copy this block into your agent. Fill in the placeholders in angle brackets.

---

Read these files in this repo, in this order:
1. `AGENTS.md`
2. `skills/build-eval/SKILL.md`
3. `judges.md`. Read the "Subscription mode" section. Check `codex login status`. Ask me to confirm my plan terms allow automated grading. Run the canary check before any grading.

Task: build an eval for my product. Judges use a ChatGPT subscription through `codex exec`. The product model uses the OpenAI API.

My inputs:
- Product: <what it is and what behavior to measure>
- How to call it from a script: <command, function, or endpoint>
- Budget cap in dollars: <number>
- Product model: <model name>

Steps:
1. Report the real product entrypoint and the files you will touch.
2. Write the contract. Show it to me.
3. Design the cases, answer keys (computed in code), and splits.
4. Set up and calibrate the judges. Run the controls.
5. Measure the baseline with the smoke, focused, and full runs.
6. Deliver the contract, runner command, dev cases, calibration results, baseline, and a cost estimate. Wait for my approval.

Rules:
- Never print a secret. Check variables with `[ -n "$VAR" ]`.
- Enforce the dollar cap with `scripts/budget.py`.
- Do not deploy, merge, or write to production.

Stop and ask me if:
- I have not approved the contract and cost estimate.
- A calibration control fails.
- The spend reaches the dollar cap.
- The baseline is about 95% or higher. Add harder cases, then ask me.
