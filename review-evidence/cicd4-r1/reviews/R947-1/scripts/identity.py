#!/usr/bin/env python3
"""Compare the serial hosted campaign verdict lines with the union of the local campaign legs' lines.
Usage: identity.py <receipts-dir>   (the published author receipts directory)
A verdict line is any line whose message starts with a bracketed verdict ([ok], [ESCAPED], [BAD], ...),
with the 'first:' line that follows it joined on; the summary lines are listed separately."""
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
HOSTED = re.compile(r"^[^\t]*\t[^\t]*\t\d{4}-\d\d-\d\dT[\d:.]+Z ?(.*)$")
LOCAL = re.compile(r"^\d+\.\d+ ?(.*)$")
VERDICT = re.compile(r"^\[(ok|ESCAPED|BAD|FAIL|PASS|ok   )\] ")
SUMMARY = re.compile(r"^(mutants: |test_ctrl_firmware: |PASS: \d+ live defects|.*caught\b)")


def messages(path, pattern):
    out = []
    for line in path.read_text(errors="replace").splitlines():
        m = pattern.match(line)
        if m:
            out.append(m.group(1).rstrip())
    return out


def verdicts(msgs):
    rows, summary = [], []
    for i, msg in enumerate(msgs):
        if VERDICT.match(msg):
            # the 'first:' line, skipping interleaved stderr noise, up to the next verdict line
            nxt = ""
            for later in msgs[i + 1:i + 200]:
                if VERDICT.match(later):
                    break
                if later.strip().startswith("first:"):
                    nxt = later.strip()
                    break
            rows.append(msg + (" || " + nxt if nxt else ""))
        elif SUMMARY.match(msg):
            summary.append(msg)
    return rows, summary


PHASES = {
    "control": ("reference/45657606423-firmware-control-mutants.log",
                [f"local/control/leg{k}.log" for k in range(4)]),
    "aecp": ("reference/45657606423-firmware-aecp-mutants.log",
             [f"local/aecp-srp/aecp-leg{k}.log" for k in range(2)]),
    "srp": ("reference/45657606423-firmware-srp-mutants.log",
            [f"local/aecp-srp/srp-leg{k}.log" for k in range(2)]),
}
for phase, (serial, legs) in PHASES.items():
    s_rows, s_sum = verdicts(messages(root / serial, HOSTED))
    leg_rows = []
    print(f"== {phase}")
    print(f"serial: {len(s_rows)} verdict lines; summaries {s_sum}")
    for leg in legs:
        rows, summ = verdicts(messages(root / leg, LOCAL))
        leg_rows.append(rows)
        print(f"{leg}: {len(rows)} verdict lines; summaries {summ}")
    union = Counter(r for rows in leg_rows for r in rows)
    serial_c = Counter(s_rows)
    only_serial = serial_c - union
    only_legs = union - serial_c
    print(f"union of legs {sum(union.values())} lines; identical multiset: {not only_serial and not only_legs}")
    for r, n in sorted(only_serial.items()):
        print(f"  only serial x{n}: {r[:220]}")
    for r, n in sorted(only_legs.items()):
        print(f"  only legs x{n}: {r[:220]}")
    not_ok = [r for r in union if not r.startswith("[ok]")]
    print(f"non-[ok] verdict lines in legs: {len(not_ok)}")
    # lines that occur in every leg (the controls) and lines that occur in more than one leg
    common = set(leg_rows[0]).intersection(*map(set, leg_rows[1:]))
    print(f"lines present in every leg (controls): {len(common)}")
    for r in sorted(common):
        print(f"  every leg: {r[:200]}")
