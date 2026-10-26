#!/usr/bin/env python3
"""Audit delta invariants and exact tracked bytes without trusting status flags.
Usage: source_audit.py CHECKOUT OUTPUT_JSON
"""
import hashlib
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tokenize

root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(sys.argv[2])
head='d33a5adc60cd93b34be41dfacf94daaec9d059c2'
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(*args,cwd=root):
    return subprocess.check_output(['git',*args],cwd=cwd,env=env)
def entries(rev,cwd):
    result=[]
    for row in git('ls-tree','-rz',rev,cwd=cwd).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1); mode,kind,oid=meta.decode().split()
        result.append((mode,kind,oid,os.fsdecode(path)))
    return result
def raw_oid(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def audit(cwd,rev):
    errors=[]; count=0; links=[]
    for mode,kind,oid,name in entries(rev,cwd):
        p=cwd/name
        if kind=='commit':
            links.append({'path':name,'gitlink':oid});continue
        count+=1
        try:
            if mode=='120000':
                assert p.is_symlink(),'expected symlink'
                data=os.fsencode(os.readlink(p))
            else:
                assert p.is_file() and not p.is_symlink(),'expected ordinary file'
                data=p.read_bytes()
                assert bool(p.stat().st_mode&0o111)==(mode=='100755'),'executable mode differs'
            assert raw_oid(data)==oid,'blob differs'
        except (AssertionError,OSError) as e:
            errors.append({'path':name,'error':str(e)})
    actual=git('rev-parse','HEAD',cwd=cwd).decode().strip()
    tree=git('rev-parse',rev+'^{tree}',cwd=cwd).decode().strip()
    index=git('write-tree',cwd=cwd).decode().strip()
    return {'expected_head':rev,'actual_head':actual,'tree':tree,'index_tree':index,
            'tracked_blobs':count,'blob_mode_errors':errors,'gitlinks':links,
            'matches':actual==rev and index==tree and not errors}

parent=audit(root,head)
submodules=[]
for item in parent['gitlinks']:
    if item['path']=='external':
        submodules.append({**item,'optional_uninitialized':not (root/item['path']/'.git').exists()})
    else:
        submodules.append({'path':item['path'],**audit(root/item['path'],item['gitlink'])})
def content(rev,path):return git('show',rev+':'+path).decode()
def no_comments(text):
    # Strings stay intact; only comments and whitespace are irrelevant here.
    pattern=r'"(?:\\.|[^"\\])*"|/\*[\s\S]*?\*/|//[^\n]*'
    text=re.sub(pattern,lambda m:m[0] if m[0].startswith('"') else '',text)
    return re.sub(r'\s+','',text)
def py_tokens(text):
    return [(t.type,t.string) for t in tokenize.generate_tokens(io.StringIO(text).readline)
            if t.type not in (tokenize.COMMENT,tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT)]
paths=['hdl/milan/mailbox/KL_mbx.sv','hdl/milan/mailbox/KL_mbx_evt.sv',
       'hdl/milan/mailbox/KL_mbx_pkg.sv','tb/verilator/mbx/suite_face.hpp',
       'tb/verilator/mbx/suite.hpp','sw/firmware/ctrl/mbx/mbx_contract.h']
comments={p:no_comments(content('44d95625',p))==no_comments(content(head,p)) for p in paths}
unchanged={p:not git('diff','--name-only','e76a755a',head,'--',p).strip() for p in
           ['hdl/milan/milan_datapath.sv','.github','sw/mailbox/ci_gate_workflows.py']}
coverage=git('diff','--name-only','44d95625',head,'--','sw/firmware/gtest').decode().splitlines()
post_receipts=git('diff','--name-only','989c9f53',head).decode().splitlines()
result={'parent':parent,'submodules':submodules,'all_initialized_match':parent['matches'] and
        all(s.get('matches',s.get('optional_uninitialized',False)) for s in submodules),
        'comment_only_or_unchanged':comments,'protected_paths_unchanged_from_base':unchanged,
        'coverage_framework_delta':coverage,'changed_since_executed_firmware_head':post_receipts}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('parent','submodules')},indent=2))
assert result['all_initialized_match']
assert all(comments.values())
