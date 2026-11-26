#!/usr/bin/env python3
"""Check the round-2 author packet of PR #1017 (#1009 step 1) against its own manifests and read the
figures the review relies on.

Usage: python3 -I check_packet.py <packet-root>   (the directory holding MANIFEST.json and author/)

Prints, for the packet: every manifest entry's hash against the file; for each full-run point: the
results.json hash against the identity record, its group count, refusals, budget misses, share and save
misses, and how many retried or queued notice rows (notice.retried, notice.queued, talker notice paths)
the run measured; for each board summary: the cuts counted, the hold readings graded and the per-cut
lines that pass.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

NOTICE_PATHS = ('notice.retried', 'notice.queued', 'notice.declared', 'notice.withdrawn')


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(root: Path) -> int:
    bad = 0
    entries = json.loads((root / 'MANIFEST.json').read_text())
    for e in entries:
        got = sha(root / e['file'])
        ok = got == e['published_sha256']
        bad += not ok
        print(f"MANIFEST.json {'OK  ' if ok else 'BAD '} {e['file']}")
    author = root / 'author'
    for line in (author / 'MANIFEST.txt').read_text().splitlines():
        if not line.strip():
            continue
        h, name = line.split(None, 1)
        ok = sha(author / name) == h
        bad += not ok
        print(f"MANIFEST.txt  {'OK  ' if ok else 'BAD '} {name}")
    for point in ('1x1', '8x8-1if'):
        run = author / 'full-run'
        ident = (run / f'{point}-identity.txt').read_text()
        res = run / f'{point}-results.json'
        recorded = re.search(r'^([0-9a-f]{64})  \S*results\.json$', ident, re.M).group(1)
        d = json.loads(res.read_text())
        notice_rows = sum(1 for g in d['results'] for r in g['probes'] if r['path'][0] in NOTICE_PATHS)
        groups = [g['group'] for g in d['results']]
        print(f"{point}: identity head {re.search(r'^head (\S+)', ident, re.M).group(1)}, "
              f"status before {re.search(r'^status entries (\d+)', ident, re.M).group(1)}, "
              f"after {re.search(r'^status entries after (\d+)', ident, re.M).group(1)}, "
              f"rc {re.search(r'^rc (\d+)', ident, re.M).group(1)}; results.json "
              f"{'matches' if sha(res) == recorded else 'DIFFERS FROM'} the identity's hash")
        print(f"{point}: {len(groups)} groups, {len(d['refusals'])} refusals, {len(d['misses'])} budget misses, "
              f"{len(d['share_misses'])} share misses, {len(d['save_misses'])} save misses, "
              f"notices {len(d['notices'])}, notice_misses {len(d['notice_misses'])}, "
              f"retried/queued/talker notice rows measured {notice_rows}, "
              f"groups named notice-retried/notice-every/notice-burst/talker-notice "
              f"{sum(g.startswith(('notice-retried', 'notice-every', 'notice-burst', 'talker-notice')) for g in groups)}")
    for shape in ('1x1', '8x8'):
        text = (author / 'board' / f'summary-{shape}.txt').read_text()
        m = re.search(r'power cuts: (\d+), durable readings in holds: (\d+)', text)
        cuts = [ln for ln in text.splitlines() if ln.startswith('  sink ')]
        passing = [ln for ln in cuts if ln.rstrip().endswith('PASS')]
        idle = [ln for ln in cuts if 'idle at the bind True' in ln]
        before = [float(x) for x in re.findall(r'durable ([\d.]+) s before it', text)]
        print(f"board {shape}: power cuts counted {m.group(1)}, hold readings {m.group(2)}, per-cut lines {len(cuts)}, "
              f"PASS {len(passing)}, idle at the bind {len(idle)}, least margin before the last frame {min(before)} s")
    print(f'RESULT: {bad} manifest mismatch(es)')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
