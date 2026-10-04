#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare a campaign's per-arm failing-check counts with the README mutation records.

Usage: compare_counts.py (--json RESULTS.json | --log LOG) TREE
A README row is `| `name`[, `-suffix` ...] | ... | N...`: N is the leading integer of
the row's last cell, and `-suffix` names expand to <name><suffix>. An arm named
`x@suite` is looked up in tb/<suite>/README.md first, then in every README.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*(`[\w-]+`(?:\s*,\s*`-[\w-]+`)*)\s*\|")


def records(readme: Path) -> dict[str, int]:
    out: dict[str, int] = {}
    for line in readme.read_text().splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        lead = re.match(r"(\d[\d,]*)", cells[-1]) if len(cells) >= 3 else None
        if not lead:
            continue
        names = re.findall(r"`([\w-]+)`", m.group(1))
        base = names[0]
        for n in names:
            out.setdefault(base + n if n.startswith("-") else n, int(lead.group(1).replace(",", "")))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--json", type=Path)
    g.add_argument("--log", type=Path)
    ap.add_argument("tree", type=Path)
    a = ap.parse_args()
    per_suite = {p.parent.name: records(p) for p in sorted(a.tree.glob("tb/*/README.md"))}
    everywhere: dict[str, int] = {}
    for suite in ["pp_top"] + sorted(per_suite):
        for k, v in per_suite[suite].items():
            everywhere.setdefault(k, v)

    arms: list[tuple[str, str, int]] = []
    if a.json:
        for r in json.loads(a.json.read_text()):
            if r["mutant"].startswith("golden"):
                print(f"{r['mutant']}: {r['verdict']}")
                continue
            arms.append((r["mutant"], r["verdict"], len(r["failing_checks"])))
    else:
        for line in a.log.read_text().splitlines():
            m = re.match(r"^([\w-]+): rc=\d+ failures=(\d+) named=\d+ (\w+)", line)
            if m:
                arms.append((m.group(1), m.group(3), int(m.group(2))))

    bad = 0
    for name, verdict, got in arms:
        base, _, suite = name.partition("@")
        want = per_suite.get(suite, {}).get(base, everywhere.get(base))
        st = "EQUAL" if want == got else "NO RECORD" if want is None else "DIFFERS"
        bad += st != "EQUAL"
        print(f"{name}: {verdict} failing {got}, README {want}: {st}")
    print(f"{len(arms)} arms, {len(arms) - bad} at their README count, {bad} not")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
