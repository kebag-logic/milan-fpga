#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Set the round-4 sections of the round-5 model's output (sections/*.out)
beside the published round-4 output (meter_rules_model_r4.out, round 4
evidence on PR #631), line by line, section by section.

Round 5 changes one rule the round-4 sections can see: rule 1's deviation
check runs as each PDU arrives, up to a gap, so the PDUs of a loss-voided
group before its gap are checked. Two kinds of line may differ, and each is
checked for exactly that change; any other difference fails:
  S  "in gap" with the step at positions 1 to 14 (the loss at 15): the step
     now voids the group by its deviation (voids 0 -> 1). The design row
     keeps restarts=1 and every other field; the no-check mutant row goes
     from restarts=0 to restarts=1 (the deviation check now catches it), so
     it no longer drops LOCKED (drops=0) and its window error changes.
  T  a case beyond the meter's tolerance, invalid in both (valid=0.0000) and
     restarting in both: more deviation restarts, because the partial
     groups are now checked too.
Usage: compare_r4_r5.py meter_rules_model_r4.out sections_dir"""
import os
import re
import sys

ORDER = ("bound", "regress", "fill", "p1", "loss", "steps", "tol", "fstep",
         "legs", "shapes")


def sections(lines):
    out, cur = {}, None
    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("== "):
            cur = line.split(".")[0][3:]
            out[cur] = [line]
        elif cur is not None and line:
            out[cur].append(line)
    return out


def fields(line):
    return dict(re.findall(r"(\w+)=\s*([-\d.]+)", line))


def expected(sec, x, y):
    fx, fy = fields(x), fields(y)
    if sec == "S":
        m = re.search(r"at pos\s+(\d+), lost pos 15", x)
        if not (x.startswith("in gap") and m and 1 <= int(m.group(1)) <= 14):
            return False
        if x.split(":")[0] != y.split(":")[0]:
            return False
        if fx["voids"] != "0" or fy["voids"] != "1":
            return False
        if fx["lossvoids"] != fy["lossvoids"]:
            return False
        if x.startswith("in gap, mutant no-chk"):
            # caught now, so the step no longer reaches the servo
            return (fx["restarts"] == "0" and fy["restarts"] == "1"
                    and fy["drops"] == "0")
        same = [k for k in fx if k not in ("voids", "restarts")]
        return (all(fx[k] == fy[k] for k in same)
                and fx["restarts"] == fy["restarts"] == "1")
    if sec == "T":
        return (x.split("restarts=")[0] == y.split("restarts=")[0]
                and fx["valid"] == fy["valid"] == "0.0000"
                and int(fx["restarts"]) > 0 and int(fy["restarts"]) > 0
                and fx["lossvoids"] == fy["lossvoids"])
    return False


r4 = sections(open(sys.argv[1]))
r5_lines = []
for name in ORDER:
    r5_lines += open(os.path.join(sys.argv[2], name + ".out")).readlines()
r5 = sections(r5_lines)
bad = 0
for sec in r4:
    la, lb = r4[sec], r5.get(sec)
    if lb is None or len(la) != len(lb):
        print(f"section {sec}: line count differs or section missing")
        bad += 1
        continue
    diff = [(x, y) for x, y in zip(la, lb) if x != y]
    unexp = [d for d in diff if not expected(sec, *d)]
    print(f"section {sec}: {len(la)} lines, identical {len(la) - len(diff)}, "
          f"differing {len(diff)}, of which unexpected {len(unexp)}")
    for x, y in diff:
        tag = "expected" if (x, y) not in unexp else "UNEXPECTED"
        print(f"  {tag}\n    r4: {x}\n    r5: {y}")
    bad += len(unexp)
print(f"round-4 sections compared: {len(r4)}; unexpected differences: {bad}")
sys.exit(1 if bad else 0)
