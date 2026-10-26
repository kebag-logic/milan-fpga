#!/usr/bin/env python3
"""Regrade available public traces, compare fresh deltas, audit path counts."""
import json
import os
from pathlib import Path
import sys
ROOT=Path(os.environ['REVIEW_ROOT']); PACKET=Path(os.environ['REVIEW_PACKET'])
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import scenario,grade,run
public=PACKET/'scratch/public/author-r2/receipts'
out=dict(raw_regrades=[],published_counts={},shutdown_counts={},fresh={},gates={})
for label in ['A1','A8','B1','B8','S1','S8','C-shutdown']:
    spec=json.loads((public/'builds'/f'{label}.build.json').read_text())
    point='8x8' if label.endswith('8') else '1x1'
    spec['elf']=str(PACKET/'scratch'/('A8' if point=='8x8' else 'A1')/'image/ctrl_app.elf')
    groups=scenario.all_groups(scenario.point(point,spec),spec)
    folder=public/'runs'/label
    results=[]
    for g in groups:
        f=folder/(g.name+'.json')
        if not f.exists():continue
        recorded=json.loads(f.read_text());results.append(recorded)
        log=folder/(g.name+'.log')
        if log.exists():
            got=grade.grade(log.read_text(),g,spec['sys_hz'],spec['cpu_hz'])
            assert got==recorded,(label,g.name)
            out['raw_regrades'].append(label+'/'+g.name)
    out['published_counts'][label]=run.counts(results)
    if label in ['S1','S8']:
        entries=[dict(group=g.name,name=p.name,path=p.path_key(),start=p.start,ends=p.ends)
                 for g in groups for p in g.probes]
        fixed=json.loads(json.dumps(results))
        for g in fixed:
            for r in g['probes']:
                if r['probe']=='control.shutdown.if0':r['path']=['adp.shutdown',0]
        out['shutdown_counts'][label]=dict(probes=entries,reported=run.counts(results),
                                          deduplicated=run.counts(fixed))
    if label in ['A1','A8']:
        fresh=PACKET/'measurements'/label/'results.json'
        if fresh.exists():
            j=json.loads(fresh.read_text());checks=[]
            for r in j['results']:
                recorded=json.loads((folder/(r['group']+'.json')).read_text())
                assert r==recorded,(label,r['group'])
                checks.append(r['group'])
            out['fresh'][label]=dict(exact_matches=checks,counts=j['counts'],refusals=j['refusals'])
for f in (public/'gates').glob('*.log'):
    out['gates'][f.name]=f.read_text().splitlines()[-3:]
(PACKET/'receipt-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('Public raw traces regraded identically:',len(out['raw_regrades']))
print('Published counts:',out['published_counts'])
print('Fresh matches:',out['fresh'])
print('SHUTDOWN counts:',{k:(v['reported'],v['deduplicated']) for k,v in out['shutdown_counts'].items()})
