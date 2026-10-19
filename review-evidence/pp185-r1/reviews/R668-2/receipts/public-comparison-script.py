"""usage: r1c_failsets.py <base-out-dir> <head-out-dir>
For each mutant log present in either campaign output directory, list the IDs of the
checks it failed (the token before the first ':' after 'FAIL:' or 'FAIL '), and print
the mutants whose sets differ between base and head, and those present on one side."""
import re
import sys
from pathlib import Path

FAIL = re.compile(r"FAIL:?\s+(?:\[[^\]]*\]\s*)?([A-Za-z][A-Za-z0-9_.-]*)")


def failsets(d: Path) -> dict[str, list[str]]:
    out = {}
    for p in sorted(d.glob("*.log")):
        ids = []
        for line in p.read_text(errors="replace").splitlines():
            m = FAIL.search(line)
            if m and "checks:" not in line:
                ids.append(m.group(1).rstrip(":"))
        out[p.stem] = ids
    return out


base, head = failsets(Path(sys.argv[1])), failsets(Path(sys.argv[2]))
same = 0
for name in sorted(set(base) | set(head)):
    if name not in base:
        print(f"HEAD ONLY {name}: {len(head[name])}: {', '.join(head[name])}")
    elif name not in head:
        print(f"BASE ONLY {name}: {len(base[name])}: {', '.join(base[name])}")
    elif sorted(base[name]) != sorted(head[name]):
        print(f"DIFFER {name}: base {len(base[name])}: {', '.join(base[name])}")
        print(f"       {' ' * len(name)}  head {len(head[name])}: {', '.join(head[name])}")
    else:
        same += 1
print(f"{same} mutants fail the same checks at base and head")
