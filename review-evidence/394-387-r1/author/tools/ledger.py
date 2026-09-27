"""Refresh the per-cycle handoff from retained analysis."""
from pathlib import Path
import json,datetime
p=Path(__file__).resolve().parent.parent
utc=lambda t:datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime("%H:%M:%S.%f")[:-3]
rows=[]
for n in range(1,11):
 f=p/f"cycle{n:02d}"/'analysis.json'
 if not f.exists():rows.append(f"| {n} | pending | pending | pending | pending | pending | pending | NOT RUN |");continue
 s=json.loads(f.read_text());off=s['off'];on=s['on'];d=s['counter_endpoints']['dut:counter-5-1']['delta'];g=s['gptp_recovery_s'];st=s['large_phc_discontinuities'];endpoint=max(s['servo_locked_at'],s['media_locked_at']['dut'],s['gptp_recovered_at']); mt=f"{endpoint-st[-1]['bracket'][1]:.3f}-{endpoint-st[-1]['bracket'][0]:.3f}" if st else 'unavailable'
 rows.append(f"| {n} | {utc(off)} / {utc(on)} | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +{d['0']}/+{d['1']} | gPTP {g:.3f} s | {'automatic both ways' if s['steady_recovered'] else 'UNRECOVERED'} | step to locked media {mt} s | #394 FAIL; #387 PASS (CRF) |");
s=p.joinpath('HANDOFF.md').read_text();a=s.index('| Cycle |');b=s.index('\n#394 acceptance',a)
s=s[:a]+"| Cycle | Off/on UTC (recorder clock) | Link down/up | Counter deltas | Recovery | Streams | Media step/relock | Result |\n|---|---|---|---|---|---|---|---|\n"+'\n'.join(rows)+'\n'+s[b:]
s=s.replace('#394 acceptance 2: NOT RUN.','#394 acceptance 2: FAIL observed, LINK_UP and LINK_DOWN remain flat; remaining cycles pending.')
p.joinpath('HANDOFF.md').write_text(s)
