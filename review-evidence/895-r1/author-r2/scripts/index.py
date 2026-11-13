#!/usr/bin/env python3
"""Scrub host paths from round 2's receipts and write receipts/INDEX.md from the files present (lane 895 round 2):
each file's size and sha256, grouped by directory, with what each directory holds."""
import hashlib
from pathlib import Path
R = Path('$MANAGEMENT/2026-09-23/895-a775/round2/receipts')
SUBS = [('/data-2/milan/tmp/895-a775', '<scratch>'), ('/data-2/milan/tmp/665s2b-a683zm/builds', '<round 28 builds>'),
        ('$LANES/895r2sweep-shard', '<sweep-clone>'), ('$LANES/895-talker', '<clone>'),
        ('$MANAGEMENT', '<mgmt>'), ('$VALIDATION_TOOLS', '<tools>'), ('$VALIDATION_STORAGE/scratch', '<tools>'),
        ('$WORKSPACE_HOME', '<home>')]
WHAT = {
    'gates': 'the gate pass on 18300f6e: dispatch log, queue, unit rcs, verify table, lane gates',
    'gates/workflows': "each workflow job's step logs and rcs (run_wf.py), drivers, campaign counts",
    'gates/harness': "the CPU budget harness re-check at the head (harness_final.sh, compare_builds.py), gates3h",
    'gates/units': "the gate pass's and this round's units' own logs",
    'sweep': 'the full Verilator sweep, four shards at 18300f6e, and the three suites re-run with CI MAKEFLAGS',
    'legs': "this round's cost legs on 17ac263f's firmware (R3-*): merges, summary, builds' executable hashes",
    'legs-e0398c40': "the superseded legs on e0398c40's firmware: the two STATED findings and the span comparison",
    'costs': "the measured costs (round 1's parsers), tables895.py's tables (unchanged), least margins, heaviest passes",
    'graders': 'load_grade.py and flip_grade.py at the head and at the base b2d39235',
    'rom': 'the eight ledger images at the head and at b2d39235, and their deltas',
    'sim': "the valid-destinations arm's wire, decoded by wire_talkers.py, with the logs' sha256",
    'plants': "the Talker plant campaigns at both points on e0398c40's worktree",
    'probes': "the Domain's leave/join probe (not committed): its test source and run logs at both points",
}
for f in R.rglob('*'):
    if f.is_file() and f.suffix in ('.txt', '.md', '.log', '.json', '.rc', '.cpp', '.sha256', '.err', '.groups', '') \
            and f.name != 'INDEX.md' and f.stat().st_size <= 200_000:
        t = f.read_text(errors='replace'); u = t
        for a, b in SUBS:
            u = u.replace(a, b)
        if u != t:
            f.write_text(u)
rows, total = {}, 0
for f in sorted(R.rglob('*')):
    if f.is_file() and f.name != 'INDEX.md':
        rel = f.relative_to(R); total += 1
        top = '/'.join(rel.parts[:2]) if rel.parts[0] == 'gates' and len(rel.parts) > 2 else rel.parts[0] if len(rel.parts) > 1 else '.'
        rows.setdefault(top, []).append((str(rel), f.stat().st_size, hashlib.sha256(f.read_bytes()).hexdigest()[:16]))
out = ['# Receipts of lane 895, round 2 (generated from the files present by scripts/index.py)', '',
       f'{total} files. Files over 200 KB were not copied: their size and sha256 are in the large.txt beside them.', '']
for top in sorted(rows):
    out += [f'## {top}', '', WHAT.get(top, WHAT.get(top.split("/")[0], '')), '', '| File | Bytes | sha256 (16) |', '|---|---:|---|']
    out += [f'| `{r}` | {n:,} | `{h}` |' for r, n, h in rows[top]]
    out.append('')
(R / 'INDEX.md').write_text('\n'.join(out))
print(total, 'files indexed')
