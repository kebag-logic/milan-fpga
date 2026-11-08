#!/usr/bin/env python3
"""Show that the twin's Milan v1.2 4.3.2 and 4.4.1 checks (twin_grades.grade_mvrp), vacuous in the stimulus,
can fail: a copy of a capture with a first stream frame before VID 2 is declared, and one with a sink settled
while VID 2 is withdrawn.

usage: probe_mvrp_vacuous.py LEG_DIR FABRIC.json
"""
import json
import sys
import tempfile
from pathlib import Path

leg = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(leg))
import twin_decode as td  # noqa: E402
import twin_grades  # noqa: E402

doc = json.loads(Path(sys.argv[2]).read_text())
with tempfile.TemporaryDirectory() as work:
    early = dict(doc, first_stream_ms=1000)
    path = Path(work) / "early.json"
    path.write_text(json.dumps(early))
    found, _ = twin_grades.grade_mvrp(td.load(path))
    print("first stream frame at 1000 ms (VID 2 declared from 5200 ms):", found or "NOTHING")
    cap = td.load(Path(sys.argv[2]))
    found, measured = twin_grades.grade_mvrp(cap)
    print("unplanted fabric capture:", found or "no finding", "| settled sinks:", measured["settled_sinks_ms"])
