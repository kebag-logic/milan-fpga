#!/usr/bin/env python3
"""Independent failure probes; mutations affect only disposable inputs or memory."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch

ROOT=Path(os.environ['REVIEW_ROOT']); PACKET=Path(os.environ['REVIEW_PACKET'])
H=ROOT/'tb/verilator/ctrl_service_budget'
sys.path.insert(0,str(H))
import build, grade, scenario, selftest, run
out={}
ch=scenario.CH['aecp']
# These are the prior round's raw, unchanged counterexample bytes. Only the
# probe declaration supplies the new required causal selector and recipients.
probe=scenario.Probe('review.notify.if0','notification fan-out','notify',f'rxc:{ch}',
                    [f'resp:{ch}:41',f'notify:{ch}:0010:0:0'],recipients=((3,0),(4,1)))
for kind in ['late','missing']:
    text=(PACKET/'scratch/public/reviews/R704-1'/f'notification-{kind}-recipient.log').read_text()
    row=selftest.one(text,probe)
    out[kind]=row
assert out['late']['ms']==14 and not out['late']['within_t_svc']
assert out['missing']['status']=='no end'
# Independently compare each backlog population with the admission formula.
out['loads']={}
for label in ['A1','A8']:
    spec=json.loads((PACKET/'scratch'/label/'build.json').read_text())
    p=scenario.point('1x1' if label=='A1' else '8x8',spec)
    for g in scenario.backlog_groups(p):
        target={c:a['at_once'] for c,a in g.admission.items()}
        target['acmp']=scenario.admission('acmp',scenario.acmp_cmd(p,'GET_RX_STATE',0,0))['at_once']
        if 'adp' not in target:
            target['adp']=8
        out['loads'][label+'/'+g.name]=dict(load=g.load,at_once=target,
            below={c:[g.load.get(c,0),n] for c,n in target.items() if g.load.get(c,0)<n})

# Exercise both public CLI entry paths on genuinely reusable copied inputs.
src=PACKET/'scratch/A1'; dest=PACKET/'scratch/attestation'
shutil.copytree(src,dest,dirs_exist_ok=True)
spec=json.loads((dest/'build.json').read_text())
spec['elf']=spec['elf'].replace(str(src),str(dest))
spec['sources']=[s.replace(str(src),str(dest)) for s in spec['sources']]
for key in list(spec['inputs']):
    if key.startswith('external:'):
        original=Path(key.removeprefix('external:'))
        copied=dest/'external'/original.name;copied.parent.mkdir(exist_ok=True)
        shutil.copy2(original,copied)
        spec['inputs']['build:external/'+original.name]=spec['inputs'].pop(key)
        spec['sources']=[str(copied) if s==str(original) else s for s in spec['sources']]
(dest/'build.json').write_text(json.dumps(spec))
build.reused(dest)
out['reuse_unchanged']=True
out['attestation']=[]
inputs=[dest/'image/ctrl_app.elf',*sorted((dest/'gateware').glob('*.init')),
        dest/'gateware/sim.v',*sorted((dest/'external').glob('Vexii*.v'))]
for path in inputs:
    saved=path.read_bytes()
    for action in ['changed','missing']:
        if action=='changed':path.write_bytes(saved+b'\n')
        else:path.unlink()
        for flag in ['--reuse-build','--regrade']:
            cmd=[sys.executable,'-B',str(H/'run.py'),'--point','1x1','--build-dir',str(dest),flag,
                 '--groups','control','--out',str(PACKET/'scratch/attestation-out'),'--jobs','1',
                 '--record-budget-findings']
            r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            assert r.returncode==1 and action in r.stdout,(path,flag,r.stdout)
            out['attestation'].append(dict(input=str(path.relative_to(dest)),action=action,
                                          flag=flag,returncode=r.returncode,stdout=r.stdout))
        path.write_bytes(saved)
bad=copy.deepcopy(spec);bad['inputs']['unresolved.elf']='0'*64
(dest/'build.json').write_text(json.dumps(bad))
try:build.reused(dest);raise AssertionError('unresolved key accepted')
except RuntimeError as e:out['unresolved']=str(e)
(dest/'build.json').write_text(json.dumps(spec))

# Identical selected-group request to round one, now refusing both absent logs.
out['missing_logs']=[]
for record in [False,True]:
    empty=PACKET/'scratch/empty-regrade';empty.mkdir(exist_ok=True)
    for g in scenario.backlog_groups(scenario.point('1x1',spec)):
        (empty/(g.name+'.txt')).write_text(g.script())
    cmd=[sys.executable,'-B',str(H/'run.py'),'--point','1x1','--build-dir',str(dest),'--regrade',
         '--out',str(empty),'--groups','backlog,backlog-adp','--jobs','1']
    if record:cmd.append('--record-budget-findings')
    r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assert r.returncode==1 and 'backlog: no recorded log' in r.stdout and 'backlog-adp: no recorded log' in r.stdout
    out['missing_logs'].append(dict(record=record,returncode=r.returncode,stdout=r.stdout))

partial=PACKET/'scratch/partial-regrade';partial.mkdir(exist_ok=True)
for suffix in ['txt','log']:
    shutil.copy2(PACKET/'scratch/public/author-r2/receipts/runs/A1'/('control.'+suffix),partial/('control.'+suffix))
backlog=scenario.backlog_groups(scenario.point('1x1',spec))[0]
(partial/'backlog.txt').write_text(backlog.script())
out['partial_regrade']=[]
for selected,record in [('control,backlog',False),('control,backlog',True),('control',False)]:
    cmd=[sys.executable,'-B',str(H/'run.py'),'--point','1x1','--build-dir',str(dest),'--regrade',
         '--out',str(partial),'--groups',selected,'--jobs','1']
    if record:cmd.append('--record-budget-findings')
    r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assert r.returncode==(1 if ',' in selected else 0),(selected,r.stdout)
    if ',' in selected:assert 'backlog: no recorded log' in r.stdout
    out['partial_regrade'].append(dict(selected=selected,record=record,returncode=r.returncode,stdout=r.stdout))

# Demonstrate which headline figures are changed by the protected rules.
oracle=json.loads((H/'oracle.json').read_text());baseline=selftest.regraded(oracle)
out['headline_controls']=[]
for name in ["clock ratio: a pass's milliseconds from the bus clock",
             "clock ratio: a pass's bus cycles equal its CPU cycles",
             'pass bound: it starts at the input, not at the running pass',
             "composition: the composed maximum is the run's worst pass"]:
    with selftest.mutated(name):
        mutated=selftest.regraded(oracle)
        failed=[n for n,ok,_ in selftest.checks() if not ok]
    before=dict(headline=selftest.headline(baseline),bounds=[r.get('bound_ms') for r in baseline['probes']])
    after=dict(headline=selftest.headline(mutated),bounds=[r.get('bound_ms') for r in mutated['probes']])
    assert before!=after and failed
    out['headline_controls'].append(dict(mutation=name,before=before,after=after,failed_checks=failed))
(PACKET/'delta-probes.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: prior raw fan-out counterexamples, attestation CLI refusals, absent logs, headline mutations')
print('Admission shortfalls:',{k:v['below'] for k,v in out['loads'].items() if v['below']})
