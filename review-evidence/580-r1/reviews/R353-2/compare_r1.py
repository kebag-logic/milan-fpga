#!/usr/bin/env python3
"""Compare builder_outputs.py results with the public round-1 artifact table.

Usage: compare_r1.py <repo> <mine.json>
The reference is 147cb4b8:review-evidence/580-r1/author/new-artifacts.json.
"""
import json
import subprocess
import sys

REF = '147cb4b8d0e4fbaeb24d5853068aa2ee6ca15319:review-evidence/580-r1/author/new-artifacts.json'
repo, mine_path = sys.argv[1:3]
ref = json.loads(subprocess.check_output(['git', '-C', repo, 'show', REF], stderr=subprocess.DEVNULL))
with open(mine_path, encoding='utf-8') as fh:
    mine = json.load(fh)
diff = [(c, p) for c in sorted(set(mine) | set(ref['configs']))
        for p in sorted(set(mine.get(c, {})) | set(ref['configs'].get(c, {})))
        if mine.get(c, {}).get(p) != ref['configs'].get(c, {}).get(p)]
print(f"reference pin {ref['pin']}; files mine {sum(map(len, mine.values()))}, "
      f"reference {sum(map(len, ref['configs'].values()))}; differences {diff}")
print('RESULT:', 'FAIL' if diff else 'PASS')
sys.exit(1 if diff else 0)
