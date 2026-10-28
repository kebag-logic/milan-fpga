#!/usr/bin/env python3
"""Each probe's taking pass, by firmware module, a reference group record beside this run's.
usage: module_diff.py <reference group .json> <this run's group .json>
Prints each probe's CPU cycles and mailbox accesses in both, then the modules whose cycles in the
taking pass differ by more than 2,000 CPU cycles (this run minus the reference)."""
import json
import sys


def probes(path: str) -> dict[str, dict]:
    """The group record's probes, by name."""
    d = json.load(open(path))
    return {p['probe']: p for p in d['probes']}


ref, here = probes(sys.argv[1]), probes(sys.argv[2])
for k in sorted(set(ref) | set(here)):
    a, b = ref.get(k), here.get(k)
    if not a or not b:
        print(f'{k}: {"missing in the reference" if not a else "missing here"}')
        continue
    print(f"{k}: cycles {a.get('cpu_cycles')} -> {b.get('cpu_cycles')}, "
          f"pass accesses {a.get('pass_mbx_accesses')} -> {b.get('pass_mbx_accesses')}, "
          f"pass cycles {a.get('pass_cycles')} -> {b.get('pass_cycles')}")
    ma, mb = a.get('pass_modules') or {}, b.get('pass_modules') or {}
    diff = {m: mb.get(m, 0) - ma.get(m, 0) for m in set(ma) | set(mb)}
    big = {m: v for m, v in sorted(diff.items(), key=lambda x: -abs(x[1])) if abs(v) > 2000}
    print(f'    modules (here - reference): {big}')
