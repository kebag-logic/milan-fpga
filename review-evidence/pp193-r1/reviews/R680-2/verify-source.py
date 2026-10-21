#!/usr/bin/env python3
"""Verify exact tracked blob bytes, executable bits, index and nested pins."""
import hashlib, os, pathlib, stat, subprocess, sys
p=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent
def git(*args):return subprocess.check_output(['git','-C',str(p),*args])
head='7b424cdfe111a426f00517ff471246b4b9650726'
tree='4142dcfe858d04687f3f37847a67f7c69d6ae0ea'
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
assert git('write-tree').decode().strip()==tree
assert not git('status','--porcelain=v1','--ignored')
inventory=[];links=[]
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not row:continue
    meta,name=row.split(b'\t',1);mode,kind,oid=meta.decode().split();name=os.fsdecode(name);f=p/name
    if kind=='commit':
        links.append((name,oid));assert subprocess.check_output(['git','-C',str(f),'rev-parse','HEAD']).decode().strip()==oid
        continue
    data=os.fsencode(os.readlink(f)) if mode=='120000' else f.read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert got==oid,name
    if mode!='120000':assert bool(f.stat().st_mode&stat.S_IXUSR)==(mode=='100755'),name
    inventory.append(f'{mode} {oid} {name}')
(out/'tracked-blobs.txt').write_text('\n'.join(inventory)+'\n')
lines=[f'HEAD {head}',f'TREE/index {tree}',f'PASS: {len(inventory)} tracked blob bytes and modes match HEAD',f'PASS: {len(links)} gitlinks match HEAD (zero means no required nested submodules)','PASS: clean status including ignored files','Source checkout never edited; disposable exports only.']
for a,b in [('21601694','HEAD'),('6ddfcda4','HEAD')]:
    for f in ['hdl/srp/KL_srp_listener_fsm.sv','hdl/srp/KL_srp_top.sv','hdl/top/protocol_processor_top.sv']:
        texta=git('show',a+':'+f).decode();textb=git('show',b+':'+f).decode()
        def header(s):
            start=s.index('module ');end=s.index('\n);',start)+3;return s[start:end]
        assert header(texta)==header(textb),(a,b,f)
        lines.append(f'PASS unchanged port/parameter header {a}..{b}: {f}')
    for f in ['docs/architecture/02_interfaces.md','docs/architecture/07_memory_maps.md']:
        assert git('show',a+':'+f)==git('show',b+':'+f)
        lines.append(f'PASS unchanged {a}..{b}: {f}')
changed=git('diff','--name-only','57fb7dd','HEAD').decode().splitlines()
assert changed==['tb/srp_top/README.md']
lines.append('PASS 57fb7dd..HEAD changes only tb/srp_top/README.md; all executable input blobs identical')
(out/'source-integrity.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
