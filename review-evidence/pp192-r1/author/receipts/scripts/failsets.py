"""usage: failsets.py <base-out-dir> <head-out-dir>
For every log in either campaign output directory, compare the sorted FAIL lines
(every line beginning 'FAIL', the suite tallies excluded) between base and head;
print the logs whose lines differ, and those present on one side only."""
import sys
from pathlib import Path


def fails(d: Path) -> dict[str, list[str]]:
    out = {}
    for p in sorted(d.rglob("*.log")):
        lines = [ln.rstrip() for ln in p.read_text(errors="replace").splitlines()
                 if ln.startswith("FAIL") and "checks:" not in ln]
        out[str(p.relative_to(d))] = sorted(lines)
    return out


base, head = fails(Path(sys.argv[1])), fails(Path(sys.argv[2]))
same = 0
for name in sorted(set(base) | set(head)):
    if name not in base:
        print(f"HEAD ONLY {name}: {len(head[name])} FAIL lines")
        for ln in head[name]:
            print(f"    + {ln}")
    elif name not in head:
        print(f"BASE ONLY {name}: {len(base[name])} FAIL lines")
    elif base[name] != head[name]:
        print(f"DIFFER {name}: base {len(base[name])}, head {len(head[name])} FAIL lines")
        for ln in sorted(set(base[name]) - set(head[name])):
            print(f"    - {ln}")
        for ln in sorted(set(head[name]) - set(base[name])):
            print(f"    + {ln}")
    else:
        same += 1
print(f"{same} logs carry the same FAIL lines at base and head")
