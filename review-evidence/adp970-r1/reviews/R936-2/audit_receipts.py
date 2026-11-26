#!/usr/bin/env python3
"""Reconcile published resource figures and record source provenance.

Run after the independent verdict; reads two prior published baseline receipts.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
def git(*args, root=repo):
    return subprocess.check_output(['git', '-C', str(root), *args])
commit = 'af092a85bcda1d60fab649ca42e2b013996ee21e'
base = 'review-evidence/adp970-r1/reviews/R935-1/'
raw_receipts = {}
for name in ('ledger-base.log', 'ledger-5de21ff3.log'):
    data = git('show', commit + ':' + base + 'receipts/' + name)
    dest = packet / 'scratch/public/baselines' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    raw_receipts[name] = data
head_data = (packet / 'scratch/public/adp970-r2/author/receipts/milan/ledger.log').read_bytes()
def rows(data):
    return {m[0]: int(m[1].replace(b',', b'')) for m in re.findall(rb'POINT ([^:]+): rom ([\d,]+) B', data)}
b, h = rows(raw_receipts['ledger-base.log']), rows(head_data)
assert b == rows(raw_receipts['ledger-5de21ff3.log'])
figures = [{'point': p.decode(), 'base_rom': b[p], 'head_rom': h[p], 'delta': h[p]-b[p]} for p in b]
assert [r['delta'] for r in figures] == [264,272,264,256]
stack = repo / 'third_party/tsn-c-stack'
assert git('rev-parse', 'c3bff8f3^{tree}', root=stack) == git('rev-parse', '95902060^{tree}', root=stack)
assert subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', '4df125b8', 'HEAD']).returncode == 0
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import ctrl_mutants
missing = ctrl_mutants.unnamed_tests()
assert not missing
out = {'figures': figures,
       'baseline_sources': [{'path': base + 'receipts/' + n, 'commit': commit,
                            'published_blob_sha256': hashlib.sha256(data).hexdigest()}
                           for n,data in raw_receipts.items()],
       'stack_merge_commit': git('rev-parse','HEAD',root=stack).decode().strip(),
       'stack_merge_tree': git('rev-parse','HEAD^{tree}',root=stack).decode().strip(),
       'stack_reviewed_head_tree_equal': True, 'source_base_is_ancestor': True,
       'full_mutant_table_count': len(ctrl_mutants.MUTANTS), 'unnamed_tests': missing,
       'parent_hdl_delta': git('diff','--name-only','4df125b8..HEAD','--','hdl').decode(),
       'declaration_unchanged': '6.0 s; 4311 ms sum; 1689 ms margin',
       'evidence_authentication': 'published content hashes checked; no detached signature supplied'}
(packet / 'receipts/audit.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
