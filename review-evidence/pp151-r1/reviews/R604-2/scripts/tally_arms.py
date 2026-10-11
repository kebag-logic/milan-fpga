#!/usr/bin/env python3
"""Tally a mutants.py log: per arm kind, how many arms were killed and by which legs.

usage: tally_arms.py LOG
Reads the `<arm>: rc=N KILLED|UNPROVEN` lines and the indented FAIL lines under each.
"""
import collections
import re
import sys


def main() -> int:
    """Print kind, arm count, killed count and the leg combinations that failed."""
    kinds: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    killed: collections.Counter[str] = collections.Counter()
    arms: collections.Counter[str] = collections.Counter()
    kind = legs = None
    status = ""

    def close() -> None:
        """Record the arm just read."""
        if kind is not None:
            kinds[kind][",".join(sorted(legs)) or "inventory-only"] += 1
            arms[kind] += 1
            killed[kind] += status == "KILLED"
    for line in open(sys.argv[1], encoding="utf-8"):
        found = re.match(r"^(\S+): rc=\d+ (KILLED|UNPROVEN)", line)
        if found:
            close()
            name, status = found.groups()
            kind = name.rsplit(":", 1)[1] if not name.startswith("bench:") else name
            legs = set()
            continue
        leg = re.match(r"^\s+FAIL: (?:GUARD|ELAB )\s*(\w+) ", line)
        if leg and legs is not None:
            legs.add(leg.group(1))
    close()
    for k in sorted(arms):
        print(f"{k:28s} arms={arms[k]:3d} killed={killed[k]:3d} legs={dict(kinds[k])}")
    print(f"total arms={sum(arms.values())} killed={sum(killed.values())}")
    return int(sum(arms.values()) != sum(killed.values()))


if __name__ == "__main__":
    raise SystemExit(main())
