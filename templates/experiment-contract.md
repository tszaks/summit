# Experiment contract (fill in and get owner approval before any paid run)

Status: DRAFT. A draft is not permission to spend money.

## Target
- Suite name:
- One behavior being measured, and who uses it in production:
- Real entrypoint of the product (the code path users hit):
- Baseline revision (commit or prompt hash):
- Eval command:
- Fast offline test command:

## Metric
- Primary metric, its denominator, and direction:
- Blocking failures (cannot be averaged away): wrong figure, invented fact, privacy leak, unauthorized action
- Smallest improvement worth keeping:
- Regression rule: any case that passes on production and fails on the candidate blocks release
- Product-failure vs infrastructure-failure policy (infra = ungraded, retried, never counted as pass or fail):
- False-rejection policy (correct answer blocked by an over-strict check counts as a product failure and is tracked separately):

## Data
- Where cases came from, and who approved them:
- Grouping unit (conversation, customer, fixture family):
- Splits: development (optimizer sees) / validation (selection) / held-out (final, one look)
- Repetitions per case (more for flaky cases):
- State reset between cases:
- Frozen clock, timezone, fixtures:
- Answer keys: computed by code from fixtures (never typed by hand)

## Judges
- Judge A model and settings:
- Judge B model and settings (different model family or size):
- Pass rule across both judges:
- Disagreement handling: both reasons kept, third look or human adjudication, never silently averaged
- Calibration controls (known-good, known-bad, injection attempt) and the pass bar (all must match):

## Limits
- Editable files:
- Protected files (hash-locked): cases, graders, runner, this contract
- Max rounds / max validation queries / max consecutive non-adoptions:
- Dollar cap enforced by the runner, and the per-call reserve:
- Behavior when usage is unknown (stop; keep the reserve):
- Human approval checkpoints:

## Records
- Ledger path (one row per trial):
- Receipts: raw outputs, verdicts, hashes, cost, error category per attempt
- Owner approval and date:
