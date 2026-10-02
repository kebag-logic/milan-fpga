#!/usr/bin/env python3
"""Compare each campaign arm's measured failing-check count with its README record.

usage: compare_readme.py REPO OUTROOT

REPO is the exact-head tree (its READMEs are the records); OUTROOT holds one
output directory per campaign as the drivers wrote them (results.json) or the
driver's stdout log (receipts/campaigns/NAME.log) for the two patch drivers.
For every arm it prints the measured count, the README record's count (the
first integer of the row's last cell, in the README section the driver owns)
and EQUAL / DIFF / NO-ROW. Arms graded in another suite's README are printed
with that README's matching text for a by-eye check (marked MANUAL).
"""
import json
import re
import sys
from pathlib import Path

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
LOGS = Path(__file__).resolve().parent.parent / "receipts" / "campaigns"


def section(readme, heading):
    text = (REPO / readme).read_text().splitlines()
    start = next(i for i, l in enumerate(text) if l.startswith("#") and heading in l)
    level = len(text[start]) - len(text[start].lstrip("#"))
    end = next((i for i in range(start + 1, len(text))
                if text[i].startswith("#") and len(text[i]) - len(text[i].lstrip("#")) <= level),
               len(text))
    return text[start:end]


def rows(lines):
    out = {}
    for l in lines:
        if not l.startswith("| `"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        names = re.findall(r"`([^`]+)`", cells[0])
        # "`hz-map-as-ro`, `-talker`": a leading-dash name is a suffix of the first
        # (or of a prefix of it: "`hz-stream-key-none-vs-read`, `-talker-read`")
        first, parts, expanded = names[0], names[0].split("-"), [names[0]]
        for n in names[1:]:
            if n.startswith("-"):
                expanded += ["-".join(parts[:k]) + n for k in range(1, len(parts) + 1)]
            else:
                expanded.append(n)
        names = expanded
        n = re.search(r"\d[\d,]*", cells[-1])
        for nm in names:
            out.setdefault(nm, []).append((int(n.group(0).replace(",", "")) if n else None, cells[-1]))
    return out


def from_log(name):
    res = {}
    for l in (LOGS / f"{name}.log").read_text().splitlines():
        m = re.match(r"^(\S+): rc=(-?\d+) failures=(\d+) named=(\d+) (\w+)", l)
        if m:
            res[m.group(1)] = (int(m.group(3)), m.group(5))
    return res


def from_json(d):
    res = {}
    p = OUT / d / "results.json"
    if not p.exists():
        return None
    for r in json.loads(p.read_text()):
        if r.get("verdict") in ("PASS",) and r["mutant"].startswith("golden"):
            continue
        suite = r.get("suite")
        if suite and not suite.startswith("tb/"):
            suite = "tb/pp_top"  # notify_mutants.py records the command; its table is in tb/pp_top
        res[r["mutant"]] = (len(r.get("failing_checks", [])), r.get("verdict"), suite)
    return res


def compare(label, measured, table, suite_filter=None):
    eq = diff = norow = 0
    print(f"== {label}: {len(measured)} arms")
    for name, val in sorted(measured.items()):
        base, _, at = name.partition("@")
        suite = val[2] if len(val) > 2 else "tb/pp_top"
        if suite and suite != "tb/pp_top":
            print(f"  MANUAL {name}: measured {val[0]} ({val[1]}) in {suite}")
            continue
        recs = table.get(base)
        if not recs:
            print(f"  NO-ROW {name}: measured {val[0]} ({val[1]})")
            norow += 1
            continue
        nums = [r[0] for r in recs]
        ok = val[0] in nums and len(set(nums)) == 1
        eq += ok
        diff += not ok
        print(f"  {'EQUAL' if ok else 'DIFF '} {name}: measured {val[0]} ({val[1]}); README {[r[1] for r in recs]}")
    print(f"  -> {eq} equal, {diff} differ, {norow} without a row")
    return diff + norow


bad = 0
PP = "tb/pp_top/README.md"
bad += compare("aecp_dispatch_mutants.py", from_log("disp"),
               rows(section(PP, "AECP dispatch and response negative controls")))
bad += compare("aecp_mutants.py", from_log("aecp"),
               rows(section(PP, "AECP deadline and hazard-class controls")))
for lab, d, head in (("d3_mutants.py", "d3", "D3 negative controls"),
                     ("notify_mutants.py", "notify", "Mutation record: `notify_mutants.py`"),
                     ("acmp_mutants.py", "acmp", "ACMP negative controls")):
    m = from_json(d)
    if m is None:
        print(f"== {lab}: no results.json yet")
        bad += 1
        continue
    bad += compare(lab, m, rows(section(PP, head)))
print(f"TOTAL non-equal pp_top rows: {bad}")
