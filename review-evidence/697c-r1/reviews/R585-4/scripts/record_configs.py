#!/usr/bin/env python3
"""Record every configuration the TSN stack boundary gate judges on the checkout.

Usage: python3 -I record_configs.py <tree> <out.json> [jobs]

Imports sw/firmware/ctrl/test/ctrl_boundary.py from <tree>, wraps its explore()
so every (side argv, unit) -> [(flags, label, deps, tested, error, stopped)] is
recorded, runs judge() on the tree's own checkout (no self-test), and writes the
normalized record plus the findings. Paths are normalized so two trees compare.
"""
import json
import re
import sys
import tempfile
import time
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402

cb.JOBS = jobs
work = Path(tempfile.mkdtemp(prefix="rec-"))
TMP = re.compile(r"/tmp/(?:ctrl-boundary-variants-|rec-|c-library-)[^/\s]*")
STANDIN = re.compile(r"standins-[^/\s]*")


def norm(s):
    s = str(s).replace(str(work), "<WORK>").replace(str(tree), "<ROOT>")
    return STANDIN.sub("standins-X", TMP.sub("<TMP>", s))


record = {}
orig = cb.explore


def explore(argv, unit, space, w, *rest, **kw):
    seen = orig(argv, unit, space, w, *rest, **kw)
    key = norm(" ".join(argv)) + " || " + norm(unit)
    rows = sorted([norm(" ".join(s.flags)), s.label, sorted(norm(d) for d in s.read.deps),
                   sorted(s.read.tested), norm(s.read.error), bool(s.read.stopped)] for s in seen)
    record.setdefault(key, []).append(rows)
    return seen


cb.explore = explore
rv32 = cb.fw_rv32.compiler()
t0 = time.time()
findings = cb.judge(cb.Trees(cb.CTRL, cb.STACK), rv32, work / "checkout")
dt = time.time() - t0
configs = sum(len(r) for v in record.values() for r in v)
json.dump({"tree": norm(tree), "rv32": bool(rv32), "seconds": round(dt, 1), "findings": findings,
           "explorations": len(record), "configurations": configs,
           "record": dict(sorted(record.items()))}, out.open("w"), indent=1, sort_keys=True)
print(f"{tree.name}: {len(record)} explorations, {configs} configurations, {len(findings)} findings, {dt:.1f}s")
