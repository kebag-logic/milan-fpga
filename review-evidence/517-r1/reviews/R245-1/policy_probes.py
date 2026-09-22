#!/usr/bin/env python3
"""Black-box policy CLI fixtures derived from the original failure receipt."""
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(sys.argv[1]).resolve(); OUT=Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True,exist_ok=False)
SOURCE=(ROOT/'scripts/check_baremetal_only.py').read_text()
OLD=subprocess.check_output(['git','-C',str(ROOT),'show','7ab1c8d0:scripts/check_baremetal_only.py']).decode()
public=Path(__file__).parent/'public/source-first-failure/29.log'
fixtures={}
for path,line in re.findall(r'  - (tb/[^:]+):(\d+):',public.read_text()):
    fixtures[path,int(line)]=(ROOT/path).read_text().splitlines()[int(line)-1]
assert len(fixtures)==20
PRODUCT='docs/overview/FULL_FPGA_SOLUTION.md'
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
env['PYTHONDONTWRITEBYTECODE']='1'
rows=[]

def execute(label,path,payload,expected,needle=None,source=SOURCE):
    dst=OUT/label;dst.mkdir()
    (dst/'scripts').mkdir();(dst/'scripts/check_baremetal_only.py').write_text(source)
    product=dst/PRODUCT;product.parent.mkdir(parents=True);product.write_text('Fabric and bare metal.\n')
    target=dst/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(payload+'\n')
    setup=[]
    for argv in (['git','init','-q'],['git','add','--all']):
        p=subprocess.run(argv,cwd=dst,env=env,capture_output=True);assert p.returncode==0,p.stderr
        setup.append(argv)
    argv=['python3','-B','scripts/check_baremetal_only.py','--check']
    p=subprocess.run(argv,cwd=dst,env=env,capture_output=True,text=True,timeout=15)
    (dst/'stdout').write_text(p.stdout);(dst/'stderr').write_text(p.stderr)
    accepted=p.returncode==expected and (needle is None or needle in p.stdout)
    row=dict(label=label,path=path,payload=payload,setup=setup,argv=argv,exit=p.returncode,expected=expected,needle=needle,accepted=accepted)
    (dst/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
    return accepted

for n,((path,line),payload) in enumerate(fixtures.items()):
    label=f'{n:02d}'
    assert execute(label+'-positive',path,payload,0)
    assert execute(label+'-original-checker',path,payload,1,source=OLD)
    tokens=[]
    if re.search('linux',payload,re.I):tokens.append(('Linux','[T]'))
    if '/proc' in payload:tokens.append(('/proc','[R]'))
    for k,(token,klass) in enumerate(tokens):
        assert execute(label+f'-wrong-file-{k}','other.py',payload,1,klass)
        assert execute(label+f'-same-line-{k}',path,payload+' # '+token,1,klass)
        assert execute(label+f'-unrelated-line-{k}',path,payload+'\nThe target requires '+token,1,klass)
        assert execute(label+f'-product-{k}',PRODUCT,payload,1,'[P]' if token=='Linux' else '[R]')
    for suffix,klass in [('rootfs','[T]'),('/etc/fstab','[R]'),('PCM ring','[S]'),('hostplane','[H]'),('CONFIG_NET=y','[K]'),('--sound-card','[O]')]:
        assert execute(label+'-extra-'+klass[1],path,payload+' # '+suffix,1,klass)
    if 'Linux' in payload:
        assert execute(label+'-prefix',path,payload.replace('Linux','Linuxptp'),1,'[T]')
    if '/proc' in payload:
        assert execute(label+'-altered-path',path,payload.replace('/proc','/proc/foreign'),1,'[R]')

# A complete source AST comparison, removing only the documented addition.
before=ast.parse(OLD);after=ast.parse(SOURCE)
for node in list(after.body):
    if isinstance(node,ast.FunctionDef) and node.name in ('_sim_pool_host_fixtures','_arms_sim_pool_host_masks'):
        after.body.remove(node)
    if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('TERM_MASKS','HOST_RUNTIME_MASKS'):
        retained=[(k,v) for k,v in zip(node.value.keys,node.value.values) if not k.value.startswith('tb/verilator/milan_dp/')]
        node.value.keys=[k for k,v in retained];node.value.values=[v for k,v in retained]
    if isinstance(node,ast.FunctionDef) and node.name=='selftest':
        for sub in ast.walk(node):
            if isinstance(sub,ast.Tuple):sub.elts=[x for x in sub.elts if not isinstance(x,ast.Name) or x.id!='_arms_sim_pool_host_masks']
assert ast.dump(before)==ast.dump(after),'undocumented policy AST change'

# Verify that representative broadening defects fail these independent probes.
prefix='\nif __name__ == "__main__":'
mutations=[
 ('global-token','TERM_MASKS["tb/verilator/milan_dp/sim_pool.py"] = re.compile("Linux")','tb/verilator/milan_dp/sim_pool.py','The target requires Linux','[T]'),
 ('whole-line','TERM_MASKS["tb/verilator/milan_dp/README.md"] = re.compile("^Linux.*")','tb/verilator/milan_dp/README.md','Linux subreaper support is required before any child starts. rootfs','[T]'),
 ('wrong-file','TERM_MASKS["other.py"] = TERM_MASKS["tb/verilator/milan_dp/README.md"]','other.py','Linux subreaper support is required before any child starts.','[T]'),
 ('global-path','HOST_RUNTIME_MASKS["tb/verilator/milan_dp/test_sim_pool.py"] = re.compile("/proc")','tb/verilator/milan_dp/test_sim_pool.py','The target requires /proc','[R]'),
 ('no-boundary','TERM_MASKS["tb/verilator/milan_dp/sim_pool.py"] = re.compile(r"(?<=Every leg is its own session and process group, reading /dev/null\\. )Linux")','tb/verilator/milan_dp/sim_pool.py','Every leg is its own session and process group, reading /dev/null. Linuxptp','[T]')]
mutrows=[]
for name,addition,path,payload,klass in mutations:
    mutated=SOURCE.replace(prefix,'\n'+addition+'\n'+prefix)
    caught=not execute('mutant-'+name,path,payload,1,klass,mutated)
    assert caught,name
    mutrows.append(dict(name=name,defect_detected=caught))
(OUT/'results.json').write_text(json.dumps(dict(fixtures=len(fixtures),cases=rows,mutations=mutrows,old_policy_ast_unchanged=True),indent=2)+'\n')
print('literal CLI cases',len(rows)-len(mutrows),'all passed; planted defects',len(mutrows),'all detected; old policy AST unchanged')
