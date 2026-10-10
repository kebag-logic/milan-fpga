#!/usr/bin/env python3
"""Dump every control-campaign plant of one tree: name, the file it plants into, old, new (JSON on stdout).
usage: plant_dump.py <repo>"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
import ctrl_mutants  # noqa: E402
import ctrl_build  # noqa: E402
prefix = getattr(ctrl_build, "STACK_PREFIX", None)
rows = []
for m in ctrl_mutants.MUTANTS:
    if prefix and m.path.startswith(prefix):
        f = ctrl_build.STACK / m.path.removeprefix(prefix)
    else:
        f = ctrl_build.CTRL / m.path
    rows.append({"name": m.name, "path": m.path, "file": str(f), "old": m.old, "new": m.new,
                 "kills": [list(k) for k in m.kills()]})
json.dump(rows, sys.stdout)
