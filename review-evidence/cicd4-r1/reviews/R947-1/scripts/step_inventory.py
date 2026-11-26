#!/usr/bin/env python3
"""Compare the gate steps of a generated workflow at two commits: every non-setup step body, with the jobs
carrying it, so a lost, duplicated or changed gate command is visible.
Usage: step_inventory.py <repo> <base> <head> <workflow-file>"""
import json
import subprocess
import sys
from collections import defaultdict

import yaml

repo, base, head, wf = sys.argv[1:5]


def load(rev):
    return yaml.safe_load(subprocess.run(["git", "-C", repo, "show", f"{rev}:{wf}"], check=True,
                                         capture_output=True, text=True).stdout)


def inventory(doc):
    where = defaultdict(list)
    for jid, job in doc["jobs"].items():
        for step in job.get("steps", []):
            body = step.get("run") or json.dumps({"uses": step.get("uses"), "with": step.get("with")}, sort_keys=True)
            key = (step.get("name", ""), body.strip())
            legs = job.get("strategy", {}).get("matrix", {}).get("leg")
            where[key].append(f"{jid}{'' if legs is None else '[' + str(len(legs)) + ' legs]'}"
                              f"{'' if 'if' not in step else ' if ' + step['if']}")
    return where


b, h = inventory(load(base)), inventory(load(head))
only_b = sorted(set(b) - set(h))
only_h = sorted(set(h) - set(b))
moved = sorted(k for k in set(b) & set(h) if sorted(b[k]) != sorted(h[k]))
print(f"{wf}: {len(b)} distinct step bodies at base, {len(h)} at head")
print(f"\n== only at base ({len(only_b)})")
for k in only_b:
    print(f"- {k[0]!r} in {b[k]}\n    {k[1][:300]!r}")
print(f"\n== only at head ({len(only_h)})")
for k in only_h:
    print(f"- {k[0]!r} in {h[k]}\n    {k[1][:300]!r}")
print(f"\n== same body, carrier changed ({len(moved)})")
for k in moved:
    print(f"- {k[0]!r}: {b[k]} -> {h[k]}")
