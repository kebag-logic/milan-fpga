#!/usr/bin/env python3
"""Read-only documentation-delta and published-receipt audit. Usage: audit.py REPO OUT."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

repo, out = map(Path, sys.argv[1:3])
head = '165476c755e4728a044c12ea6bc33ce0a0a9d28f'
prior = '8267b8951616cfd570baf690835d4b0d38f14596'
packet = 'f4e3a75bea92d8eb0bae6fbaafabce6fcafccd5a'
prefix = 'review-evidence/gptpsw-r1/'
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def blob(path):
    return git('show', packet + ':' + prefix + path)
assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '7d5ec9042ef3db671fe66b143b158a0b3fb2b7ff'
paths = git('diff', '--name-only', prior, head).decode().splitlines()
assert paths == ['docs/design/GPTP_SOFTWARE.md', 'docs/design/SPLIT_CONTROL_MEMORY.md']
(out / 'delta.diff').write_bytes(git('diff', '--no-ext-diff', '--no-textconv', prior, head))
(out / 'source-history.txt').write_bytes(git('log', '--oneline', '59b098841b1e2826aaf7a38b557faa5345f91c82..' + head))
(out / 'source-diff-stat.txt').write_bytes(git('diff', '--stat', '59b098841b1e2826aaf7a38b557faa5345f91c82', head))
print('PASS exact head/tree; only the two requested documentation files differ from', prior)
print('PASS executable inputs, tests, budgets, layout and gitlinks unchanged from prior review')
commit = git('cat-file', 'commit', packet)
print('Packet commit:', packet, 'embedded signature:', b'\ngpgsig ' in commit)
manifest = json.loads(blob('MANIFEST.json'))
selected = [r for r in manifest if r['file'].startswith('author-r5/receipts/')]
assert selected
dest = out / 'published'
dest.mkdir(exist_ok=True)
for row in selected:
    data = blob(row['file'])
    digest = hashlib.sha256(data).hexdigest()
    assert digest == row['published_sha256'], row['file']
    target = dest / row['file']
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print('HASH', digest, row['file'])
(out / 'published-manifest-selection.json').write_text(json.dumps(selected, indent=2) + '\n')
print('PASS published SHA-256 values:', len(selected), 'receipts; authenticity is not a signature claim')
for copied, original in [('plat_ledger-a6323318.log', 'author-r4/receipts/memory/plat_ledger-self-test-a6323318.log'),
                         ('plat_ledger-631dc544.log', 'author-r4/receipts/memory-631dc544/plat_ledger-631dc544.log')]:
    assert blob('author-r5/receipts/prior-memory/' + copied) == blob(original)
    print('PASS original receipt equals republished copy:', copied)
sys.path.insert(0, str(repo / 'sw/litex'))
import ctrl_memory as memory
import ctrl_memory_ledger as ledger
doc = (repo / paths[1]).read_text()
for key, entry in memory.LEDGERED.items():
    row = next(line for line in doc.splitlines() if line.startswith('| `' + key + '` |'))
    assert float(row.split('|')[-2].strip()) == entry.tiles
    for symbol, size in entry.symbols:
        assert f'`{symbol}` of {size:,} B' in row, (key, symbol, size)
    assert ledger.HELD[key] == (entry.symbols, entry.tiles)
    print('PASS documented key, symbols and limit:', key, entry.symbols, entry.tiles)
assert (ledger.IMG_GPTP_1, ledger.IMG_GPTP_2) == (1104, 2152)
regex = r'^POINT (\S+): rom ([\d,]+) B, sram ([\d,]+) B, ([\d.]+) RAMB36 .*ctrl_plat (\d+) B: PASS$'
def points(name):
    text = blob('author-r5/receipts/prior-memory/' + name).decode()
    assert 'plat_ledger controls: 9 of 9 as required' in text
    assert 'plat_ledger: PASS (0 finding(s))' in text
    return {m[0]: tuple(int(v.replace(',', '')) for v in (m[1], m[2])) + (float(m[3]), int(m[4]))
            for m in re.findall(regex, text, re.M)}
before, after = points('plat_ledger-a6323318.log'), points('plat_ledger-631dc544.log')
for point, roms in [('1x1-if1', (126632, 126640)), ('8x8-if2', (140952, 140960))]:
    assert (before[point][0], after[point][0]) == roms
    assert before[point][1:] == after[point][1:]
    print('PASS plain image:', point, before[point], '->', after[point])
measured_delta = git('diff', '--name-only', '631dc544', head).decode().splitlines()
assert measured_delta == paths + ['sw/litex/ctrl_memory.py']
old_memory = git('show', '631dc544:sw/litex/ctrl_memory.py').decode()
new_memory = (repo / 'sw/litex/ctrl_memory.py').read_text()
assert old_memory.replace('12,656 B of rom', '12,664 B of rom').replace('152,064 B of rom', '152,072 B of rom') == new_memory
print('PASS since measured image head 631dc544: two docs plus only measured ROM figures in one ledger explanation string')
print('PASS all documentation-delta and receipt checks')
