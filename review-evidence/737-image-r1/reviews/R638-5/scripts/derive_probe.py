#!/usr/bin/env python3
"""Run the candidate deriver on a probe tree; classify REFUSED / ACCEPTED-SAME / ACCEPTED-DIFF.

Usage: derive_probe.py <probe-tree> <reference-inventory.json> [watch-path ...]
ACCEPTED-SAME means the deriver returned the committed tools and residue unchanged.
"""
import json, subprocess, sys
tree, ref = sys.argv[1], sys.argv[2]
watch = sys.argv[3:]
code = ("import sys, json; sys.path.insert(0, sys.argv[1] + '/scripts'); "
        "from pathlib import Path; import ci_tool_inventory as m; "
        "print(json.dumps(m.derive(Path(sys.argv[1]))))")
r = subprocess.run([sys.executable, '-B', '-c', code, tree], capture_output=True, text=True)
reference = json.load(open(ref))
out = {'tree': tree}
if r.returncode:
    last = [l for l in r.stderr.strip().splitlines() if l.strip()]
    out['status'] = 'REFUSED'
    out['message'] = last[-1] if last else ''
else:
    got = json.loads(r.stdout)
    same_tools = got['tools'] == reference['tools']
    same_res = got['residue'] == reference['residue']
    out['status'] = 'ACCEPTED-SAME' if same_tools else 'ACCEPTED-DIFF'
    out['residue_same'] = same_res
    out['new_residue'] = sorted(set(got['residue']) - set(reference['residue']))
    out['tool_changes'] = [t for t in got['tools'] if t not in reference['tools']]
    out['watched_inputs'] = {w: (w in got['inputs']) for w in watch}
print(json.dumps(out, indent=1))
