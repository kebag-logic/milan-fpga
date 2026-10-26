#!/usr/bin/env python3
"""Assemble round 3's receipts: copy each source into receipts/, replace host paths with role
placeholders, keep files of at most 200 KB, and list every file (kept or not) in MANIFEST.json
with its sha256 and size before and after normalisation; INDEX.md is generated from the files
present.

Usage: assemble_receipts.py PACKET SCRATCH ROUND2_SCRATCH CHECKOUT
"""
import hashlib
import json
import sys
from pathlib import Path

PACKET, SCRATCH, ROUND2, CHECKOUT = (Path(a) for a in sys.argv[1:5])
OUT = PACKET / 'receipts'
LIMIT = 200 * 1024
HOME = Path.home()
SUBSTITUTIONS = [
    (str(PACKET), '<packet>'), (str(SCRATCH), '<scratch>'), (str(ROUND2), '<round-2 scratch>'),
    (str(CHECKOUT), '<checkout>'), (str(HOME / 'litex-milan'), '<litex>'),
    (str(HOME / 'br-milan-rv32'), '<rv32-sdk>'), ('$VALIDATION_TOOLS', '<tools>'), (str(HOME), '<home>'),
]
#: (receipt directory, source directory, file patterns)
SOURCES = []
for arm in ('A1', 'A8', 'B1', 'B8', 'S1', 'S8', 'C-slow', 'C-shutdown', 'C-asbuilt'):
    SOURCES.append((f'runs/{arm}', SCRATCH / 'runs' / arm, ('*.txt', '*.json', '*.log', 'table.md')))
SOURCES += [
    ('builds', None, ()),
    ('drivers', SCRATCH / 'logs', ('run-*.log', 'regrade-*.log')),
    ('head-regrade', SCRATCH / 'headgrade', ('summary.txt',)),
    ('review-probes/R704-2', SCRATCH / 'r704/packet', (
        'publication-check.json', 'A1-build.rc.json', 'A8-build.rc.json', 'A1-delta.log', 'A8-delta.log',
        'A1-delta.rc.json', 'A8-delta.rc.json', 'native-probes.log', 'probe_scenario_control.log',
        'scenario-control.json', 'probe_delta.log', 'delta-probes.json', 'receipt-audit.json', 'receipt-audit.log',
        'selftest.log')),
    ('review-probes/R704-2/native-probes/A1', SCRATCH / 'r704/packet/native-probes/A1', ('*',)),
    ('review-probes/R704-2/native-probes/A8', SCRATCH / 'r704/packet/native-probes/A8', ('*',)),
]
for arm in ('A1', 'A8'):
    SOURCES.append((f'review-probes/R704-2/measurements/{arm}', SCRATCH / 'r704/packet/measurements' / arm,
                    ('*.txt', '*.json', '*.log', 'table.md')))
    SOURCES.append((f'review-probes/R703-2/fanout-{arm}', SCRATCH / 'r703' / f'fanout-{arm}', ('*',)))
SOURCES.append(('review-probes/R703-2', SCRATCH / 'logs', ('r703-*.log',)))


def normalised(data: bytes) -> bytes:
    """The bytes with every host path replaced by its role placeholder."""
    try:
        text = data.decode()
    except UnicodeDecodeError:
        return data
    for path, role in SUBSTITUTIONS:
        text = text.replace(path, role)
    return text.encode()


def place(rel: str, data: bytes, origin: str, rows: list) -> None:
    """Keep one receipt (or only list it, when it is too large) and record its digests."""
    out = normalised(data)
    row = dict(file=rel, origin=origin, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data),
               published_sha256=hashlib.sha256(out).hexdigest(), published_bytes=len(out),
               kept=len(out) <= LIMIT)
    if row['kept']:
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(out)
    rows.append(row)


def main() -> int:
    """Copy every source, then write MANIFEST.json and INDEX.md over the files present."""
    rows: list = []
    for rel_dir, src, patterns in SOURCES:
        if src is None or not src.is_dir():
            continue
        seen = set()
        for pattern in patterns:
            for path in sorted(src.glob(pattern)):
                if path.is_file() and path.name not in seen:
                    seen.add(path.name)
                    place(f'{rel_dir}/{path.name}', path.read_bytes(),
                          str(path).replace(str(SCRATCH), '<scratch>'), rows)
    for label in ('A1', 'A8', 'B1', 'B8', 'S1', 'S8', 'C-slow', 'C-shutdown', 'C-asbuilt'):
        place(f'builds/{label}.build.json', (ROUND2 / label / 'build.json').read_bytes(),
              f'<round-2 scratch>/{label}/build.json', rows)
    for label in ('A1', 'A8'):
        src = SCRATCH / 'r704/packet/scratch' / label / 'build.json'
        if src.is_file():
            place(f'builds/fresh-{label}.build.json', src.read_bytes(), f'<scratch>/r704/packet/scratch/{label}/build.json',
                  rows)
    # Receipts written in place (gates, probe outputs): their host paths are replaced too.
    placed = {r['file'] for r in rows}
    for path in sorted(OUT.rglob('*')):
        rel = path.relative_to(OUT).as_posix()
        if path.is_file() and rel not in placed and rel not in ('MANIFEST.json', 'INDEX.md'):
            data = path.read_bytes()
            out = normalised(data)
            path.write_bytes(out)
            rows.append(dict(file=rel, origin='written in place', sha256=hashlib.sha256(data).hexdigest(),
                             bytes=len(data), published_sha256=hashlib.sha256(out).hexdigest(),
                             published_bytes=len(out), kept=True))
    manifest = OUT / 'MANIFEST.json'
    manifest.write_text(json.dumps(rows, indent=1) + '\n')
    present = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file() and p.name != 'INDEX.md')
    kept = {r['file'] for r in rows}
    lines = ['# Round-3 receipts (index generated from the files present)', '',
             f'{len(present)} files here; MANIFEST.json lists {len(rows)} assembled receipts, '
             f'{sum(not r["kept"] for r in rows)} of them over 200 KB and not kept (sha256 and size only).', '']
    for rel in present:
        size = (OUT / rel).stat().st_size
        note = '' if rel in kept or rel == 'MANIFEST.json' else ' (written in place)'
        lines.append(f'- `{rel}` ({size:,} B){note}')
    lines += ['', 'Not kept (over 200 KB):', '']
    lines += [f'- `{r["file"]}`: sha256 `{r["sha256"]}`, {r["bytes"]:,} B' for r in rows if not r['kept']]
    (OUT / 'INDEX.md').write_text('\n'.join(lines) + '\n')
    print(f'{len(rows)} receipts, {sum(r["kept"] for r in rows)} kept, {len(present)} files present')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
