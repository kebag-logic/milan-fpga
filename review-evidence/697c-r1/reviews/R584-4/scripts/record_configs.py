#!/usr/bin/env python3
"""Record every configuration the TSN stack boundary gate judges in a checkout (no self-test).

Usage: python3 -I record_configs.py <checkout-root> <out.json> [--rv32]

Wraps ctrl_boundary.judged (present at both d1b22e80 and e07b3054) and records, for every unit it
explores, the side's argument vector, the unit and, for each configuration, its label, flags, the files
it read, the deciding macros, and its error/#error state. Paths are normalised (checkout root, the
gate's temporary directory, stand-in directories) so two checkouts at different places compare.
"""
import json
import re
import sys
import threading
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402

lock = threading.Lock()
records = []
orig = cb.judged
TMP = re.compile(r"/tmp/ctrl-boundary-[^/\s]+")
STAND = re.compile(r"standins-[^/\s]+")


def norm(s):
    s = str(s).replace(str(root), "<ROOT>")
    s = TMP.sub("<WORK>", s)
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
rc = cb.main(["--require-rv32"])
out.write_text(json.dumps({"rc": rc, "records": records}, indent=0, sort_keys=True), encoding="utf-8")
print(f"recorded {len(records)} configurations, rc {rc}")
