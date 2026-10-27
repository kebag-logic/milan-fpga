#!/usr/bin/env python3
"""Show one fuzz seed's composition and verdict under one named release control.

Usage: python3 -B show_mutant_seed.py <tb/tools dir> <work dir> <seed> <defect name>

Applies the named control from the driver's table to a copy of the planner in
<work dir>, then prints the seed's DUT events, the verdict and the events the
mutated grader lists, with their attribution.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

tools, work, seed, name = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(tools))
spec = importlib.util.spec_from_file_location("release_mutants", tools / "torture_release_mutants.py")
table = importlib.util.module_from_spec(spec)
spec.loader.exec_module(table)
_, old, new, test = next(m for m in table.MUTANTS if m[0] == name)
text = (tools / "torture_campaign.py").read_text()
assert text.count(old) == 1
work.mkdir(parents=True, exist_ok=True)
(work / "torture_campaign.py").write_text(text.replace(old, new))
sys.path.insert(0, str(work))
import torture_campaign as m  # noqa: E402
assert Path(m.__file__).parent == work.resolve()
T = type("T", (m._ReleaseGateChecks, unittest.TestCase), {})
t = T(test)
units = t._fuzz_units(16384, seed)
print(f"control: {name}\nseed {seed}:")
for kind, at, channels, span, events in units:
    first = {k: (f"0x{v:08X}" if k == "mask" else v) for k, v in events[0].items()}
    print(f"  {kind} at {at}, channels {channels}, {span} word(s): {first}")
verdict, detail, _ = t._sweep_grade(16384, [e for u in units for e in u[4]])
print(f"verdict {verdict}: {detail['why']}; missed {[a['index'] for a in detail['planted_missed']]}")
for e in detail["events"]:
    if abs(e["capture_index"] - units[0][1]) <= 70:
        print(f"  ch{e['channel']} {e['capture_index']} {e['class']} {e['n']} {e.get('mask', '')} {e['attribution']}")
