"""Read-only wall-time forecast; never a measurement or qualification gate."""
import datetime,json,re,statistics,sys,time
from pathlib import Path
root=Path('$LANES/arty-split')
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
out=r/'final-census'
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import run,scenario
manifest=json.loads((out/'manifest.json').read_text())
completed=json.loads((out/'completed.json').read_text())
done={(x['variant'],x['group']) for x in completed}
live=json.loads((r/'live-status.json').read_text())
active={(x['variant'],x['group']):x['simulated_seconds'] for x in live['active']}
now=time.time();remaining=[];rates=[]
def waits(group):
    seconds=0
    for line in group.script().splitlines():
        if m:=re.fullmatch(r'wait cycles (\d+)',line):seconds+=int(m[1])/80_000_000
        elif m:=re.fullmatch(r'wait ms (\d+)',line):seconds=max(seconds,int(m[1])/1000)
    return seconds
for variant,wanted in manifest['groups'].items():
    directory=out/variant;spec=json.loads((directory/'build.json').read_text())
    for group in run.all_groups(scenario.point('arty-1x1',spec),spec):
        key=(variant,group.name)
        if group.name not in wanted or key in done:continue
        nominal=waits(group)
        if key in active:
            path=directory/'results'/(group.name+'.txt')
            elapsed=now-path.stat().st_mtime
            if elapsed>60:rates.append(active[key]/elapsed)
        remaining.append(dict(variant=variant,group=group.name,
                              remaining_simulated_seconds=max(0,nominal-active.get(key,0))))
rate=statistics.median(rates) if rates else None
work=sum(x['remaining_simulated_seconds'] for x in remaining)
record=dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status='FORECAST ONLY; not qualification evidence',completed=len(done),
            remaining=len(remaining),nominal_simulated_seconds=work,
            current_simulated_seconds_per_wall_second=rate,
            native_hours_at_four_legs=work/rate/4/3600 if rate else None,
            note='Explicit waits are a lower estimate; simulated instruction/response overhead and final grading are additional.')
(r/'remaining-work-estimate.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
