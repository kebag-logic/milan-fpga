#!/usr/bin/env python3
import json,sys
from pathlib import Path
T=Path('<scratch>'); tree,point,arm=sys.argv[1:]
b=T/'meas/full'/tree/point/arm; out=T/'checkpoint'/tree/point/arm
sys.path.insert(0,str(T/'clones'/tree/'tb/verilator/ctrl_service_budget'))
import run,scenario
spec=json.loads((b/'build.json').read_text()); groups=[g for g in run.all_groups(scenario.point(point,spec),spec) if g.name.startswith('backlog-adp@')]
assert len(groups)==72
for g in groups:
 assert not g.save.get('journal')
 (out/(g.name+'.txt')).write_text(g.script())
(out/'manifest').write_text(''.join(f'{out}/{g.name}.txt {out}/{g.name}.log\n' for g in groups))
