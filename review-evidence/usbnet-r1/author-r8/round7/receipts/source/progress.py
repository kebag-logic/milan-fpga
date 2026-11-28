from pathlib import Path
import json,re,time,shutil
root=Path('$VALIDATION_STORAGE/usbnet-a855/round7/census')
old=Path('$VALIDATION_STORAGE/artysplit-a829/r10/final-census')
packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
def cycles(p):
 if not p.exists():return 0
 with p.open('rb') as f:
  f.seek(max(0,p.stat().st_size-12000));s=f.read().decode(errors='replace')
 m=re.search(r'SUMMARY sys=(\d+)',s)
 if m:return int(m[1])
 vals=[int(m[1]) for m in re.finditer(r'(?m)^(?:SPAN|CALL|PASS|TX|EGRESS|TXC) (\d+) ',s)]
 return max(vals,default=0)
manifest=json.loads((root/'manifest.json').read_text())
ends={(v,g):cycles(old/v/'results'/(g+'.log')) for v,gs in manifest['groups'].items() for g in gs}
extra=root.with_name('census-supplemental')
progress=sum(min(end,max(cycles(root/v/'results'/(g+'.log')),cycles(extra/v/'results'/(g+'.log')))) for (v,g),end in ends.items())/sum(ends.values())
rows=json.loads((root/'completed.json').read_text()) if (root/'completed.json').exists() else []
rows+=json.loads((extra/'completed.json').read_text()) if (extra/'completed.json').exists() else []
replay=json.loads((packet/'replay.json').read_text()) if (packet/'replay.json').exists() else {}
finding_rows=[]
for directory in (root,extra):
 f=directory/'findings.json'
 if f.exists():finding_rows+=json.loads(f.read_text())
live=[]
for f in (packet/'egress-cases').glob('*/*.json'):
 try:live.append(json.loads(f.read_text()))
 except json.JSONDecodeError:pass
r=dict(live_replayed=len(live),replay_failures=[x['case'] for x in live if x['result'].get('refused') or x['result'].get('agree_ps')],live_max_wait_us=max((x['result'].get('wait_ps',0) for x in live),default=0)/1e6,finding_cases=[x['variant']+'/'+x['group'] for x in finding_rows],utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),completed=len(rows),total=len(ends),estimated_trace_fraction=round(progress,3),baseline_replayed=len(replay),data_free_gb=round(shutil.disk_usage('/data').free/1e9,2),findings=(root/'findings.json').exists() or (extra/'findings.json').exists(),status=manifest['status'])
print(json.dumps(r))
(packet/'progress.json').write_text(json.dumps(r,indent=2)+'\n')
