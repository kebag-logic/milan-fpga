#!/usr/bin/env python3
"""Verify raw tracked file bytes, modes, the complete index and submodule gitlinks."""
import argparse,hashlib,json,os,pathlib,stat,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args();r=a.repo.resolve()
def git(*x):return subprocess.check_output(['git',*x],cwd=r)
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();errors=[];files=[];submodules=[]
for rec in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not rec:continue
 meta,name=rec.split(b'\t',1);mode,kind,oid=meta.decode().split();rel=os.fsdecode(name);f=r/rel
 if mode=='160000':
  actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=f,text=True).strip();submodules.append({'path':rel,'expected':oid,'actual':actual});assert actual==oid;continue
 data=os.readlink(f).encode() if mode=='120000' else f.read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();actual_mode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode&stat.S_IXUSR else '100644')
 files.append({'path':rel,'mode':mode,'blob':oid,'matches':actual==oid and mode==actual_mode})
 if not files[-1]['matches']:errors.append(rel)
index_tree=git('write-tree').decode().strip();status=git('status','--porcelain=v1').decode();out={'head':head,'tree':tree,'index_tree':index_tree,'tracked_count':len(files),'raw_byte_mode_errors':errors,'status':status,'submodule_gitlinks':submodules,'files':files}
a.output.write_text(json.dumps(out,indent=2)+'\n')
assert head=='cd9825c947cf67b735d26cc1c42541ccd9d7f637';assert tree==index_tree=='7234360164b13afa707faa552ebf72d4f10a44e7';assert not errors and not status
print('Exact head, tree, index, all',len(files),'raw blobs/modes verified; submodule gitlinks',len(submodules))
