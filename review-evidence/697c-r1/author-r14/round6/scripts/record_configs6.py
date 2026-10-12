"""Scratch (after R584-4's record_configs.py): record every configuration the boundary gate judges in a checkout.

Usage: python3 -I record_configs5.py <checkout-root> <out.json> [gate arguments...]

Wraps ctrl_boundary.judged and records, for every unit explored, the side's argument vector, the unit and,
for each configuration, its label, flags, files read, deciding macros and error state; paths normalised (the
checkout root, the gate's temporary directory, stand-ins, the shapes' and contracts' generated directories).
"""
import json
import os
import re
import sys
import threading
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402

temp = re.escape(os.path.realpath(os.environ.get("TMPDIR") or "/tmp"))
lock = threading.Lock()
records = []
orig = cb.judged
WORK = re.compile(temp + r"/ctrl-boundary-[^/\s]+")
VARIANTS = re.compile(temp + r"/ctrl-boundary-variants-[^/\s]+")
STAND = re.compile(r"standins-[^/\s]+")


def norm(s):
    s = str(s).replace(str(root), "<ROOT>")
    s = VARIANTS.sub("<VARIANTS>", s)
    s = WORK.sub("<WORK>", s)
    return STAND.sub("standins-X", s)


def judged(units, argv, space, work, *rest, **kw):
    result = orig(units, argv, space, work, *rest, **kw)
    rows = []
    for unit, seen in result:
        for s in seen:
            rows.append({
                "argv": [norm(a) for a in argv], "unit": norm(unit), "label": s.label,
                "flags": [norm(f) for f in s.flags],
                "deps": sorted(norm(d) for d in s.read.deps),
                "tested": sorted(s.read.tested), "error": norm(s.read.error), "stopped": s.read.stopped})
    with lock:
        records.extend(rows)
    return result


cb.judged = judged
rc = cb.main(sys.argv[3:])
out.write_text(json.dumps({"rc": rc, "records": records}, indent=0, sort_keys=True), encoding="utf-8")
print(f"recorded {len(records)} configurations, rc {rc}")
