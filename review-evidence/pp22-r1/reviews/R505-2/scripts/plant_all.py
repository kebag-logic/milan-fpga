#!/usr/bin/env python3
"""Plant every checked-in patch and exact-text campaign arm, without builds."""
import argparse, collections, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('repo',type=Path); p.add_argument('packet',type=Path); a=p.parse_args()
sys.dont_write_bytecode=True
work=a.packet/'scratch/planting'; work.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(work); tempfile.tempdir=str(work)
rows=[]
def load(rel):
    path=a.repo/rel
    sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location('plant_'+path.parent.name+'_'+path.stem,path)
    module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module)
    return module
patchtree=work/'patch-tree'
subprocess.run(['git','-C',str(a.repo),'archive','--output='+str(work/'source.tar'),'HEAD'],check=True)
import tarfile
with tarfile.open(work/'source.tar') as t: t.extractall(patchtree,filter='data')
paths=subprocess.check_output(['git','-C',str(a.repo),'ls-files','tb/**/*.patch'],text=True).splitlines()
for rel in paths:
    rc=subprocess.run(['git','apply','--check',str(a.repo/rel)],cwd=patchtree,capture_output=True,text=True)
    assert rc.returncode==0,(rel,rc.stderr)
    subprocess.run(['git','apply',str(a.repo/rel)],cwd=patchtree,check=True,capture_output=True)
    subprocess.run(['git','apply','--reverse',str(a.repo/rel)],cwd=patchtree,check=True,capture_output=True)
    rows.append(dict(population='patch',name=rel,pass_=True))
def plant(population,name,edits,fn=None):
    # Each arm starts with its exact-head source, never a previous mutation.
    with tempfile.TemporaryDirectory(dir=work) as tmp:
        tree=Path(tmp)
        for rel,_,_,_ in edits:
            out=tree/rel; out.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(a.repo/rel,out)
        if fn:
            reason=fn(tree,tuple((r,o,n) for r,o,n,_ in edits)); assert not reason,(population,name,reason)
        else:
            for rel,old,new,count in edits:
                target=tree/rel; text=target.read_text(); assert text.count(old)==count,(population,name,rel,text.count(old),count)
                target.write_text(text.replace(old,new))
        rows.append(dict(population=population,name=name,pass_=True,
                         outputs={r:hashlib.sha256((tree/r).read_bytes()).hexdigest() for r,_,_,_ in edits}))
for name in ['notify','acmp','d3']:
    m=load(f'tb/pp_top/{name}_mutants.py')
    for ix,arm in enumerate(m.MUTANTS):
        plant(name,f'{ix}:{arm.name}',[(r,o,n,1) for r,o,n in arm.edits],m.plant)
m=load('tb/pp_top/gsi_mutants.py')
for name,rel,old,new,count,_ in m.mutations(): plant('gsi',name,[(rel,old,new,count)])
m=load('tb/srp_admission/mutants.py')
for name,edits,_ in m.MUTANTS: plant('admission',name,[(m.ADMISSION,o,n,c) for o,n,c in edits])
m=load('tb/acmp_talker/retry_mutants.py')
for name,edits in m.MUTATIONS.items():
    if isinstance(edits[0],str): edits=(edits,)
    plant('retry',name,[(m.RTL,o,n,1) for o,n in edits])
plant('name-write','decode',[('hdl/aecp/KL_aecp_engine.sv','  assign name_wr_o = d3_nchg_w;',
    '  assign name_wr_o = txn_valid_i && txn_ready_o && sname_w;',1)])
plant('descriptor-guard','hold-deleted',[('hdl/aecp/KL_aecp_desc_mem_guard.sv',' && !owed_r','',2)])
m=load('tb/nvm_port/measure_figures.py')
# The figures driver creates its own source copy at import, within TMPDIR.
# Exercise its actual refusal/restore logic while replacing only the build callback.
m.run_suite=lambda *args: (0,0,0)
for name,_,edits in m.MUTATIONS + m.MODELS:
    m.apply_edits(edits)
    rows.append(dict(population='nvm-figures',name=name,pass_=True))
for line,name in m.ARMS:
    m.with_arm_disabled(line)
    rows.append(dict(population='nvm-line-arms',name=f'{line}:{name}',pass_=True))
for name,anchor,code in m.MATRIX_FORMS:
    m.apply_edits([(m.SIM,anchor,code+anchor)])
    rows.append(dict(population='nvm-historical-anchors',name=name,pass_=True))
counts=dict(collections.Counter(r['population'] for r in rows))
result=dict(head=subprocess.check_output(['git','-C',str(a.repo),'rev-parse','HEAD'],text=True).strip(),
            total=len(rows),counts=counts,results=rows,meaning='planting only; no mutation kill claim')
(a.packet/'receipts/planting.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(total=len(rows),counts=counts,all_pass=True)))
