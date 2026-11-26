#!/usr/bin/env python3
"""Recompute the changed figure and retained campaign evidence without builds."""
from collections import Counter
import json
from pathlib import Path
import re
import sys
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.path[:0] = [str(root / "scripts"), str(root / "sw/firmware/ctrl/test")]
import suite_shards
import ci_events
import ctrl_configs

r1 = packet / "scratch/cicd4-r1/author/receipts"
r2 = packet / "scratch/cicd4-r2/author/receipts"
for path, expected in ((r1 / "hosted/45735453538-gptp-worker.log",672),
                       (r2 / "hosted/gptp/45755846909-22of27.log",679)):
    text = path.read_text()
    normalized = text if "\t" in text.splitlines()[0] else "\n".join("worker\tstep\t"+line for line in text.splitlines())
    measured = suite_shards.measure_log(normalized)
    assert measured.seconds["gptp_shadow"] == expected
    assert "3ce71b768a2f6f6a5274c127080146e755d02275" in text
    print(f"PASS {path.name}: gptp_shadow {expected} s, pin 3ce71b76")

def normalize(path, serial=False):
    lines = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if serial:
            match = re.match(r"\ufeff?\d{4}-\d\d-\d\dT[\d:.]+Z (.*)$", line.split("\t",2)[-1])
            if match and not match[1].startswith("[endstation_builder] WARNING"):
                lines.append(match[1])
        elif " " in line:
            lines.append(line.split(" ",1)[1])
    records = []
    for index, line in enumerate(lines):
        if re.match(r"\[(ok|ESCAPED|BAD)\] ",line):
            following = lines[index+1] if index+1 < len(lines) else ""
            records.append(line + ("\n"+following if following.startswith("    first:") else ""))
    assert all(line.startswith("[ok]") for line in records)
    return records

for phase, count in (("control",844),("aecp",398),("srp",662)):
    serial = normalize(r1 / f"reference/45657606423-firmware-{phase}-mutants.log", True)
    legs = sorted((r1 / "local/control").glob("leg*.log")) if phase == "control" else sorted((r1 / "local/aecp-srp").glob(phase+"-leg*.log"))
    records = [normalize(p) for p in legs]
    if phase == "srp":
        controls = [x for x in serial if x.startswith("[ok] lwSRP pin,")]
        assert len(controls) == 2
        for leg in records:
            assert [x for x in leg if x.startswith("[ok] lwSRP pin,")] == controls
        serial = [x for x in serial if x not in controls]
        records = [[x for x in leg if x not in controls] for leg in records]
    actual = sum(records,[])
    assert len(serial) == count and Counter(serial) == Counter(actual)
    print(f"PASS historical {phase} verdicts including first-failure details: {count}, leg sizes {[len(x) for x in records]}")

texts = ctrl_configs.builder_texts()
known = {b.path for b in ctrl_configs.BUILDERS}
unlisted = [ctrl_configs.rel(p) for p,t in texts.items() if ctrl_configs.program(p,t)
            and ctrl_configs.rel(p) not in known | set(ctrl_configs.OUTSIDE) | set(ctrl_configs.PART_OF) | set(ctrl_configs.SUITES)]
assert not unlisted, unlisted
name = "scripts/ci_fast_legs_selftest.py"
assert name in ctrl_configs.OUTSIDE and any(ctrl_configs.rel(p)==name for p in texts)
print("PASS firmware boundary text classification, with actual self-test dispatch stood in for")

original = ci_events.check_fast_legs
def without_count(c, wf):
    before = len(c.findings)
    original(c,wf)
    c.findings[before:] = [x for x in c.findings[before:] if "matrix's leg count" not in x]
world = ci_events.parse_world(ci_events.read_tree(root))
with patch.object(ci_events,"check_fast_legs",without_count):
    found = []
    for name, mutate, wanted in ci_events._fast_leg_arms():
        if "command counts one leg more" not in name:
            continue
        import copy
        changed = copy.deepcopy(world); mutate(changed)
        c = ci_events.Contract(); ci_events.check_fast_legs(c,changed[ci_events.RTL_FAST])
        assert not any(wanted in f for f in c.findings)
        found.append(name)
    assert len(found) == 3
print("PASS killing control: removing count checks makes all three COUNT+1 planted-arm assertions fail")

comments = json.loads((packet / "scratch/cicd4-r1/author/pr1003.json").read_text())["comments"]
for comment in comments:
    body = comment["body"]
    if body.startswith("[A10]") and ("#1008" in body or "1,377" in body) and "STARTED" not in body:
        print("PUBLIC SCOPE",comment["url"],body)
