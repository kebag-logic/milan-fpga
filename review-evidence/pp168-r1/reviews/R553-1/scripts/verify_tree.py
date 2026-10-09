#!/usr/bin/env python3
"""Verify HEAD, index, tracked bytes/modes and submodule gitlinks without resetting."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2])
head='96d3b78384f34a630d6056ebd8fa5e30f6836650';tree='37ee429d6fb58f8c3f93d735131e4821f5240004'
def git(*a):return subprocess.check_output(['git','-C',str(root),*a])
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
entries=[];links=[];errors=[]
for row in git('ls-tree','-rz',head).split(b'\0'):
 if not row:continue
 meta,path=row.split(b'\t',1);mode,kind,obj=meta.decode().split();path=path.decode();f=root/path
 if mode=='160000':
  actual=subprocess.check_output(['git','-C',str(f),'rev-parse','HEAD'],text=True).strip()
  links.append(dict(path=path,required=obj,actual=actual));assert actual==obj
  continue
 b=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
 oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 actual_mode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & stat.S_IXUSR else '100644')
 if oid!=obj or actual_mode!=mode:errors.append(path)
 entries.append(dict(path=path,mode=actual_mode,blob=oid))
index=git('ls-files','--stage','-z');index_rows=[]
for row in index.split(b'\0'):
 if not row:continue
 meta,path=row.split(b'\t',1);mode,obj,stage=meta.decode().split()
 index_rows.append((path.decode(),mode,obj,stage))
expected={(x['path'],x['mode'],x['blob'],'0') for x in entries}|{(x['path'],'160000',x['required'],'0') for x in links}
assert set(index_rows)==expected
assert not errors
assert not git('status','--porcelain=v2','--untracked-files=all')
cgroup=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::')[1].lstrip('/')
mem={n:(cgroup/n).read_text().strip() for n in ['memory.max','memory.peak','memory.current','memory.events'] if (cgroup/n).exists()}
receipt=dict(head=head,tree=tree,tracked_files=len(entries),tracked_bytes_and_modes_match=True,index_matches=True,gitlinks=links,working_tree_clean=True,memory=mem,files=entries)
out.write_text(json.dumps(receipt,indent=2)+'\n');print('PASS',len(entries),'tracked blobs/modes, exact index,',len(links),'gitlinks; clean')
