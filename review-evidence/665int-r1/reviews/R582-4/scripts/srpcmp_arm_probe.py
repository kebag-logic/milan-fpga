#!/usr/bin/env python3
"""Reviewer probe (R582-4) of the firmware gate's srpcmp arm (ctrl_arms.arm_srpcmp).

Runs the arm against the tracked srp_wire_compare.py and against stand-in
comparators written under <scratch>, each a way the self-test can report a
failure or rot, and prints whether the arm fails it.
Usage: python3 -I -B srpcmp_arm_probe.py <checkout> <scratch-dir>
"""
import json
import sys
from pathlib import Path

tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_arms  # noqa: E402

GOOD = {"packing_only": "PASS", "within_opportunity_order": "PASS", "frame_grouping": "PASS",
        "zero_padding": "PASS", "five_value_vector": "PASS"}


def stub(name: str, body: str) -> Path:
    p = scratch / f"{name}.py"
    p.write_text("import sys, json\n" + body + "\n", encoding="utf-8")
    return p


CASES = [
    ("tracked comparator", None, 0),
    ("non-zero exit", stub("rc1", "print('boom'); sys.exit(1)"), 1),
    ("a control reported FAIL with exit 0",
     stub("ctlfail", f"c={GOOD!r}; c['frame_grouping']='FAIL'; c['plants']=[{{'plant':'x'}}];"
                     "print(json.dumps({'controls': c}))"), 1),
    ("no plant reported, exit 0",
     stub("noplant", f"c={GOOD!r}; c['plants']=[]; print(json.dumps({{'controls': c}}))"), 1),
    ("unreadable report, exit 0", stub("garbage", "print('not json')"), 1),
    ("report without plants key, exit 0", stub("nokey", f"print(json.dumps({{'controls': {GOOD!r}}}))"), 1),
]
bad = 0
for what, path, want in CASES:
    if path is not None:
        ctrl_arms.SRP_COMPARE = path
    else:
        ctrl_arms.SRP_COMPARE = tree / "sw/firmware/ctrl/test/srp_wire_compare.py"
    out = ctrl_arms.arm_srpcmp()
    got = 1 if out.rc else 0
    ok = got == want
    bad += not ok
    first = out.log.strip().splitlines()[0] if out.log.strip() else ""
    print(f"[{'ok' if ok else 'BAD'}] {what}: arm rc {out.rc} (want {'fail' if want else 'pass'}) :: {first[:140]}")
print(f"srpcmp arm probe: {bad} unexpected of {len(CASES)}")
sys.exit(1 if bad else 0)
