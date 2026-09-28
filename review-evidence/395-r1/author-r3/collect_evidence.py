"""Check retained measurements and preserve small receipts without large artifacts."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path('$LANES/395-timing-grade')
OUT = Path('$MANAGEMENT/2026-09-23/395-a393')
WORK = Path('$VALIDATION_STORAGE/395-a393-work')
SHIPPING = Path('$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9')
HEAD = '3b5603e3d16a164c35329efeb633800fe4fe9f95'
REPORTS = WORK / ('reports-' + HEAD[:9])


def fingerprint(path: Path) -> dict:
    """Measure the original file without copying it."""
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == HEAD
metrics = []
for name, expected in (
    ('Slow_0C', (0.123, 0.0, 0.101, 0.0)),
    ('Slow_85C', (0.123, 0.0, 0.101, 0.0)),
    ('Fast_0C', (1.429, 0.0, 0.036, 0.0)),
    ('Fast_85C', (1.429, 0.0, 0.036, 0.0)),
    ('all', (0.123, 0.0, 0.036, 0.0)),
):
    path = REPORTS / ('signoff_' + name + '_timing.rpt')
    lines = path.read_text().splitlines()
    index = next(i for i, line in enumerate(lines) if 'WNS(ns)' in line and 'WHS(ns)' in line)
    row = lines[index + 2].split()
    measured = tuple(float(row[i]) for i in (0, 1, 4, 5))
    assert measured == expected, (path, measured)
    assert measured[0] >= 0.03 and measured[2] >= 0
    assert row[2:4] == ['0', '175907'] and row[6:8] == ['0', '175907']
    metrics.append(dict(report=path.name, WNS=measured[0], TNS=measured[1],
                        WHS=measured[2], THS=measured[3], WPWS=float(row[8])))
    (OUT / (path.stem + '-summary.txt')).write_text('\n'.join(lines[:16] + lines[index:index+7]) + '\n')
(OUT / 'timing-metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
prior = Path('$REVIEWS/395-r372-2-packet/receipts/r2-v1-crossings-r2-results.txt')
assert (REPORTS / 'crossings-r2-results.txt').read_bytes() == prior.read_bytes()
rows = []
for path in sorted(REPORTS.iterdir()):
    if not path.is_file() or path.suffix not in ('.rpt', '.txt', '.tcl', '.log'):
        continue
    row = {'source': str(path), **fingerprint(path)}
    if row['bytes'] <= 200000:
        target = OUT / 'reports' / path.name
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(path.read_bytes())
        row['copy'] = str(target.relative_to(OUT))
    rows.append(row)
(OUT / 'report-artifacts.json').write_text(json.dumps(rows, indent=2) + '\n')
before = json.loads((OUT / 'shipping-inputs-before.json').read_text())
after = {rel: fingerprint(SHIPPING / rel) for rel in before}
assert before == after, 'shipping inputs changed'
(OUT / 'shipping-inputs-after.json').write_text(json.dumps(after, indent=2) + '\n')
print('All five timing summaries match the recorded numbers and meet the margin.')
print('Crossing endpoint classes and measurements match the round-2 reviewer receipt byte for byte.')
print('Seven shipping input hashes unchanged; all retained copies at most 200000 bytes.')
if '--reports-only' in sys.argv:
    raise SystemExit(0)
gates = json.loads((OUT / 'gate-results.json').read_text())
assert len(gates) == 21 and all(row['returncode'] == 0 and row['head'] == HEAD for row in gates)
for row in gates:
    assert fingerprint(Path(row['log'])) == {'bytes': row['bytes'], 'sha256': row['sha256']}, row
for mode in ('present', 'absent'):
    log = (WORK / ('gates-' + HEAD[:9]) / ('builder-' + mode + '.log')).read_text()
    selected = [line for line in log.splitlines() if '[timing grade]' in line
                or re.search(r'\[gate [^]]+\] SKIP:', line)
                or 'GATE ARM(S) DID NOT RUN' in line
                or line.startswith(('ALL GATES', 'Full builder bank completed'))]
    (OUT / ('builder-' + mode + '-summary.txt')).write_text('\n'.join(selected) + '\n')
print('All 21 final-head gate results are rc 0; log hashes verified.')
