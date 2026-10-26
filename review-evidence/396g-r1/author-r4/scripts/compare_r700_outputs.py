#!/usr/bin/env python3
"""Compare R700-3's probe outputs from the round-3 planner and from this head.

Usage: python3 -I compare_r700_outputs.py <dir of outputs at round 3> <dir of outputs at this head>

The probes are byte-identical copies of R700-3's published scripts, run from
scratch directories because they write their JSON beside themselves. For
each output: whether it is byte-identical, and every row whose events,
verdict or compound-rule result differ, with channel 2's DUT events.
"""
import hashlib
import json
import pathlib
import sys

base, head = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
for name in ("delta-probes.json", "qualified-probes.json", "boundary-matrix.json", "compound-ambiguity.json"):
    old, new = (base / name).read_bytes(), (head / name).read_bytes()
    print(f"{name}: round3 sha256 {hashlib.sha256(old).hexdigest()} head sha256 {hashlib.sha256(new).hexdigest()} "
          f"{'identical' if old == new else 'differs'}")
    if old == new:
        continue
    for a, b in zip(json.loads(old), json.loads(new)):
        keys = ("verdict", "events", "matches_compound_rule")
        if all(a.get(k) == b.get(k) for k in keys):
            continue
        print(f"  {a['name']}: verdict {a['verdict']} -> {b['verdict']}; "
              f"compound rule {a.get('matches_compound_rule')} -> {b.get('matches_compound_rule')}")
        for label, row in (("round3", a), ("head", b)):
            events = [(e["capture_index"], e["class"], e["n"], e.get("mask"), e.get("located_within"))
                      for e in row["events"] if e["attribution"] == "dut" and e["channel"] == 2]
            print(f"    {label} channel 2: {events}")
