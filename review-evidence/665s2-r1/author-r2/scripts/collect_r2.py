#!/usr/bin/env python3
"""Copy this round's evidence into receipts/: text files with host paths replaced, files over
200 KB recorded by sha256 and size only (MANIFEST.json), and INDEX.md generated from what is present.

Usage: collect_r2.py SCRATCH RECEIPTS
"""
import hashlib
import json
import sys
from pathlib import Path

SCRATCH, RECEIPTS = Path(sys.argv[1]), Path(sys.argv[2])
LIMIT = 200 * 1024
SUBST = [('$LANES/665-s2-budget', '<checkout>'), (str(SCRATCH), '<scratch>'),
         ('$WORKSPACE_HOME/litex-milan', '$LITEX'), ('$WORKSPACE_HOME/br-milan-rv32', '$SDK'), ('/tmp/a681', '<round-1 scratch>'),
         ('$MANAGEMENT/2026-09-23/665s2-a681b', '<output>'), ('$WORKSPACE_HOME', '~')]
manifest: dict[str, dict] = {}


def put(src: Path, dest: str, sanitize: bool = True) -> None:
    """One file into receipts/dest, or into the manifest when it is too large."""
    data = src.read_bytes()
    entry = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    if sanitize:
        text = data.decode()
        for old, new in SUBST:
            text = text.replace(old, new)
        data = text.encode()
        entry['published_sha256'] = hashlib.sha256(data).hexdigest()
    if len(data) > LIMIT:
        entry['kept'] = False
        manifest[dest] = entry
        return
    target = RECEIPTS / dest
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    entry['kept'] = True
    manifest[dest] = entry


# The measured runs at the head: every group's script and raw log, its grade, and the arm's tables.
for arm in ('A1', 'A8', 'B1', 'B8', 'S1', 'S8', 'C-slow', 'C-shutdown', 'C-asbuilt'):
    base = SCRATCH / 'headgrade2' / arm
    for path in sorted(base.iterdir()):
        put(path, f'runs/{arm}/{path.name}', sanitize=path.suffix != '.log')
    put(SCRATCH / 'headgrade2' / f'{arm}-regrade.log', f'runs/{arm}-regrade.log')
# The measuring drivers, the builds and their reproduction at the head.
for name in ('A1-long', 'A8-long', 'B1-long', 'B8-long', 'A1-bl', 'A8-bl', 'B1-bl', 'B8-bl', 'S1', 'S8',
             'C-slow', 'C-shutdown', 'C-asbuilt', 'fx2', 'repro'):
    put(SCRATCH / f'{name}.log', f'drivers/{name}.log')
for name in ('A1', 'A8', 'B1', 'B8', 'S1', 'S8', 'C-slow', 'C-shutdown', 'C-asbuilt'):
    put(SCRATCH / name / 'build.json', f'builds/{name}.build.json')
    put(SCRATCH / 'head' / name / 'build.json', f'builds/{name}.head-rebuild.build.json')
# The reviewers' probes and mutants at d58c8e22 and at the head.
put(SCRATCH / 'ovn-old.json', 'review-probes/d58c8e22.json')
put(SCRATCH / 'ovn-new.json', 'review-probes/head.json')
put(SCRATCH / 'review_mutants_r2.log', 'review-probes/review_mutants_r2.log')
put(SCRATCH / 'report.md', 'report.md')
put(SCRATCH / 'scripts-before.json', 'scripts-digest-before-refactor.json')
put(SCRATCH / 'scripts-after.json', 'scripts-digest-after-refactor.json')
(RECEIPTS / 'MANIFEST.json').write_text(json.dumps(manifest, indent=1, sort_keys=True) + '\n')

lines = ['# Receipts index', '', 'Generated from the files present. Paths are relative to this directory.',
         'Files over 200 KB are listed in `MANIFEST.json` by sha256 and size only.', '',
         '| File | Bytes | sha256 |', '|---|---:|---|']
for path in sorted(p for p in RECEIPTS.rglob('*') if p.is_file() and p.name != 'INDEX.md'):
    data = path.read_bytes()
    lines.append(f'| `{path.relative_to(RECEIPTS)}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()[:16]}` |')
withheld = [k for k, v in manifest.items() if not v['kept']]
lines += ['', f'Withheld for size ({len(withheld)}): ' + ', '.join(f'`{k}`' for k in withheld)]
(RECEIPTS / 'INDEX.md').write_text('\n'.join(lines) + '\n')
print(f'{sum(v["kept"] for v in manifest.values())} kept, {len(withheld)} withheld')
