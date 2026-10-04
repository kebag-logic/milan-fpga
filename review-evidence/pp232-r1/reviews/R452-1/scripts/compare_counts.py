#!/usr/bin/env python3
"""Compare a mutation campaign's per-arm verdicts and failing-check counts with
the counts the suite READMEs record.

Usage: compare_counts.py RESULTS README [README ...]
  RESULTS  a driver's results.json (list of records with mutant / verdict /
           failing_checks) or a driver log with lines "NAME: rc=R failures=N ... VERDICT"
Every README table row whose first cell is a backticked name and whose last
cell starts with an integer is a recorded count. Prints one line per arm and
exits 0 only when every killed arm's count equals its recorded count.
"""
import json
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*(`[^|]*?`)\s*\|.*\|\s*(?:the same )?(\d[\d,]*)\b[^|]*\|\s*$")


def recorded(readmes):
    rec = {}
    prev = ""
    for p in readmes:
        for line in Path(p).read_text().splitlines():
            m = ROW.match(line)
            if m:
                # a first cell may name siblings: "`base`, `-talker`" is base and base-talker
                first = line.split("|")[1]
                names = re.findall(r"`([^`]+)`", first)
                base = names[0]
                # ... or, as in the hazard table, siblings of the previous row's name
                for n in names:
                    keys = [base + n, prev + n] if n.startswith("-") else [n]
                    for key in keys:
                        rec.setdefault(key, []).append(int(m.group(2).replace(",", "")))
                prev = base
    return rec


def measured(path):
    text = Path(path).read_text()
    out = {}
    if path.endswith(".json"):
        for r in json.loads(text):
            out[r["mutant"]] = (r["verdict"], len(r.get("failing_checks") or []))
    else:
        for line in text.splitlines():
            m = re.match(r"^\s*(?:\d+:)?([\w.-]+): rc=\S+ failures=(\d+).*\b(KILLED|SURVIVED|PASS|FAIL)\b", line)
            if m:
                out[m.group(1)] = (m.group(3), int(m.group(2)))
    return out


def main() -> int:
    meas = measured(sys.argv[1])
    rec = recorded(sys.argv[2:])
    bad = 0
    for name, (verdict, n) in sorted(meas.items()):
        if name.startswith(("golden", "control")):
            print(f"{name}: {verdict}")
            bad += verdict != "PASS"
            continue
        want = rec.get(name)
        ok = verdict == "KILLED" and want is not None and n in want
        print(f"{name}: {verdict} {n} recorded {want} {'OK' if ok else 'DIFF'}")
        bad += not ok
    print(f"{len(meas)} records, {bad} differing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
