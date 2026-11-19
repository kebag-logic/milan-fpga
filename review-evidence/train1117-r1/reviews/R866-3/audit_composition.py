#!/usr/bin/env python3
"""Read-only composition and published receipt audit; run from the candidate clone."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(sys.argv[1]).resolve()
HEAD = '0839453f6d7135063e904bcaf4ac1852ad6b522a'
BASE = 'cb96336d'
PREV = 'b1f1161b'
SOURCE = 'fe297847'
ARCHIVE = '33c82526d5f62e39b1324b5dd3e34b63602f8c03'

def git(*args):
    return subprocess.check_output(['git', *args])

def changes(a, b, path):
    raw = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', '-U0', a, b, '--', path)
    return [line for line in raw.splitlines() if line[:1] in (b'+', b'-') and not line.startswith((b'+++', b'---'))]

ledger = {'docs/design/SPLIT_CONTROL_MEMORY.md', 'sw/firmware/ctrl/plat/README.md',
          'sw/litex/ctrl_memory.py', 'sw/litex/ctrl_memory_ledger.py', 'sw/litex/test_ctrl_memory.py',
          'tb/verilator/ctrl_split_boot/plat_ledger.py', 'tb/verilator/ctrl_split_boot/README.md'}
paths = git('diff', '--name-only', BASE, SOURCE).decode().splitlines()
actual = set(git('diff', '--name-only', PREV, HEAD).decode().splitlines())
print('HEAD', git('rev-parse', 'HEAD').decode().strip())
print('TREE', git('rev-parse', 'HEAD^{tree}').decode().strip())
print('source paths', len(paths), 'composition paths', len(actual))
print('unexpected composition paths', sorted(actual - set(paths)))
assert not actual - set(paths)
for p in paths:
    equal = changes(BASE, SOURCE, p) == changes(PREV, HEAD, p)
    print('LEDGER' if p in ledger else 'CARRIAGE', 'equal' if equal else 'different', p)
    assert equal or p in ledger, p
for name, a, b in [('full-train.diff', BASE, HEAD), ('step12.diff', PREV, HEAD), ('source947.diff', BASE, SOURCE)]:
    (OUT / 'scratch' / name).write_bytes(git('diff', '--no-ext-diff', '--no-textconv', a, b))
for commit in ['d09c7118', '7650a02d', HEAD]:
    parents = git('show', '-s', '--format=%P', commit).decode().strip()
    print('MERGE', commit, parents)
    raw = git('show', '--remerge-diff', '--format=', commit)
    (OUT / 'scratch' / ('resolution-' + commit[:8] + '.diff')).write_bytes(raw)
    print('remerge paths', [x.decode() for x in raw.splitlines() if x.startswith(b'diff --git')])
for p in sorted(ledger - {'sw/firmware/ctrl/plat/README.md'}):
    print('round2 retains first parent', p, git('rev-parse', '967b1ca9:'+p) == git('rev-parse', '7650a02d:'+p))
print('round3 ledger comment retains first parent', git('rev-parse', '7650a02d:sw/litex/ctrl_memory.py') == git('rev-parse', HEAD+':sw/litex/ctrl_memory.py'))
for p in ['sw/firmware/ctrl/plat/README.md', 'sw/firmware/ctrl/test/test_plat_sinks.cpp', 'sw/firmware/ctrl/test/sink_mutants.py']:
    assert changes('9f4f3de0', SOURCE, p) == changes('7650a02d', HEAD, p)
    print('round3 exact delta', p)
for area in ['hdl', 'sw/mailbox', 'sw/firmware/ctrl/aecp', 'sw/firmware/ctrl/loop', 'tb/verilator/ctrl_service_budget']:
    assert not git('diff', '--name-only', PREV, HEAD, '--', area)
    print('unchanged dependency', area)
root = OUT / 'scratch/review-evidence/train1117-r1'
manifest = json.loads((root / 'MANIFEST.json').read_text())
checked = []
for item in manifest:
    if not item['file'].startswith('author-r5/'):
        continue
    p = root / item['file']
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest == item['published_sha256'], p
    checked.append((item['file'], digest))
print('published manifest verified', len(checked), 'files; no mismatch')
(OUT / 'archive-hashes.txt').write_text(''.join(f'{h}  {p}\n' for p,h in checked))
commit = git('cat-file', 'commit', ARCHIVE).split(b'\n\n', 1)[0]
print('archive commit carries gpgsig', b'\ngpgsig ' in commit)
print('PASS composition carriage and archive digest audit')
