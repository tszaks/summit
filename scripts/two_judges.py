#!/usr/bin/env python3
"""Two independent judges over the OpenAI API, with calibration controls.

Fill in call_judge() with your own client call. It must return the parsed JSON grade
(see templates/grader-schema.json) plus the usage/cost the API reported. Keep this file
outside the optimizer's reach. Run `python two_judges.py controls controls.json case.json`
before trusting any score.
"""
import json, os, sys

JUDGES = ["JUDGE_A_MODEL", "JUDGE_B_MODEL"]  # two different models; set real names

def is_claude(model):
    return any(s in model.lower() for s in ("claude", "anthropic"))

def check_billing(model):
    """Claude judges run on an Anthropic API key only, never a Claude subscription
    (claude -p, Claude Code): Anthropic bans accounts for that. See judges.md."""
    if is_claude(model) and not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError(f"{model} is a Claude judge: set ANTHROPIC_API_KEY. "
                           "Never fall back to a Claude subscription.")

def call_judge(model, prompt):
    raise NotImplementedError("wrap your API client here; use structured output with the schema")

def passes(g):
    return (all(g[k] >= 3 for k in ("correctness", "grounding")) and not g["criticalFailures"])

def grade_both(prompt):
    for m in JUDGES:
        check_billing(m)
    out ={m: call_judge(m, prompt) for m in JUDGES}
    verdicts = {m: passes(r["grade"]) for m, r in out.items()}
    return {"passed": all(verdicts.values()), "disagree": len(set(verdicts.values())) > 1,
            "judges": out}

def run_controls(controls, case, build_prompt):
    """Every control must come out as expected, on BOTH judges, twice. One miss blocks the run."""
    bad = []
    for c in controls:
        for _ in range(2):
            out = grade_both(build_prompt(case, c["answer"]))
            for m, r in out["judges"].items():
                if passes(r["grade"]) != c["expect_pass"]:
                    bad.append({"control": c["name"], "judge": m})
    return bad

if __name__ == "__main__":
    print(__doc__)
    print("This file is a template: implement call_judge() and import grade_both / run_controls from your runner.")
