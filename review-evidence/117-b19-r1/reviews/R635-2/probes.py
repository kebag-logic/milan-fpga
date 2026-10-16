#!/usr/bin/env python3
"""Independent offline checks. Usage: probes.py AUTHOR_PACKET RAW_ROOT OUTPUT_PACKET."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

packet, raw, out = map(lambda x: Path(x).resolve(), sys.argv[1:])
scratch = out / 'scratch' / 'probes'
scratch.mkdir(parents=True, exist_ok=True)
def module(name):
    spec = importlib.util.spec_from_file_location(name, packet / 'tools' / (name + '.py'))
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
grader = module('r2_box3_grade')
model, edges, ranges = grader.grade(packet)
rows = []
for edge in edges:
    m = model['actions'][f"cycle{edge['cycle']:02d}"]
    bracket = dict(last_before=edge['last_before_s'], first_after=edge['first_after_s'], how=edge['how'])
    a, b = bracket['last_before'], bracket['first_after']
    ua, ub = [grader.u_of(m, x) for x in bracket['how']]
    effect = edge['edge'] == 'first tu=1 CRF PDU'
    for label, cause in [('before', a-m['d_lo_s']+ua-0.0001),
                         ('after', b-m['d_hi_s']-ub+(0.002 if effect else 0)+0.0001)]:
        result = grader.grade_edge(edge['edge'], bracket, cause, m, effect)
        assert result['verdict'] == 'FAIL'
        rows.append(dict(cycle=edge['cycle'], edge=edge['edge'], control=label, verdict=result['verdict']))
(out / 'edge-boundary-probes.json').write_text(json.dumps(rows, indent=2)+'\n')

# Re-derive transitions without the published transition-search implementation.
published = json.loads((packet/'round2/gm-steps-r2.json').read_text())
history = []
for run in range(1, 6):
    name = f'gm{run:02d}'
    events = [json.loads(x) for x in (raw/name/'events.jsonl').read_text().splitlines()]
    start = next(x['t'] for x in events if x['kind']=='gm-start')
    samples = []
    for line in (raw/name/'console.jsonl').read_text().splitlines():
        record = json.loads(line)
        if record['cmd']=='milan_status':
            words = dict(re.findall(r'(\w+)=([a-zA-Z0-9_]+)',record['raw']))
            samples.append((record['t']-start,record['end']-start,words))
    for label, lo, hi in [('takeover',-9,27),('release',27,200)]:
        rises = [k for k in range(1,len(samples)) if lo<=samples[k][0]<hi
                 and samples[k][2]['TU']=='1' and samples[k-1][2]['TU']=='0']
        assert len(rises)==1
        k=rises[0]
        healthy=lambda s: all(s[2][key]==value for key,value in [('SYNC','1'),('ASCAPABLE','1'),('TU','0')])
        clear=next(j for j in range(k+1,len(samples)) if samples[-1][0]>=samples[j][0]+2
                   and all(healthy(s) for s in samples[j:] if s[0]<samples[j][0]+2))
        expected=next(x for x in published['rows'] if x['run']==name and x['edge']==label)
        assert round(samples[k][0],3)==expected['tu']['tu_set']['t']
        assert round(samples[clear][0],3)==expected['tu']['steady_clear']['t']
        history.append(dict(run=name,edge=label,set=round(samples[k][0],3),clear=round(samples[clear][0],3)))
(out/'independent-tu.json').write_text(json.dumps(history,indent=2)+'\n')

# Exercise the complete grade process, rather than only the poll helper.
work=scratch/'packet'
shutil.copytree(packet,work,dirs_exist_ok=True)
rawcopy=scratch/'raw'
for run in range(1,6):
    name=f'gm{run:02d}'
    (rawcopy/name).mkdir(parents=True,exist_ok=True)
    for file in ['events.jsonl','console.jsonl','controller.jsonl']:
        shutil.copyfile(raw/name/file,rawcopy/name/file)
baseline=(rawcopy/'gm01/controller.jsonl').read_bytes()
control=[]
for label, index in [('takeover',15),('release',70)]:
    records=[json.loads(x) for x in baseline.splitlines()]
    polls=[x for x in records if x.get('role')=='dut' and x.get('what')=='avb']
    polls[index]['response']['decoded']['as_capable']=0
    (rawcopy/'gm01/controller.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in records))
    result=subprocess.run([sys.executable,str(work/'tools/r2_gm.py'),str(rawcopy),str(work)],capture_output=True,text=True,timeout=60)
    assert result.returncode==1
    derived=json.loads((work/'round2/gm-steps-r2.json').read_text())
    failures=[(r['run'],r['edge']) for r in derived['rows'] if not r['pass_']]
    assert failures==[('gm01',label)]
    control.append(dict(plant=label,returncode=result.returncode,failures=failures))
(rawcopy/'gm01/controller.jsonl').write_bytes(baseline)
(out/'poll-process-probes.json').write_text(json.dumps(control,indent=2)+'\n')
print('54 edge-boundary controls rejected; 10 transitions independently match; two process-level poll mutations exit 1 at the intended edge.')
