#!/usr/bin/env python3
"""hcompare2.py MEASURED_POINT_DIR HEAD_POINT_DIR: hsubset.sh's group results (<arm>/subset/<group>.json) against the
measured run's same group (found through that arm's parts.json), leaf by leaf as hcompare.py compares them."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hcompare import leaves  # noqa: E402

measured, head = Path(sys.argv[1]), Path(sys.argv[2])
total = same = 0
for mine in sorted(head.glob("*/subset/*.json")):
    if mine.name == "results.json":
        continue
    arm, group = mine.parts[-3], mine.stem
    parts = json.loads((measured / arm / "parts.json").read_text())["parts"]
    k = next(i for i, p in enumerate(parts) if group in p["groups"])
    theirs = measured / arm / f"part{k}" / mine.name
    a, b = dict(leaves(json.loads(theirs.read_text()))), dict(leaves(json.loads(mine.read_text())))
    diff = sorted(x for x in set(a) | set(b) if a.get(x) != b.get(x))
    cyc = [(p.get("probe"), p.get("cpu_cycles")) for p in json.loads(mine.read_text()).get("probes", [])]
    total += 1
    same += not diff
    print(f"{arm}/{group} (measured part{k}): {len(cyc)} probes, {'IDENTICAL' if not diff else f'{len(diff)} leaves differ'}"
          + ("" if not diff else ": " + "; ".join(f"{x} {a.get(x)!r} -> {b.get(x)!r}" for x in diff[:5])))
print(f"groups compared: {total}, identical: {same}")
sys.exit(0 if total and same == total else 1)
