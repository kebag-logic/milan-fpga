#!/usr/bin/env python3
"""collect.py OUT: copy this round's receipts from the lane scratch into OUT, text only, with host paths replaced by
the placeholders round 1 used (<scratch>, <lane>, <scripts>, <home>, <tools>). Build trees, copied checkouts and the
runner's temporary directories are not receipts and are skipped. Hashes quoted inside a receipt are of the raw files."""
import hashlib
import shutil
import sys
from pathlib import Path

T = Path('<scratch>/r2')
R1 = Path('<home>/milan-fpga-management/2026-09-23/963-a819/round1/receipts')
SCRIPTS = Path('<scripts>')
SUBS = (('<scripts>', '<scripts>'),
        ('<scratch>', '<scratch>'), ('<lane>', '<lane>'),
        ('<tools>', '<tools>'), ('<tools>/scratch', '<tools>/scratch'), ('<home>', '<home>'))
SKIP = {'work', 'build', 'nogit', 'runner_temp', 'checkout', 'reuse'}
out = Path(sys.argv[1]).resolve()
if out.exists():
    shutil.rmtree(out)


def scrub(text: str) -> str:
    for old, new in SUBS:
        text = text.replace(old, new)
    return text


def put(src: Path, dst: Path) -> None:
    if src.is_dir():
        for p in sorted(src.iterdir()):
            if p.name not in SKIP and not p.name.startswith('github_'):
                put(p, dst / p.name)
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_bytes()
    text = scrub(raw.decode(errors='replace'))
    if len(raw) > 200_000:  # as round 1 published a long log: a headed excerpt, its first and last 400 lines
        lines = text.splitlines()
        head = (f'# {src.name}: {len(raw):,} bytes, sha256 {hashlib.sha256(raw).hexdigest()}; its first and last 400 '
                f'of {len(lines):,} lines')
        text = '\n'.join([head, *lines[:400], '[...]', *lines[-400:]]) + '\n'
    dst.write_text(text)


put(T / 'focused-head', out / 'tests/focused-head')
put(T / 'probe-plant-on-r1-test', out / 'tests/probe-plant-on-r1-test')
put(T / 'probe-tallies', out / 'tests/probe-tallies')
put(T / 'aecp-suite-arms', out / 'firmware/shard0-aecp-arms')
put(T / 'aecp-campaign', out / 'firmware/aecp-campaign')
put(T / 'union.txt', out / 'firmware/aecp-campaign/union.txt')
put(T / 'plant-tally.txt', out / 'firmware/plant-tally.txt')
for name, src in (('coverage-selftest', 'coverage_selftest'), ('coverage-ctrl', 'coverage-ctrl'),
                  ('coverage-nvm', 'coverage-nvm'), ('coverage-check', 'coverage-check'),
                  ('coverage-check-cut-by-cap', 'coverage_check')):
    put(T / 'fw-unit' / src, out / 'coverage' / name)
for k in (1, 2, 3, 4):
    put(T / f'docs/d{k}', out / f'docs/group-{k}')
put(T / 'docs/d5', out / 'docs/gate_24-cut-by-cap-1')
put(T / 'docs/d6', out / 'docs/gate_24-cut-by-cap-2')
put(T / 'delta', out / 'delta')
put(T / 'side-effects.txt', out / 'side-effects.txt')
for p in sorted(SCRIPTS.iterdir()):
    if p.is_file():
        put(p, out / 'scripts' / p.name)
put(T / 'HOW.md', out / 'HOW.md')
print(f'{sum(1 for p in out.rglob("*") if p.is_file())} files')
