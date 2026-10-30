"""capture_summary.py <side-dir> <committed measurements.json>: each arm's rows, minimum, maximum and the run's own
margin against the 49 ms hold floor, its distance to the 24.5 ms production bound, and the committed receipt's
maximum for the same arm; then each control's exit status and the byte-only slowdown."""
import json
import sys
from pathlib import Path

side, committed = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
BOUND = 24.5
ref = {(m['shape'], m['cpu_hz'], m['traffic']): m for m in committed['measurements']}
print('| Arm | rc | Rows | ok | Minimum ms | Maximum ms | Under 24.5 ms by | Margin to the 49 ms floor | Committed receipt maximum ms |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
worst = None
for label in ('8x8-50-on', '8x8-50-off', '8x8-100-on', '8x8-100-off', '1x1-50-on', '1x1-50-off'):
    rc = (side / f'{label}.rc').read_text().strip() if (side / f'{label}.rc').exists() else 'running'
    path = side / f'capture-{label}' / 'measurement.json'
    if not path.exists():
        print(f'| {label} | {rc} | - | - | - | - | - | - | - |')
        continue
    m = json.loads(path.read_text())
    ok = sum(1 for r in m['rows'] if r['ok'] == 1)
    c = ref.get((m['shape'], m['cpu_hz'], m['traffic']))
    print(f"| {label} | {rc} | {len(m['rows'])} | {ok} | {m['minimum_ms']:.5f} | {m['maximum_ms']:.5f} | "
          f"{BOUND - m['maximum_ms']:.5f} ms ({100 * (BOUND - m['maximum_ms']) / BOUND:.1f} %) | {m['margin']:.4f}x | "
          f"{c['maximum_ms']:.5f} |" if c else '- |')
    if m['cpu_hz'] == 50000000 and (worst is None or m['maximum_ms'] > worst[1]):
        worst = (label, m['maximum_ms'])
print()
if worst:
    print(f'Worst contract-clock capture: {worst[0]}, {worst[1]:.5f} ms, {BOUND - worst[1]:.5f} ms under the 24.5 ms bound.')
for label in ('skip-copy', 'no-traffic', 'byte-only'):
    rc = (side / f'{label}.rc').read_text().strip() if (side / f'{label}.rc').exists() else 'running'
    extra = ''
    if label == 'byte-only' and (side / 'byte-only.log').exists():
        text = (side / 'byte-only.log').read_text()
        if '"minimum_slowdown"' in text:
            extra = ', minimum slowdown ' + text.split('"minimum_slowdown":', 1)[1].split('}')[0].strip()
    print(f'Control {label}: rc {rc}{extra}')
