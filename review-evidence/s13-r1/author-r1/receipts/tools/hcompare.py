#!/usr/bin/env python3
"""hcompare.py MEASURED_POINT_DIR HEAD_POINT_DIR: the CPU budget harness's per-group results of one point, this head's
run against the measured run's, leaf by leaf.

Both directories are <point>/ trees as legs.py writes them: <arm>/part<k>/<group>.json (each probe's start and end
on sys, its CPU cycles, its pass cycles, instructions, regions and modules, the group's timeouts, passes and
summary) and <arm>/part<k>/results.json (the graded rows). Only parts this head finished (its <arm>.part<k>.rc
reads 0) are compared. Every leaf is compared as written, except string leaves that name a filesystem path,
which differ by the scratch directory alone. Prints, per arm, the groups compared, identical and differing, and
for each differing group its first differing leaves; exit 0 when every compared group is identical."""
import json
import sys
from pathlib import Path


def leaves(node, path=""):
    """(path, value) of every leaf; a string that holds a '/' is a path and is left out."""
    if isinstance(node, dict):
        for k in sorted(node):
            yield from leaves(node[k], f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, f"{path}[{i}]")
    elif not (isinstance(node, str) and "/" in node):
        yield path, node


def main():
    measured, head = Path(sys.argv[1]), Path(sys.argv[2])
    total = same = 0
    bad = []
    for rc in sorted(head.glob("*.part*.rc")):
        arm, part = rc.name[:-3].rsplit(".part", 1)
        if rc.read_text().strip() != "0":
            print(f"{arm} part{part}: this head's run exited {rc.read_text().strip()}; not compared")
            bad.append((arm, part, "rc"))
            continue
        for mine in sorted((head / arm / f"part{part}").glob("*.json")):
            theirs = measured / arm / f"part{part}" / mine.name
            total += 1
            if not theirs.is_file():
                bad.append((arm, part, f"{mine.name}: no measured counterpart"))
                continue
            a = dict(leaves(json.loads(theirs.read_text())))
            b = dict(leaves(json.loads(mine.read_text())))
            diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
            if diff:
                bad.append((arm, part, f"{mine.name}: {len(diff)} leaves differ, first "
                            + "; ".join(f"{k} {a.get(k)!r} -> {b.get(k)!r}" for k in diff[:4])))
            else:
                same += 1
    print(f"groups' result files compared: {total}, identical: {same}, differing or missing: {total - same}")
    for arm, part, why in bad:
        print(f"  {arm} part{part}: {why}")
    return 0 if total and same == total and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
