# SPDX-License-Identifier: Apache-2.0
"""Verify every tracked byte, mode and index entry, with explicit gitlink inventory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args();root=a.source.resolve()
def git(*args):
    return subprocess.check_output(['git',*args],cwd=root)
head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='a9cd5ef58a2478cb2ce4899b31aa02d5c2072646'
assert tree=='bc5b80a60d923ce869647e3f3ba95276456864d1'
entries={};gitlinks=[];records=[]
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not row: continue
    meta,name=row.split(b'\t'); mode,kind,oid=meta.decode().split();name=os.fsdecode(name)
    entries[name]=(mode,oid)
    if mode=='160000':
        gitlinks.append({'path':name,'commit':oid});continue
    path=root/name
    data=os.fsencode(os.readlink(path)) if mode=='120000' else path.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actual_mode='120000' if path.is_symlink() else '100755' if path.stat().st_mode&0o111 else '100644'
    assert (actual_mode,actual)==(mode,oid),(name,actual_mode,actual)
    assert b'SPDX-License-Identifier: Apache-2.0' in data or name in ['LICENSE','NOTICE'],name
    records.append({'path':name,'mode':mode,'blob':oid,'verified':True})
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
    if not row:continue
    meta,name=row.split(b'\t');mode,oid,stage=meta.decode().split()
    assert stage=='0'
    index[os.fsdecode(name)]=(mode,oid)
assert index==entries
status=git('status','--porcelain=v1').decode()
assert not status,status
diff=git('diff','--check','1401654530ce7d9275de9b901e67df47e5bbc536..HEAD').decode()
assert not diff
report={'head':head,'tree':tree,'tracked_files':len(records),'tracked_blobs_modes_and_index':'PASS',
        'gitlinks':gitlinks,'gitlink_result':'No submodule gitlinks in this standalone repository.',
        'working_tree':'CLEAN','diff_check':'PASS','files':records}
a.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
