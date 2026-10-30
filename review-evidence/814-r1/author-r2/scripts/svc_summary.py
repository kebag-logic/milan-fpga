"""svc_summary.py <side-dir>: each service run's exit status, verdict line, commands, flash operations and findings
(the receipt's budget and service findings, the heartbeat's worst gap), from the run's own log and JSON receipt."""
import json
import re
import sys
from pathlib import Path

side = Path(sys.argv[1])
print('| Shape | rc | Verdict | Commands | Erases / page programs / bytes (largest command) | Commits logged | Heartbeat max gap ms | Measurement-only budget findings | Service findings (the verdict) |')
print('|---|---:|---|---:|---|---:|---:|---:|---:|')
for label in ('1x1', '8x8'):
    rc_path = side / f'{label}-all.rc'
    rc = rc_path.read_text().strip() if rc_path.exists() else 'running'
    log = (side / f'{label}-all.log').read_text(errors='replace') if (side / f'{label}-all.log').exists() else ''
    verdict = next((l for l in log.splitlines() if l.startswith(('PASS', 'FAIL'))), '-')
    rec = side / f'service-{label}' / 'service-all-1-0-0.json'
    raw = side / f'service-{label}' / 'service-all-1-0-0.log'
    text = raw.read_text(errors='replace') if raw.exists() else ''
    ends = re.findall(r'kind=command_end index=(\d+) erases=(\d+) programs=(\d+) bytes=(\d+)', text)
    big = max(ends, key=lambda e: int(e[3])) if ends else None
    commits = len(re.findall(r'Milan NVM: commit .* acknowledged', text))
    if rec.exists() and rc != 'running':
        d = json.loads(rec.read_text())
        gap, bf, sf = d.get('heartbeat_max_gap_ms'), len(d.get('budget_findings', [])), len(d.get('service_findings', []))
        gap = f'{gap:.3f}' if isinstance(gap, float) else str(gap)
    else:
        gap = bf = sf = '-'
    flash = f'{big[1]} / {big[2]} / {big[3]}' if big else '-'
    print(f'| {label} | {rc} | {verdict} | {len(ends)} | {flash} | {commits} | {gap} | {bf} | {sf} |')
