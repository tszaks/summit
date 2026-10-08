#!/usr/bin/env python3
"""Runner-enforced dollar cap with per-call reserves.

The runner, not the agent, owns this file. Pattern:
  1. reserve(worst_case) BEFORE every paid call. If it would pass the cap, stop.
  2. settle(call_id, actual) after the call, using the usage the API returned.
  3. If usage is unknown (timeout, crash), the reserve STAYS charged. Never refund a guess.
State is one JSON file, written atomically, so a crash or resume never resets spend.
"""
import json, os, tempfile, threading, uuid

class Budget:
    def __init__(self, path, cap_usd):
        self.path, self.cap, self.lock = path, cap_usd, threading.Lock()
        if not os.path.exists(path):
            self._save({"cap": cap_usd, "spent": 0.0, "held": {}, "stopped": None})

    def _load(self):
        with open(self.path) as f:
            return json.load(f)

    def _save(self, s):
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(self.path)))
        with os.fdopen(fd, "w") as f:
            json.dump(s, f, indent=2)
        os.replace(tmp, self.path)

    def reserve(self, worst_case_usd):
        with self.lock:
            s = self._load()
            if s["stopped"]:
                raise RuntimeError("budget stopped: " + s["stopped"])
            total = s["spent"] + sum(s["held"].values()) + worst_case_usd
            if total > s["cap"]:
                s["stopped"] = "cap would be exceeded"
                self._save(s)
                raise RuntimeError("budget cap reached")
            call_id = uuid.uuid4().hex
            s["held"][call_id] = worst_case_usd
            self._save(s)
            return call_id

    def settle(self, call_id, actual_usd):
        with self.lock:
            s = self._load()
            s["held"].pop(call_id, None)
            s["spent"] += actual_usd
            self._save(s)

    def report(self):
        s = self._load()
        return {"cap": s["cap"], "spent": s["spent"], "held_unknown": sum(s["held"].values())}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__ + "\nUsage: python budget.py STATE_FILE CAP_USD   (prints spend report)\nIn code: from budget import Budget; b = Budget(path, cap)")
        sys.exit(0)
    print(json.dumps(Budget(sys.argv[1], float(sys.argv[2])).report()))
