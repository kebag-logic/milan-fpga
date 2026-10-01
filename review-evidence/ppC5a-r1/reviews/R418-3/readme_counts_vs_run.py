#!/usr/bin/env python3
"""Compare each campaign arm's measured failing-check count with the count its
tb/pp_top/README.md row records.

usage: readme_counts_vs_run.py <README.md> <campaign log>...
A row is `| `arm` | ... | N ... |`; the recorded count is the first integer of
the last cell, or for a "the same N" cell, that N. A measured line is the
driver's "arm: rc=.. failures=N named=.. VERDICT".
"""
import re
import sys


def recorded(readme):
    rows = {}
    for line in open(readme, encoding="utf-8"):
        m = re.match(r"^\|\s*`([a-z0-9-]+)`", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        last = cells[-1]
        n = re.match(r"(?:the same\s+)?(\d+)", last)
        if not n:
            continue
        # a shared row names its first arm in full and the rest as suffixes
        # (`hz-map-as-ro`, `-talker`): expand each suffix onto the first
        # arm's stem (the first arm itself, or minus its last suffix word)
        names = re.findall(r"`(-?[a-z0-9-]+)`", cells[0])
        first = names[0]
        for name in names:
            if not name.startswith("-"):
                arms = [name]
            else:
                stem = first
                arms = [first + name]
                while "-" in stem:
                    stem = stem.rsplit("-", 1)[0]
                    arms.append(stem + name)
            for arm in arms:
                rows.setdefault(arm, []).append(int(n.group(1)))
    return rows


def measured(logs):
    out = {}
    for log in logs:
        for line in open(log, encoding="utf-8"):
            m = re.match(r"^([a-z0-9-]+): rc=(\d+) failures=(\d+) named=(\d+) (\w+)", line)
            if m:
                out[m.group(1)] = (int(m.group(3)), m.group(5))
    return out


def main():
    rec = recorded(sys.argv[1])
    meas = measured(sys.argv[2:])
    bad = 0
    for arm, (n, verdict) in sorted(meas.items()):
        want = rec.get(arm)
        ok = want is not None and n in want and verdict == "KILLED"
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {arm}: measured {n} {verdict}, README {want}")
    print(f"arms {len(meas)}, mismatches {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
