#!/usr/bin/env python3
"""Regenerate ROMs outside the clone, run documentation gates, check tracked identity."""
import argparse, hashlib, os, pathlib, subprocess
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parent
def git(*args): return subprocess.check_output(['git','-C',str(a.repo),*args])
assert git('rev-parse','HEAD').decode().strip()=='409c3075a6c5525d283de5a93584ad87a4528137'
assert git('rev-parse','HEAD^{tree}').decode().strip()=='b552de2244475b15bfc430b683f8a4fe9c6a7db3'
with (root/'docs-check.log').open('w') as f:
    r=subprocess.run(['make','-j16','docs'],cwd=a.repo,stdout=f,stderr=subprocess.STDOUT)
(root/'docs-check.rc').write_text(str(r.returncode)+'\n');assert r.returncode==0
rows=[]
for path,args in [('tb/verilator/engine/gptp_ucode.hex',['--clk-hz','2000000','--cease-ms','3000']),('tb/tsngen/gptp_ucode.hex',['--clk-hz','2000000']),('tb/verilator/ucpu/gptp_ucode.hex',[]),('syn/ooc/work/gptp_ucode.hex',[])]:
    dst=root/'scratch'/('regen-'+path.replace('/','-'))
    c=subprocess.run(['python3',str(a.repo/'hdl/ucode/gen_gptp_ucode.py'),*args,'-o',str(dst)],capture_output=True,text=True,check=True)
    assert dst.read_bytes()==(a.repo/path).read_bytes(),path
    rows.append(path+' '+hashlib.sha256(dst.read_bytes()).hexdigest()+' byte-identical\n'+c.stdout)
(root/'rom-regeneration.log').write_text('\n'.join(rows))
tree=git('ls-tree','-rz','HEAD')
n=0;links=[]
for row in tree.split(b'\0'):
    if not row:continue
    meta,rawpath=row.split(b'\t',1);mode,kind,oid=meta.decode().split();path=rawpath.decode()
    if mode=='160000':links.append((path,oid));continue
    f=a.repo/path;data=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==oid,path
    if mode!='120000':assert bool(f.stat().st_mode&0o111)==(mode=='100755'),path
    n+=1
subprocess.run(['git','-C',str(a.repo),'diff','--cached','--exit-code','HEAD'],check=True)
subprocess.run(['git','-C',str(a.repo),'diff','--exit-code','HEAD'],check=True)
assert not git('status','--porcelain').strip()
(root/'tracked-index.txt').write_bytes(git('ls-files','--stage'))
(root/'integrity.log').write_text(f'HEAD 409c3075a6c5525d283de5a93584ad87a4528137\nTREE b552de2244475b15bfc430b683f8a4fe9c6a7db3\n{n} tracked blobs and executable modes match HEAD\nIndex matches HEAD; clean working tree\nDonor gitlinks: {links}\nCompanion donor gitlink verified separately by check_evidence.py\n')
print('Docs rc 0; four ROMs byte-identical;',n,'tracked blobs/modes/index verified; gitlinks',links)
