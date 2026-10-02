#!/usr/bin/env python3
"""Compare each campaign arm's measured failing-check count with its README record.

usage: compare_readme.py TREE OUTDIR [OUTDIR...]
Measured count = the arm's results.json "failures" (or len "failing_checks") when present, else the number of
lines starting "FAIL:" in the arm's log (<arm>.log or <arm>@<suite>.log). Recorded
count = the leading integer of the last cell of a README table row whose first cell
names `arm` (grouped rows expanded), in tb/<suite>/README.md (suite from the log name, else every tb README).
"""
import json, re, sys
from pathlib import Path
tree = Path(sys.argv[1])
records = {}
suites = {d.name for d in tree.glob("tb/*") if d.is_dir()}
for readme in sorted(tree.glob("tb/*/README.md")):
    for ln in readme.read_text().splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0].startswith("`"):
            continue
        names = re.findall(r"`([^`]+)`", cells[0])
        # candidates from the row's last cell: "N FAIL", "N failures", and its first integer
        nums = {int(x.replace(",", "")) for x in
                re.findall(r"(\d[\d,]*) FAIL", cells[-1]) + re.findall(r"(\d[\d,]*) failures", cells[-1])
                + re.findall(r"^\D*?(\d[\d,]*)", cells[-1])}
        if not names or not nums:
            continue
        # a grouped row: `base-arm`, `-suffix` is the README's shorthand for a
        # prefix of the first arm's name + suffix; every prefix is registered
        parts = names[0].split("-")
        for n in names:
            fulls = ["-".join(parts[:k]) + n for k in range(1, len(parts) + 1)] if n.startswith("-") else [n]
            for full in fulls:
                records.setdefault(full, []).extend((readme.parent.name, n) for n in sorted(nums))
bad = total = 0
for out in map(Path, sys.argv[2:]):
    measured = {}
    res = out / "results.json"
    data = json.loads(res.read_text()) if res.exists() else None
    if isinstance(data, list) and any("failures" in r for r in data):
        for r in data:
            if "failures" in r:
                measured[(r["arm"], None)] = r["failures"]
    elif isinstance(data, list) and any("failing_checks" in r for r in data):
        for r in data:
            if not r["mutant"].startswith("golden"):
                arm = r["mutant"].partition("@")[0]
                suite = r.get("suite", "").split("/")[-1]
                measured[(arm, suite if suite in suites else None)] = len(r["failing_checks"])
    else:
        for log in sorted(list(out.glob("*.log")) + list(out.glob("*.txt"))):
            stem = log.stem
            if stem.startswith(("golden", "control")) or stem.endswith(("-build", "-run")):
                continue
            arm, _, suite = stem.partition("@")
            suite = suite if suite in suites else None
            for sfx in sorted(suites, key=len, reverse=True):
                if suite is None and arm.endswith("-" + sfx):
                    arm, suite = arm[:-len(sfx) - 1], sfx
                    break
            measured[(arm, suite)] = sum(1 for l in log.read_text(errors="replace").splitlines()
                                                 if l.startswith("FAIL:"))
    for (arm, suite), n in sorted(measured.items()):
        total += 1
        rec = [c for s, c in records.get(arm, []) if suite is None or s == suite]
        ok = n in rec
        bad += not ok
        print(f"{'EQUAL' if ok else 'DIFF '} {out.name:12s} {arm}{'@' + suite if suite else ''}: measured {n}, recorded {rec}")
print(f"compared {total}, equal {total - bad}, differing {bad}")
