from pathlib import Path
import datetime,json,re
base=Path('/data-2/milan/tmp/opt-a837/scale')
record=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),arms={})
for arm in ('32-d0','32-d8','64-d0','64-d8'):
 d=base/arm/'results'
 if not d.exists():continue
 rows=[]
 for p in sorted(d.glob('*.log')):
  with p.open('rb') as f:f.seek(max(0,p.stat().st_size-64000));tail=f.read().decode(errors='replace')
  ms=re.findall(r'^MS \d+ (\d+) ',tail,re.M)
  rows.append(dict(group=p.stem,ms=int(ms[-1]) if ms else None,
                   result=('PASS' if 'RESULT: PASS' in tail[-8000:] else 'FAIL' if 'RESULT:' in tail[-8000:] else None)))
 record['arms'][arm]=rows
 completed=[r['group'] for r in rows if r['result']]
 running=[f"{r['group']}={r['ms']}ms" for r in rows if not r['result']]
 print(arm,f'{len(completed)}/9 completed',','.join(completed),'; running',','.join(running))
(base/'progress.json').write_text(json.dumps(record,indent=2)+'\n')
print(record['at'])

# Keep the public handoff's status current while this measurement stage is active.
from zoneinfo import ZoneInfo
handoff=Path('$MANAGEMENT/2026-09-23/opt-a837/round1/HANDOFF-r1.md')
lines=handoff.read_text().splitlines()
if lines and lines[0].startswith('STATUS: ACTIVE'):
 counts=', '.join(f"{a} {sum(bool(r['result']) for r in rs)}/9" for a,rs in record['arms'].items())
 now=datetime.datetime.now(ZoneInfo('Europe/Warsaw')).strftime('%Y-%m-%d %H:%M CET')
 lines[0]=f'STATUS: ACTIVE, item 1 REVIEW READY; {counts} groups complete ({now}). ETA: full 32x32 matrix around 12:30–13:00 CET, then the 64x64 build attempt. MAAP grades and the full self-test retain their findings; no waiver.'
 handoff.write_text('\n'.join(lines)+'\n')
