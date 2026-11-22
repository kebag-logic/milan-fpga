#!/usr/bin/env python3
"""Reproduce the review's static checks and verify the public receipt index."""
import hashlib
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
evidence_rev = '4ee921e6bb38b753a83701cf89dfb6105739808d'
prefix = 'review-evidence/584-r1/author-r1/receipts/'
def public(path):
    return subprocess.check_output(['git', 'show', evidence_rev + ':' + prefix + path], cwd=root)

index = public('INDEX.md').decode()
rows = re.findall(r'\| `([^`]+)` \| (\d+) \| `([a-f0-9]{64})` \|', index)
assert rows
lines = ['Public receipts: ' + evidence_rev + ':' + prefix]
bad = 0
for path, size, digest in rows:
    data = public(path)
    actual = hashlib.sha256(data).hexdigest()
    if len(data) != int(size) or actual != digest:
        bad += 1
        lines.append(f'MISMATCH {path}: indexed {size} B / {digest}; actual {len(data)} B / {actual}')
    else:
        lines.append('PASS ' + digest + '  ' + path)
lines.append(f'{len(rows)} indexed public receipts checked against immutable Git blobs: {len(rows)-bad} match, {bad} mismatch.')

make = (root / 'tb/verilator/milan_dp/Makefile').read_text()
recipe = next(line for line in make.splitlines() if '--Mdir obj_nxn8 ' in line)
assert '-GLOOPBACK_P=1' in recipe
assert 'AUDIO_IF_RENDER_SLOTS_P' not in recipe
assert 'AUDIO_IF_SLOTS_P' not in recipe
lines += ['', 'nxn8 recipe: ' + recipe.strip()]
rtl = (root / 'hdl/milan/milan_datapath.sv').read_text()
for name in ('AUDIO_IF_SLOTS_P', 'AUDIO_IF_MASTER_P', 'AUDIO_IF_RENDER_SLOTS_P', 'CTRL_SPLIT_P'):
    match = re.search(r'parameter\s+int\s+' + name + r'\s*=\s*0\s*,', rtl)
    assert match, name
    lines.append('default: ' + match.group(0))
assert 'assign tdm_dout_o       = 1\'b0;' in rtl
lines.append('AUDIO_IF_RENDER_SLOTS_P=0 selects g_tdm_render_parked; tdm_dout_o is zero.')

doc = (root / 'docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
doc = doc.split('**Since #584**', 1)[1].split('Every image grows', 1)[0]
lines += ['', 'Memory-table arithmetic (base -> new, ROM / SRAM deltas):']
for line in doc.splitlines():
    cells = [s.strip() for s in line.split('|')]
    if len(cells) < 6 or not ('one interface' in cells[1] or 'two interfaces' in cells[1]):
        continue
    def pair(s):
        if not re.fullmatch(r'[\d,]+ / [\d,]+', s): return None
        return [int(n.replace(',', '')) for n in s.split(' / ')]
    a, b = pair(cells[2]), pair(cells[3])
    if a is not None and b is not None:
        lines.append(f'{cells[1]}: {b[0]-a[0]} / {b[1]-a[1]} B')
text = '\n'.join(lines) + '\n'
(packet / 'static-and-provenance.txt').write_text(text)
print(text)
