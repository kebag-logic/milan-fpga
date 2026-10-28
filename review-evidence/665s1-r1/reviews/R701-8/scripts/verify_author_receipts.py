#!/usr/bin/env python3
"""Fetch the author's published round-8 receipts this review relies on and check each against
the evidence tree's MANIFEST.json (published_sha256). Prints one line per file and a summary.

Usage: python3 -I verify_author_receipts.py <empty-or-new download directory>
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

BASE = ('https://raw.githubusercontent.com/kebag-logic/milan-fpga/'
        'af4490faf13cf56cb76de0c9c750ab79f80c4dd5/review-evidence/665s1-r1/')
FILES = [
    'author-r8/a680k/PR-BODY.md',
    'author-r8/a680k/probes/plant-asbuilt-clean.diff',
    'author-r8/a680j/probes/plant-ack-early.diff',
    'author-r8/a680j/probes/plant-ack-probe.diff',
    *[f'author-r8/a680k/receipts/{f}' for f in (
        'INDEX.md', 'gates/harness-selftest.txt', 'gates/harness-selftest.txt.head', 'gates/docs-gates.txt',
        'gates/docs-gates.txt.head', 'gates/firmware-boundary.txt', 'gates/behave.txt',
        'runs/C-asbuilt/driver.log', 'runs/C-asbuilt/verilate.log', 'runs/C-asbuilt/elf-sha256.txt',
        'runs/C-asbuilt/pc-trace-boot-fault.txt', 'runs/C-asbuilt/mailbox-pins-missing.txt',
        'runs/plant-asbuilt-clean-1x1/WHAT.txt', 'runs/plant-asbuilt-clean-1x1/pc-trace-boot-fault.txt',
        'runs/plant-asbuilt-clean-1x1/results/boot-fault.log')],
    'author-r8/a680j/receipts/INDEX.md',
    *[f'author-r8/a680j/receipts/runs/{r}/{f}' for r in ('A1', 'A8', 'B1', 'B8')
      for f in ('WHAT.txt', 'soc.json', 'driver.log', 'mailbox-pins-missing.txt')],
    *[f'author-r8/a680j/receipts/compare/{f}' for f in (
        'aecp-1x1-vs-probe1.md', 'aecp-8x8-vs-probe1.md', 'aecp-1x1-late256.md')],
]

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)


def fetch(rel: str) -> bytes:
    with urllib.request.urlopen(BASE + rel, timeout=60) as r:
        return r.read()


manifest = {e['file']: e['published_sha256'] for e in json.loads(fetch('MANIFEST.json'))}
bad = 0
for rel in FILES:
    data = fetch(rel)
    (out / rel).parent.mkdir(parents=True, exist_ok=True)
    (out / rel).write_bytes(data)
    ok = manifest.get(rel) == hashlib.sha256(data).hexdigest()
    bad += not ok
    print(f"{'MATCH   ' if ok else 'MISMATCH'} {rel}")
print(f'{len(FILES)} files, {bad} mismatches, manifest entries {len(manifest)}')
sys.exit(1 if bad else 0)
