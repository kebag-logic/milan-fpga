#!/usr/bin/env python3
"""logcmp4.py A B [--multiset]: round 3's logcmp.py normalisation plus round 4's host text.

Added to round 3's masks (tools/logcmp.py, imported unchanged):
- the clone's own directory under r4/wt/<name> (the two arms are two clones);
- a mutant staging directory: tempfile's random name at the base, the stable
  milan-mutant-stage-<uid>/<prefix><slot> at the head (the change under test moves it);
- the wall-clock fields of milan_dp's RENDER-PHASE timing records ("t_s", "elapsed_s").
--multiset compares the sorted lines (a suite whose arms print as they finish, at base too).
"""
import importlib.util
import re
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "logcmp", "$MANAGEMENT/2026-09-23/cicd-a839/round3/receipts/tools/logcmp.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
EXTRA = [
    (re.compile(r'/data-2/milan/tmp/cicd-a839/r4/wt/[A-Za-z0-9_]+'), '<CLONE>'),
    (re.compile(r'/data-2/milan/tmp/cicd-a839/r4/tmp/(milan-mutant-stage-\d+/)?[A-Za-z0-9_.-]+'), '<STAGE>'),
    (re.compile(r'"(t_s|elapsed_s|wall_s|idle_s|seconds)": [0-9.]+'), r'"\1": <T>'),
]


def norm(path):
    """EXTRA on the raw lines, then round 3's drops and masks, unchanged."""
    out = []
    for line in open(path, errors="replace").read().splitlines():
        for p, r in EXTRA:
            line = p.sub(r, line)
        if any(p.search(line) for p in base.DROP):
            continue
        for p, r in base.SUBS:
            line = p.sub(r, line)
        out.append(line)
    return out


def main():
    a, b = norm(sys.argv[1]), norm(sys.argv[2])
    if "--multiset" in sys.argv:
        a, b = sorted(a), sorted(b)
    if a == b:
        print(f"IDENTICAL ({len(a)} normalised lines)")
        return 0
    import difflib
    for line in list(difflib.unified_diff(a, b, lineterm="", n=0))[:12]:
        print(line[:200])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
