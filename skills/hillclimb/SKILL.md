---
name: hillclimb
description: Improve an LLM product against an existing, calibrated eval using small bounded trials, with a runner-enforced dollar cap and a regression-only release rule. Billing-neutral. Use only when explicitly asked to optimize against an eval.
---

# Hillclimb

Method only. Needs a finished eval (see ../build-eval/SKILL.md). Where judges are called, use the judge setup in ../../judges.md. Scripts are in ../../scripts and templates in ../../templates.

## Preconditions
An executable runner, calibrated judges, an allowlist of editable files, finite limits, and an acceptance rule, all in the contract (../../templates/experiment-contract.md). If any is missing, go back to build-eval. If the baseline is about 95% or higher, do not hillclimb; add harder cases.

Keep three roles apart:
- optimizer: you
- target: the product
- controller: runner code. It computes metrics, enforces the cap, owns the judge scripts, and decides acceptance.

Your opinion is not the acceptance rule. Keep judge scripts, instructions, and private cases outside the optimizer's reach. Verify protected-file hashes before every trial. Start in a fresh session that has not seen the private cases.

## Loop
1. Diagnose development failures. Group by cause. Prefer a cause over a one-off patch. Never paste case text or answer keys into the production prompt.
2. One hypothesis, one coherent change, in an allowed file. Do not mix model, prompt, and tool changes.
3. Run offline tests, then the focused development set, then the full set. Use 3 to 5 repetitions on flaky cases.
4. If development clears the screen, the controller runs private validation. Give it the revision only. Count every validation query, rejected candidates included.
5. Compare paired against a fresh baseline on the same cases (models drift). One lucky run is not an improvement.
6. Decide by the contract. Noisy evidence is inconclusive, not a win.

## Failure classes
- Pass.
- Product failure: wrong or malformed answer, the product's own timeout.
- False rejection: a verification layer blocked or rewrote a correct answer. A product failure, counted separately so it is not hidden in "wrong answer".
- Infrastructure failure: network, auth, rate limit, runner, or judge broke. Ungraded; retry on the same saved answer; never rerun the product to get a pass.
- Ungraded: uninterpretable. Kept, never a pass.
Classify with ../../scripts/classify.py.

## Release rule
The only release blocker is regression versus production. A case that passes on production and fails on the candidate blocks release. A case that already fails on production does not block; list it as a known issue. Separate product bugs become tickets, not part of the optimizer's patch.

Reject on: a blocking failure, a changed protected file, missing result rows, an exceeded cap, a changed judge model, or unexplained corruption.

## Budget
Estimate first and show the owner. Enforce with ../../scripts/budget.py: reserve before each paid call, settle after. Unknown usage keeps the reserve charged. Spend survives resumes. Allow only approved models. Hard dollar cap and hard round cap in the contract.

## Experiment contract
Fill in ../../templates/experiment-contract.md before the first paid trial. Append one ledger row per trial: ID, parent and candidate revision, hypothesis, change, hashes, dev and validation summaries, failures, cost, decision and reason. Undo only your own rejected patch and keep its result files.

## Stop
Stop at any of these:
- the success criterion
- the dollar cap
- the round cap
- three non-adoptions in a row (or the number in the contract)
- a blocker

Then list the remaining failures by root cause before you spend more. If the cause is data quality, a missing capability, a product decision, or a broken case, say so and stop.

## Final comparison
Lock one candidate using development and validation only. The controller compares it with the original baseline once on the held-out set. If it fails or is inconclusive, report that; do not choose another candidate from the same held-out feedback and call it untouched.

Hand back: patch, ledger, exact commands, baseline and candidate results, sample sizes, hard-failure counts, cost, limits. Recommend review or no promotion. Leave merge and deploy to the owner.

## Evidence
Keep receipts for every claim. "Tests pass", "merged", and "deployed" are three facts. Do not hide stderr when verifying.
