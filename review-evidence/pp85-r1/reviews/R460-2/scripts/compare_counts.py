#!/usr/bin/env python3
"""Compare each campaign arm's failure count with its README row and a prior campaign.

usage: compare_counts.py README CAMPAIGN_LOG [PRIOR_CAMPAIGN_LOG]
rc 0 iff every arm is KILLED and its count equals the leading number of its
README row's "Failing checks" cell.
"""
import re
import sys


def readme_counts(path):
    rows = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\| `([a-z0-9-]+)` \| [^|]+ \|[^|]+\| (\d+)", line)
        if m:
            rows[m.group(1)] = int(m.group(2))
    return rows


def campaign(path):
    arms = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"([a-z0-9-]+): rc=(\d+) failures=(\d+) named=(\d+) (\w+)", line)
        if m:
            arms[m.group(1)] = (int(m.group(3)), m.group(5))
    return arms


readme = readme_counts(sys.argv[1])
now = campaign(sys.argv[2])
prior = campaign(sys.argv[3]) if len(sys.argv) > 3 else {}
bad = 0
for arm, (n, verdict) in now.items():
    want = readme.get(arm)
    was = prior.get(arm, (None, None))[0]
    ok = verdict == "KILLED" and want == n
    bad += not ok
    delta = "" if was is None else ("" if was == n else f"  (prior {was} -> {n})")
    print(f"{'OK ' if ok else 'BAD'} {arm}: campaign {n} {verdict}, README {want}{delta}"
          + ("" if arm in prior or not prior else "  (new arm)"))
missing = sorted(set(readme) - set(now))
print(f"arms {len(now)}, README rows {len(readme)}, README rows not run: {missing}")
print("ALL MATCH" if not bad and not missing else f"{bad} MISMATCH")
sys.exit(1 if bad or missing else 0)
