#!/usr/bin/env python3
"""Prove HEAD, raw worktree blobs/modes, complete indexes and gitlinks."""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

root=Path(sys.argv[1]).resolve()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
expected='500b8f64443777685e6a54049d933476710d26f0'
tree='b1b7d3b1b9dcf7d8f3f7f299365392ebc1f17ed8'
required={'protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP'}
records=[];failures=[]
def git(where,*args):
    return subprocess.check_output(['git','--no-optional-locks','-C',str(where),*args],env=env)
def inspect(where,relative,pin):
    head=git(where,'rev-parse','HEAD').decode().strip()
    actual_tree=git(where,'rev-parse','HEAD^{tree}').decode().strip()
    assert head==pin,(relative,head,pin)
    if relative=='.':assert actual_tree==tree
    raw=git(where,'ls-tree','-rz','--full-tree',pin)
    expect_index=[];entries=[];gitlinks=[];count=0
    for line in raw.split(b'\0'):
        if not line:continue
        meta,path=line.split(b'\t',1);mode,kind,oid=meta.split()
        expect_index.append(mode+b' '+oid+b' 0\t'+path+b'\0')
        name=os.fsdecode(path);f=where/name
        if kind==b'commit':
            gitlinks.append({'path':name,'pin':oid.decode()})
            if name in required:inspect(f,name,oid.decode())
            continue
        count+=1
        try:
            st=f.lstat()
            if mode==b'120000':
                assert stat.S_ISLNK(st.st_mode)
                data=os.fsencode(os.readlink(f))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode&0o111)==(mode==b'100755')
                data=f.read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert actual==oid.decode()
            entries.append({'path':name,'mode':mode.decode(),'blob':actual})
        except (OSError,AssertionError):failures.append(f'{relative}/{name}: blob or mode mismatch')
    index=git(where,'ls-files','--stage','-z')
    expected_index=b''.join(expect_index)
    if index!=expected_index:failures.append(relative+': index does not equal HEAD tree')
    flags=git(where,'ls-files','-v','-z').split(b'\0')
    hidden=[os.fsdecode(x) for x in flags if x and x[:1]!=b'H']
    if hidden:failures.append(relative+': hidden or non-normal index flags')
    untracked=git(where,'ls-files','--others','--exclude-standard','-z').split(b'\0')
    untracked=[os.fsdecode(x) for x in untracked if x]
    if untracked:failures.append(relative+': untracked files')
    records.append({'path':relative,'head':head,'tree':actual_tree,'blobs_checked':count,
      'index_equals_tree':index==expected_index,'index_sha256':hashlib.sha256(index).hexdigest(),
      'worktree_records_sha256':hashlib.sha256(json.dumps(entries,sort_keys=True).encode()).hexdigest(),
      'hidden_flags':hidden,'untracked':untracked,'gitlinks':gitlinks})
inspect(root,'.',expected)
report={'head':expected,'tree':tree,'repositories':records,'failures':failures,
        'optional_external':'gitlink checked; checkout remains uninitialized'}
print(json.dumps(report,indent=2))
sys.exit(bool(failures))
