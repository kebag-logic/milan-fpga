#!/usr/bin/env python3
"""Produce portable result summary and checksums; exclude all scratch data."""
import hashlib
import json
from pathlib import Path
import re
import sys
packet = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
scratch = packet / 'scratch'
initial = packet / 'focused-result.json'
if initial.exists():
    initial.rename(packet / 'focused-initial-result.json')
names = ('focused-gates', 'delta-probe', 'shape-check', 'shape-selftest', 'load-check',
         'flip-1x1', 'flip-all', 'docs-check', 'evidence-compare', 'prior-reader', 'object-probe', 'integrity')
results = {n: int((packet / (n + '.rc')).read_text()) for n in names}
assert all(rc == (1 if n == 'flip-all' else 0) for n, rc in results.items()), results
(packet / 'final-results.json').write_text(json.dumps({
    'head': '58f7673b8c57a80230e716bc1774ff9cc2f71ddc',
    'results': results,
    'notes': ['delta-probe initial setup failed due to omitted mailbox include; corrected probe passed',
              'flip-all rc 1 is byte-identical to published base, including documented 8x8/2if FAIL',
              'run.py --self-test not repeated; published base/head timeouts are not passes']
}, indent=2) + '\n')
added = [line[1:] for line in (packet / 'delta.diff').read_text().splitlines()
         if line.startswith('+') and not line.startswith('+++')]
for line in added:
    assert not re.search(r'\[R\d|R900|R902|B17|lane [A-Z]\d|issuecomment-|round [123]', line), line
(packet / 'comment-scan.log').write_text('Delta added-line marker scan: no reviewer IDs, review rounds, issue-comment IDs or bench lane labels.\nManual comment review: behavior/reason and #983 present; no new comment-rule residue.\n')
# Keep unredacted originals in scratch only. Replace location prefixes in logs.
raw = scratch / 'raw-receipts'
raw.mkdir(exist_ok=True)
for path in packet.glob('*.log'):
    data = path.read_text()
    clean = data.replace(str(packet), '<PACKET>').replace(str(repo), '<REPO>')
    if clean != data:
        (raw / path.name).write_text(data)
        path.write_text(clean)
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R900] POSITIVE - exact head 58f7673b8c57a80230e716bc1774ff9cc2f71ddc'
assert report.splitlines()[-1] == 'R900-3 FINISHED'
assert 'SKELETON' not in report and '\u2014' not in report and '\u200b' not in report
files = sorted(p for p in packet.iterdir() if p.is_file() and p.name != 'MANIFEST.sha256')
(packet / 'MANIFEST.sha256').write_text(''.join(
    hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in files))
print('Final statuses:', json.dumps(results, sort_keys=True))
print('Publishable files:', len(files), '; scratch excluded')
