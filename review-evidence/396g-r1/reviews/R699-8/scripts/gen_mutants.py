#!/usr/bin/env python3
"""Write the probe mutants into <scratch>/m/<name>/torture_campaign.py from the head planner.

usage: gen_mutants.py <repo> <scratch>
m298: control #298 exactly as tb/tools/torture_release_audio_mutants.py states it.
s64/s63: DUT slip listings on channel 3 moved 64 / 63 samples later (capture_index and located_within).
"""
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "tb/tools"))
from torture_release_audio_mutants import AUDIO_GRADER_MUTANTS  # noqa: E402

text = (repo / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
name, old, new, test = AUDIO_GRADER_MUTANTS[-1]
print("m298:", name, "->", test)
anchor = "    refusal, missed = _audio_attribute(events, log, counter_channels, scan)\n"
assert old == anchor and text.count(anchor) == 1
def shift(k):
    return anchor + (
        "    for e in events:\n"
        '        if e["attribution"] == "dut" and e["channel"] == 3 and e["class"] in ("dropped", "repeated"):\n'
        f'            e["capture_index"] += {k}\n'
        '            if "located_within" in e:\n'
        f'                e["located_within"] = tuple(v + {k} for v in e["located_within"])\n')
for d, n in (("m298", new), ("s64", shift(64)), ("s63", shift(63))):
    (scratch / "m" / d / "torture_campaign.py").write_text(text.replace(anchor, n), encoding="utf-8")
    print("wrote", d)
