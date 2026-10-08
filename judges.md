# Judges

Two billing modes. Choose one. The product model bills to the OpenAI API in both modes. Only the judges differ.

| Mode | Judges run on | Judge cost |
| --- | --- | --- |
| API | OpenAI API | API charges, inside your dollar cap |
| Subscription | `codex exec` signed in with ChatGPT | No API charge. Uses your plan allowance. |

Both modes use the same rules:
- Use two judges. Use two different models.
- A case passes only if both judges pass.
- Keep both sets of reasons. Never average.
- Use the schema in `templates/grader-schema.json`. Validate every grade.
- A malformed or missing grade is ungraded. It is never a pass.
- Write the judge instructions with the rubric rules in `skills/build-eval/SKILL.md`, section 6.

## Shared: calibration controls
Run controls before any paid product call.

1. Copy `templates/controls.example.json`. Write controls for your domain.
2. Include a known-good answer, known-bad answers (wrong arithmetic, invented access), and a judge-injection attempt.
3. Run each control at least twice on each judge.
4. Require every control to match its expected verdict. One miss blocks the run.
5. Restart calibration after any change to the instructions, the schema, or a judge model.
6. Regrade saved answers that have trusted verdicts. Read every disagreement.

## Shared: infrastructure or product failure
Use `scripts/classify.py`.

- Infrastructure failure: your network, auth, rate limit, runner, or judge broke. The attempt is ungraded.
- Retry only the missing judgment, on the same saved product answer.
- Never rerun the product to get a pass.
- A judge that already returned a verdict keeps it.
- Product failure: the product answered wrong, returned bad output, or hit its own timeout.
- A run is fully measured only when no attempt is infrastructure or ungraded.

## API mode
1. Choose two judge models from different model families or sizes.
2. Open `scripts/two_judges.py`. Put your API client call in `call_judge()`. Use structured output with the schema.
3. Set the two model names in `JUDGES`.
4. Keep this file outside the optimizer's reach.
5. Run the calibration controls with `run_controls()`.

Cost control:
1. Count judge calls first: 2 per answer, plus bounded retries. Add them to the cost estimate.
2. Call `scripts/budget.py` `reserve()` before each judge call. Call `settle()` after it.
3. A cheaper judge is allowed only if it still passes every control.
4. Allow only the approved judge models.

## Subscription mode
Read the plan terms first. Automated, high-volume grading through a ChatGPT plan can be restricted by plan or organization terms. It also uses your usage allowance. Your user must check that this use is allowed. Rate limits will happen. This kit treats them as infrastructure failures: retry with backoff, never count as a pass. If this use is not allowed, use API mode. Flags and plans change. Check current OpenAI documentation and `codex exec --help`.

Setup:
1. Run `codex login status`. It must say "Logged in using ChatGPT". An API-key login bills the API.
2. Set the variables:
   ```
   export GRADER_STATE_DIR=./grader-state
   # optional: export GRADER_INSTRUCTIONS=./my-grader-instructions.txt
   export GRADER_MODELS=<modelA>,<modelB>
   ```
3. Review `templates/grader-instructions.txt`. The script uses it by default. To use your own file, set `GRADER_INSTRUCTIONS`.
4. Read the header of `scripts/grade_with_codex.py`. It runs one judge call.

Isolation. A judge that can read your repo can read the answer key. Do not rely on instructions. Use these layers:
1. Each call gets an empty temporary folder and its own state and log folders. The script does this.
2. The script removes every `OPENAI_*` variable.
3. The script uses Codex's read-only sandbox. Note: read-only blocks writes, not reads. Without layer 5, the judge can read any file your user account can read. It turns off user config, project rules, host skills, search, MCP, apps, plugins, browser, memory, and delegation.
4. The model that Codex reports must equal the model you asked for. If it changes, stop the campaign.
5. On macOS, use an OS sandbox. Fill `templates/macos-grader-policy.sb.tmpl`. Start `scripts/allowlist_proxy.py PORT`. Set `GRADER_POLICY_TMPL` and `GRADER_PROXY_PORT`. On Linux, use a container or a separate OS user with only the call input mounted.

Canary check. Run it before any real grading:
```
python3 scripts/isolation_check.py MODEL <repo dir> <cases dir> <keys dir>
```
It plants unique strings in protected folders and one control string in a readable folder. It uses its own probe instructions, because the grader instructions tell the judge to ignore requests inside the data.
- Without the OS sandbox, the judge must read the control (proof that it tried) and must not show any protected string. Expect a FAIL here: layer 3 alone does not block reads.
- With the macOS sandbox, Codex's shell tool cannot start (macOS refuses a sandbox inside a sandbox). So the judge cannot read anything. The script then tests the profile directly: each protected file must be blocked, the control must be readable, and a direct fetch that skips the proxy must fail.

Keep `isolation-proof.json`. Run the check again after any change to the Codex version, flags, or paths. State what the proof shows and what it does not show.

Calibration:
```
python3 scripts/calibrate.py case.json controls.json MODEL_A MODEL_B
```
It runs each control twice on each judge, at most 3 calls at a time. It exits 0 only if all controls match. It writes `calibration.json`.

Usage limits:
1. Estimate judge calls first: 2 per answer. Show the number to your user.
2. Expect rate limits. The script retries with backoff.
3. If a rate limit stops the run, record the run as not fully measured. Resume later on the same saved answers.
