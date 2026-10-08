#!/usr/bin/env python3
"""Calibration gate for two subscription judges.

Usage: python calibrate.py CASE_PAYLOAD.json CONTROLS.json MODEL_A MODEL_B
CASE_PAYLOAD.json holds the case question, evidence and rubric (everything except the answer).
Each control (known-good, known-bad, injection) runs twice on each judge, max 3 at a time.
Stops at the first mismatch or ungraded call. Writes calibration.json. Exit 0 only if ALL match.
"""
import concurrent.futures as cf, json, pathlib, sys
if len(sys.argv) < 5 or sys.argv[1] in ("-h", "--help"):
    print(__doc__)
    sys.exit(0)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import grade_with_codex as g

case = json.loads(pathlib.Path(sys.argv[1]).read_text())
controls = json.loads(pathlib.Path(sys.argv[2]).read_text())
models = sys.argv[3:5]
jobs = [(m, c, rep) for c in controls for rep in (1, 2) for m in models]
rows, stop = [], None


def run(job):
    m, c, rep = job
    r = g.grade_with_backoff(m, {**case, "answer": c["answer"]}, f"calibration:{c['name']}:{rep}")
    r.update(control=c["name"], expected=c["expect_pass"],
             matched=r["status"] == "graded" and r["passed"] == c["expect_pass"])
    return r


with cf.ThreadPoolExecutor(max_workers=3) as pool:
    for r in pool.map(run, jobs):
        rows.append(r)
        if not r["matched"] and not stop:
            stop = "ungraded" if r["status"] != "graded" else "verdict mismatch"
ok = len(rows) == len(jobs) and all(r["matched"] for r in rows)
pathlib.Path("calibration.json").write_text(json.dumps({"complete": True, "matched": ok,
                                                        "stopped": stop, "rows": rows}, indent=2))
print(json.dumps({"matched": ok, "stopped": stop, "calls": len(rows)}))
sys.exit(0 if ok else 1)
