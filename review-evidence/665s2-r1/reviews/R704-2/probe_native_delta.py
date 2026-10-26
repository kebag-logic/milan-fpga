#!/usr/bin/env python3
"""Repeat the unchanged earlier fan-out stimulus and falsify the owed-load claim."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(os.environ['REVIEW_ROOT']); PACKET=Path(os.environ['REVIEW_PACKET'])
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import scenario, grade

def execute(label, name, g, script=None):
    out=PACKET/'native-probes'/label;out.mkdir(parents=True,exist_ok=True)
    script_path=out/(name+'.txt');script_path.write_text(script if script is not None else g.script())
    with (out/(name+'.log')).open('w') as log:
        r=subprocess.run([str(PACKET/'scratch'/label/'native/Vsim'),str(script_path),'-'],
                         cwd=PACKET/'scratch'/label/'gateware',stdout=log,stderr=subprocess.STDOUT)
    assert r.returncode==0
    text=(out/(name+'.log')).read_text()
    result=grade.grade(text,g,100000000,50000000)
    (out/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    return result

def owed(label):
    spec=json.loads((PACKET/'scratch'/label/'build.json').read_text())
    p=scenario.point('1x1' if label=='A1' else '8x8',spec)
    g=scenario.owed_group(p)
    # Preserve seven commands ahead of the original input. Four more arrive
    # immediately behind it, bringing this channel to its admitted twelve.
    at=next(i for i,s in enumerate(g.steps) if s.startswith('wait drained'))
    extra=[f'frame 0 {scenario.acmp_cmd(p,"GET_RX_STATE",0,0x7390+n).hex()}' for n in range(4)]
    g.steps[at:at]=extra;g.load['acmp']+=4
    return execute(label,'owed-twelve',g)

def fanout():
    spec=json.loads((PACKET/'scratch/A8/build.json').read_text())
    p=scenario.point('8x8',spec)
    script=(PACKET/'scratch/public/reviews/R704-1/controls/fanout.txt').read_text()
    ch=scenario.CH['aecp']
    # The prior native stimulus is byte-for-byte unchanged. The declaration
    # adds only the endpoint metadata required by the corrected grader API.
    g=scenario.Group('review-fanout',probes=[scenario.Probe('review.fanout.if0',
       'two-interface SET_NAME fan-out','notify',f'rxc:{ch}',
       [f'resp:{ch}:7902',f'notify:{ch}:0010:0:0'],recipients=((scenario.CTL1,0),(scenario.CTL1,1)))])
    return execute('A8','prior-fanout',g,script)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    jobs=[pool.submit(owed,n) for n in ['A1','A8']]+[pool.submit(fanout)]
    results=[j.result() for j in jobs]
for r in results:
    print(r['group'],[(p['probe'],p['status'],p.get('ms')) for p in r['probes']])
