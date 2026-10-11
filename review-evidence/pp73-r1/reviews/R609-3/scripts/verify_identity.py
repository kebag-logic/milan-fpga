#!/usr/bin/env python3
"""Check every tracked byte, mode and index entry, gitlinks, and generated ROM identity."""
import argparse,hashlib,json,os,stat,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args()
p=a.packet.resolve();root=a.root.resolve();head='15981b511370a8cfb58ec023fae27f8a800c058c';base='2cbed0a987c1e68402658d69459ab7e5aa571adc'
def git(*args):return subprocess.check_output(['git','-C',str(root),*args])
def sha(b):return hashlib.sha256(b).hexdigest()
rows=[];links=[];errors=[]
entries=git('ls-tree','-rz',head).split(b'\0')
for ent in entries:
 if not ent:continue
 meta,name=ent.split(b'\t',1);mode,kind,oid=meta.decode().split();name=name.decode();f=root/name
 if kind=='commit':links.append(dict(path=name,oid=oid));continue
 data=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 actual_mode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode&0o111 else '100644')
 good=actual==oid and actual_mode==mode
 if not good:errors.append(name)
 rows.append(dict(path=name,blob=oid,sha256=sha(data),mode=mode,match=good))
index=git('ls-files','--stage','-z').split(b'\0');want=[]
for ent in entries:
 if ent:
  meta,name=ent.split(b'\t',1);mode,kind,oid=meta.split();want.append(mode+b' '+oid+b' 0\t'+name)
index_ok=sorted(x for x in index if x)==sorted(want)
production=git('ls-tree','-r','--name-only',base,'hdl').decode().splitlines();sv=[x for x in production if x.endswith('.sv')]
prod=[dict(path=x,base_blob=git('rev-parse',base+':'+x).decode().strip(),head_blob=git('rev-parse',head+':'+x).decode().strip()) for x in sv]
roms=[]
for gen,name in [('hdl/aecp/ucode/gen_ucode.py','ucode.hex'),('hdl/acmp/rom/gen_ltn_rom.py','ltn_rom.hex')]:
 row=dict(name=name)
 for label in ['base','head']:
  out=p/'scratch'/('identity-'+label+'-'+name)
  r=subprocess.run(['python3','-B',str(p/'scratch'/label/gen),'-o',str(out)],capture_output=True,text=True,check=True)
  row[label]=dict(bytes=out.stat().st_size,sha256=sha(out.read_bytes()))
 row['identical']=row['base']==row['head'];roms.append(row)
version=subprocess.check_output([os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'),'--version'],text=True).strip()
report=dict(head=git('rev-parse','HEAD').decode().strip(),tree=git('rev-parse','HEAD^{tree}').decode().strip(),detached=subprocess.run(['git','-C',str(root),'symbolic-ref','-q','HEAD'],capture_output=True).returncode==1,tracked_blobs=len(rows),tracked_errors=errors,index_matches=index_ok,gitlinks=links,status=git('status','--porcelain=v1','--untracked-files=all').decode(),production_sv_count=len(prod),production_identical=all(x['base_blob']==x['head_blob'] for x in prod),roms=roms,compiler_version=version)
for name,obj in [('tracked-blobs.json',rows),('production-identity.json',prod),('integrity.json',report)]: (p/'receipts'/name).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['head']==head and report['tree']=='e4dacda27467378e175562d5001b8dbadea9d4bd' and report['detached'] and not errors and index_ok and not report['status'] and report['production_identical'] and all(r['identical'] for r in roms)
