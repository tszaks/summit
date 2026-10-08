#!/usr/bin/env python3
"""Sort every attempt into one of four buckets. Only the first two count in the score.

  pass            product answered, judges (and code checks) agree it is right
  product_fail    product answered wrong, timed out under its own deadline, or returned
                  malformed output; or a verification layer rejected a correct answer
                  (tag these 'false_rejection' so they stay visible)
  infra           our harness, network, auth, rate limit, or judge broke. UNGRADED.
                  Retry on the SAME saved product answer. Never rerun the product to get a pass.
  ungraded        any record you cannot interpret. Kept as evidence, never scored as pass.
"""
def classify(attempt):
    if attempt.get("infra_error"):
        return "infra"
    if attempt.get("judge_status") not in (None, "graded") or attempt.get("record_invalid"):
        return "ungraded"
    if attempt.get("product_error") or attempt.get("product_timeout"):
        return "product_fail"
    if attempt.get("false_rejection"):
        return "product_fail"
    return "pass" if attempt.get("passed") else "product_fail"

def score(attempts):
    buckets = {"pass": 0, "product_fail": 0, "infra": 0, "ungraded": 0}
    false_rejections = 0
    for a in attempts:
        buckets[classify(a)] += 1
        false_rejections += bool(a.get("false_rejection"))
    measured = buckets["pass"] + buckets["product_fail"]
    return {**buckets, "false_rejections": false_rejections, "measured": measured,
            "rate": buckets["pass"] / measured if measured else None,
            "fully_measured": buckets["infra"] == 0 and buckets["ungraded"] == 0}


if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__ + "\nUsage: python classify.py ATTEMPTS.json   (a JSON list of attempt records)\n"
              "Prints the score summary. Recognized keys: infra_error, judge_status, record_invalid,\n"
              "product_error, product_timeout, false_rejection, passed.")
        sys.exit(0)
    print(json.dumps(score(json.load(open(sys.argv[1])))))
