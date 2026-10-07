#!/usr/bin/env python3
"""Repeat record generators in a disposable registered parent clone."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from copy import deepcopy

root=Path.cwd();packet=Path(__file__).resolve().parent;scratch=packet/'scratch';tree=scratch/'parent-notify'
env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
commands=[['python3','scripts/check_port_contracts.py','--write-budget'],
          ['python3','scripts/measure_naming.py','--write-budget'],
          ['python3','docs/diagrams/submodule_boundaries.gen.py'],
          ['bash','syn/yosys/ooc.sh','--record-rom-digests']]
files=['scripts/port_docs.budget','scripts/naming.budget','syn/yosys/rom_digests.tsv',
       'docs/diagrams/submodule_boundaries.svg','docs/diagrams/submodule_boundaries.drawio',
       'docs/diagrams/submodule_boundaries.png','docs/diagrams/PNG_MANIFEST.json']
before={p:(tree/p).read_bytes() for p in files}
records=[]
for repeat in range(2):
    for i,cmd in enumerate(commands):
        name=f'records-{repeat+1}-{i+1}'
        r=subprocess.run(cmd,cwd=tree,env=env,capture_output=True)
        log=(r.stdout+r.stderr).replace(str(scratch).encode(),b'$SCRATCH')
        (packet/(name+'.log')).write_bytes(log);(packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
        records.append({'name':name,'command':cmd,'rc':r.returncode,'sha256':hashlib.sha256(log).hexdigest()})
        assert r.returncode==0,(cmd,log.decode())
    assert all((tree/p).read_bytes()==v for p,v in before.items())

# Exercise the committed resource policy against its current real baseline.
sys.path.insert(0,str(root/'syn/ooc'))
spec=importlib.util.spec_from_file_location('resource_gate',root/'syn/ooc/pp_resource_gate.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
base=json.loads((root/'syn/ooc/pp_resource_baseline.json').read_text())['endpoints']['route-1x1']
probes=[]
for name,field,value,expected in [('unchanged',None,None,0),('LUT-growth','LUT',50458,1),
    ('slice-growth','SLICE',15815,1),('new-RAMB36','RAMB36',75,1),('setup-floor','WNS_ns',0.029,1),
    ('hold-floor','WHS_ns',-0.001,1),('BRAM-reserve','BRAM_TILE',122,1)]:
    candidate=deepcopy(base['record'])
    if field:
        candidate['inputs_sha256']='0'*64;candidate['figures'][field]=value
    rc,lines=gate.judge(base,candidate,[])
    assert rc==expected,(name,rc,lines)
    probes.append({'name':name,'expected':expected,'actual':rc,'diagnostic':lines})
candidate=deepcopy(base['record']);candidate['identity']['flow']=candidate['identity']['flow'][1:]
rc,lines=gate.judge(base,candidate,[]);assert rc==2
probes.append({'name':'unrecorded-worker-setting','expected':2,'actual':rc,'diagnostic':lines})
rc,lines=gate.judge(base,base['record'],['1 unrouted net']);assert rc==1
probes.append({'name':'unrouted-net','expected':1,'actual':rc,'diagnostic':lines})
print(json.dumps({'generator_runs':records,'repeated_bytes_identical_to_head':{p:hashlib.sha256(v).hexdigest() for p,v in before.items()},'resource_policy_probes':probes},indent=2))
