#!/usr/bin/env python3
"""Probe the published comparison on disposable, non-identifying fixtures.

Usage: python3 restore_controls.py EVIDENCE_ROOT SCRATCH_DIRECTORY
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

evidence,scratch=map(Path,sys.argv[1:])
scratch.mkdir(parents=True,exist_ok=True)
source=(evidence/'author/restore_compare.py').read_text()
old="RAW=Path('/tmp/653-b12/raw')"
assert source.count(old)==1
source=source.replace(old,'RAW=Path(sys.argv[1])')
script=scratch/'comparison.py';script.write_text(source)
baseline=[]
for role,counts in [('dut',(4,4,2,2)),('peer',(14,14,2,1))]:
    for cat,count in zip(('bindings','formats','maps','clocks'),counts):
        for i in range(count):
            r={'role':role,'status':0,'what':role+'-'+cat+'-'+str(i)}
            if cat=='bindings':r.update(what='rx-state-'+role+'-'+str(i),conn_count=0)
            if cat=='formats':r.update(cmd='GET_STREAM_FORMAT',payload='000500000205022001006000')
            if cat=='maps':r.update(cmd='GET_AUDIO_MAP',payload='00000000')
            if cat=='clocks':r.update(cmd='GET_CLOCK_SOURCE',payload='000a00000001')
            baseline.append(r)


def run(name,start,end,expected):
    folder=scratch/name;folder.mkdir(exist_ok=True)
    for tag,rows in [('start',start),('end',end)]:
        (folder/('census-'+tag+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in rows))
        for other in ('dut-descs','peer-descs'):(folder/(other+'-'+tag+'.jsonl')).write_text('')
    result=subprocess.run([sys.executable,str(script),str(folder)],capture_output=True,text=True,timeout=30)
    assert result.returncode==expected,(name,result.returncode)
    data=json.loads(result.stdout)
    print(json.dumps({'fixture':name,'rc':result.returncode,'accepted':data['pass_restore'],
                      'group_observation_counts':[r['observations'] for r in data['rows']]}))


run('successful-equal',baseline,baseline,0)
end=copy.deepcopy(baseline)
next(r for r in end if r.get('cmd')=='GET_CLOCK_SOURCE')['payload']='000a00000002'
run('changed-clock',baseline,end,1)
run('missing-one-endpoint',baseline,baseline[:-1],1)
failed=copy.deepcopy(baseline)
for row in failed:row['status']=1
run('matching-error-statuses',failed,failed,0)
run('missing-both-endpoints',baseline[:-1],baseline[:-1],0)
run('empty-inventory',[],[],0)
print('CONFIRMED: equality detects differences but accepts matching errors and absent inventory')
