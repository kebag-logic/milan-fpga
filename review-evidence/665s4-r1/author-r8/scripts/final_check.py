#!/usr/bin/env python3
"""Fail unless every cited run is rc 0, at the head, in the packet. usage: final_check.py <packet> <head>."""
import hashlib
import subprocess
import sys
from pathlib import Path

packet, head = Path(sys.argv[1]), sys.argv[2]
runs = packet / 'receipts/runs'
RAW = Path('$VALIDATION_STORAGE/scratch/665s4-a698i/docs-final/logs')
NAMES = ('image-selftest', 'firmware_boundary', 'firmware_boundary_verilator', 'mutants2', 'boot-1x1', 'boot-8x8',
         'partial-map-probe', 'map-edges', 'py-idiom', 'identity')
#: Words each run's log must hold, so an rc of 0 from the wrong run cannot pass.
WORDS = {'image-selftest': 'ctrl_image self-test: 40 checks PASS', 'firmware_boundary': 'ctrl_boundary: PASS',
         'firmware_boundary_verilator': 'ctrl_boundary: PASS', 'mutants2': 'mutants: 15 planted, 0 escaped',
         'boot-1x1': 'ctrl_split_boot: PASS (0 finding(s))', 'boot-8x8': 'ctrl_split_boot: PASS (0 finding(s))',
         'partial-map-probe': 'json-only-map: rc=2 elf=no', 'map-edges': 'relative: rc=0 elf=yes',
         'py-idiom': 'over-long line', 'identity': '0 private line(s)'}
bad = 0
for name in NAMES:
    rc = (runs / f'{name}.rc').read_text().strip()
    log = (runs / f'{name}.log').read_text(errors='replace')
    ok = rc == '0' and log.startswith(f'# {head} ') and WORDS[name] in log
    bad += not ok
    print(f'{"ok " if ok else "BAD"} {name}: rc {rc}')
docs = packet / 'receipts/docs'
table = (docs / 'docs-yml-table.md').read_text()
ok = (docs / 'verify.rc').read_text().strip() == '0' and '71 steps ran, 24 not run with a reason, 0 bad' in table
bad += not ok
print(f'{"ok " if ok else "BAD"} docs.yml: {table.strip().splitlines()[-1]}')


def at_head(log: Path) -> bool:
    """The log's first line names the head; a log the packet holds as a digest and tail is read from its raw copy,
    which must match that digest."""
    first = log.read_text(errors='replace').split('\n', 1)[0]
    if not first.startswith('FULL LOG:'):
        return head in first
    data = (RAW / log.name).read_bytes()
    return (f'sha256={hashlib.sha256(data).hexdigest()}' in first and
            head in data.decode(errors='replace').split('\n', 1)[0])


wrong = [p.name for p in docs.glob('*.log') if not at_head(p)]
bad += bool(wrong)
print(f'{"BAD" if wrong else "ok "} docs logs at another head: {len(wrong)} of {len(list(docs.glob("*.log")))}')
lane = '$LANES/665-s4-f1-target'
now = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
dirty = subprocess.run(['git', '-C', lane, 'status', '--porcelain'], capture_output=True, text=True, check=True).stdout
ok = now == head and not dirty
bad += not ok
print(f'{"ok " if ok else "BAD"} lane at {now[:10]}, status lines {len(dirty.splitlines())}')
print(f'final check: {bad} bad')
sys.exit(1 if bad else 0)
