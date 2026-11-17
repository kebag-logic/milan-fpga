#!/usr/bin/env python3
"""R853-3 audit of the published round-6 author packet.

Usage: python3 -I audit_r6_packet.py <extracted review-evidence/sync1115-r1 directory> <its MANIFEST.json>

1. Every author-r6 file matches the archive MANIFEST.json's published sha256; every file the author-r6 INDEX.md lists
   exists with the listed byte count and sha256 prefix (pre-redaction values: a file the manifest marks path-redacted
   is held to the manifest only), and no unlisted file is present.
2. Each of the 13 round-6 legs' table.md is byte-identical to round 5b's (author-r5 legs-at-e2be92b0), and each rc is
   round 5b's.
3. The regrade comparison's moves: the count by change and by timer, that none moves to late, absent or unowned, and
   that every moved run-out names its owner and the participant that answered it before.
Exit 0 when all hold, 1 otherwise.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
r6 = root / 'author-r6'
r5 = root / 'author-r5' / 'receipts' / 'budget' / 'legs-at-e2be92b0'
bad = []

# The archive's MANIFEST.json (argument 2, the archive's review-evidence/sync1115-r1/MANIFEST.json) records each
# file's published sha256 and whether its paths were redacted after INDEX.md was generated.
manifest = json.loads(Path(sys.argv[2]).read_text())
entries = [e for e in manifest if e['file'].startswith('author-r6/')]
redacted = {e['file'][len('author-r6/'):] for e in entries if e['path_redacted']}
for e in entries:
    if hashlib.sha256((root / e['file']).read_bytes()).hexdigest() != e['published_sha256']:
        bad.append(f"manifest mismatch {e['file']}")
print(f'manifest: {len(entries)} author-r6 entries, published sha256 checked; path-redacted: {sorted(redacted)}')

listed = {}
for line in (r6 / 'INDEX.md').read_text().splitlines():
    m = re.match(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{16})` \|', line)
    if m:
        listed[m.group(1)] = (int(m.group(2)), m.group(3))
present = {str(p.relative_to(r6)) for p in r6.rglob('*') if p.is_file() and p.name != 'INDEX.md'}
for name, (size, digest) in listed.items():
    p = r6 / name
    if not p.is_file():
        bad.append(f'missing {name}')
        continue
    data = p.read_bytes()
    if (len(data) != size or hashlib.sha256(data).hexdigest()[:16] != digest) and name not in redacted:
        bad.append(f'mismatch {name}')
for extra in sorted(present - set(listed)):
    bad.append(f'unlisted {extra}')
print(f'index: {len(listed)} listed, {len(present)} present, {sum(1 for b in bad if b.startswith(("missing", "mismatch", "unlisted")))} problems')

legs = sorted(p.name for p in (r6 / 'receipts' / 'budget' / 'legs-at-9aa55d3b').iterdir())
for leg in legs:
    a = r6 / 'receipts' / 'budget' / 'legs-at-9aa55d3b' / leg
    b = r5 / leg
    same_table = (a / 'table.md').read_bytes() == (b / 'table.md').read_bytes()
    rc6, rc5 = (a / 'regrade.rc').read_text().strip(), (b / 'regrade.rc').read_text().strip()
    head = (a / 'regrade.log').read_text().splitlines()[0][:120]
    print(f'leg {leg}: table identical {same_table}; rc {rc6} (round 5b {rc5}); {head}')
    if not same_table or rc6 != rc5:
        bad.append(f'leg {leg} differs')

reg = json.loads((r6 / 'receipts' / 'budget' / 'regrade-at-9aa55d3b.json').read_text())
moves, by_change, by_timer, totals = [], {}, {}, {}
for leg in reg['legs']:
    for group, g in leg['groups'].items():
        mv = g['moves']
        totals[(leg['leg'], group)] = mv['run_outs']
        for x in mv['every']:
            moves.append((leg['leg'], group, x))
            k = f"{x['round5b']}->{x['round6']}"
            by_change[k] = by_change.get(k, 0) + 1
            by_timer[x['timer']] = by_timer.get(x['timer'], 0) + 1
            if x['round6'] in ('late', 'absent', 'unowned') or not x.get('owner') or not x.get('answered_by') \
                    or x['owner'] in x['answered_by']:
                bad.append(f"move {leg['leg']} {group} {x}")
pairs = {}
for _, _, x in moves:
    k = (x['owner'], tuple(x['answered_by']))
    pairs[k] = pairs.get(k, 0) + 1
print(f'moves: {len(moves)} of {sum(totals.values())} run-outs; by change {by_change}; by timer {by_timer}')
print(f'owner <- answered before: {dict((f"{o} <- {"/".join(a)}", n) for (o, a), n in sorted(pairs.items()))}')
print(f"field owner_frame_after_opportunity_ms non-null in {sum(1 for _, _, x in moves if x['owner_frame_after_opportunity_ms'] is not None)} moves")
print('problems:', bad or 'none')
raise SystemExit(1 if bad else 0)
