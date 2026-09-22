"""Verify reviewed source, workflow preservation, and pinned checkout bytes."""
from pathlib import Path
import ast
import hashlib
import json
import os
import stat
import subprocess

ROOT=Path.cwd()
OUT=Path(__file__).resolve().parent
HEAD='6af65a151663e1301f1983a6c9d22650a0b35da9'
BASE='b17580b91deb11f3441dfc5d7f9fafe539d929b8'
ENV={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'}
def git(*args,root=ROOT):
    return subprocess.check_output(['git','-C',str(root),*args],env=ENV)

assert git('rev-parse','HEAD').decode().strip()==HEAD
changed=git('diff','--name-only',BASE,HEAD).decode().splitlines()
assert changed==['docs/testing/CI_WORKFLOWS.md','scripts/ci_events.py']
workflow_blobs={}
for name in ['docs.yml','elaborate.yml','rtl-fast.yml','rtl.yml']:
    path='.github/workflows/'+name
    old=git('rev-parse',BASE+':'+path).decode().strip()
    new=git('rev-parse',HEAD+':'+path).decode().strip()
    assert old==new
    workflow_blobs[path]=new

base_tree=ast.parse(git('show',BASE+':scripts/ci_events.py'))
head_tree=ast.parse((ROOT/'scripts/ci_events.py').read_text())
def functions(tree):
    result={}
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            if isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
                node.body.pop(0)
            result[node.name]=ast.dump(node,include_attributes=False)
    return result
old,new=functions(base_tree),functions(head_tree)
modified=[name for name in old if old[name]!=new.get(name)]
added=sorted(set(new)-set(old))
assert sorted(modified)==sorted(['check_carrier_steps','_mutations','_selftest_whitespace','selftest'])
assert added==sorted(['check_carrier_script','_carrier_run_steps','_carrier_script_edits','_carrier_script_arms','_selftest_carrier_script_pins'])
data=dict(head=HEAD,base=BASE,changed=changed,workflow_blobs_unchanged=workflow_blobs,
          existing_functions_with_executable_changes=modified,new_functions=added,
          unchanged_existing_function_count=len(old)-len(modified))
(OUT/'source-preservation.json').write_text(json.dumps(data,indent=2)+'\n')

def verify_tree(root,revision):
    count=0;links={};problems=[]
    for record in git('ls-tree','-r','-z',revision,root=root).split(b'\0'):
        if not record: continue
        meta,raw_path=record.split(b'\t',1)
        mode,kind,expected=meta.decode().split()
        rel=os.fsdecode(raw_path);p=root/rel
        if mode=='160000':
            links[rel]=expected;continue
        try:
            s=p.lstat()
            if mode=='120000':
                assert stat.S_ISLNK(s.st_mode)
                body=os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(s.st_mode)
                assert bool(s.st_mode & stat.S_IXUSR)==(mode=='100755')
                body=p.read_bytes()
            observed=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
            assert observed==expected
        except (OSError,AssertionError):
            problems.append(rel)
        count+=1
    assert not problems,(str(root),problems)
    return count,links

parent_count,gitlinks=verify_tree(ROOT,HEAD)
modules={}
for rel in ['gptp-processor','protocol-processor','third_party/verilog-axis']:
    expected=gitlinks[rel]
    observed=git('rev-parse','HEAD',root=ROOT/rel).decode().strip()
    assert observed==expected
    count,_=verify_tree(ROOT/rel,expected)
    status=git('status','--porcelain=v1','--untracked-files=all',root=ROOT/rel).decode()
    assert not status,(rel,status)
    modules[rel]=dict(pin=expected,tracked_blobs_verified=count,status=status)
status=git('status','--porcelain=v1','--untracked-files=all','--ignore-submodules=none').decode()
assert not status,status
result=dict(head=HEAD,head_tree=git('rev-parse','HEAD^{tree}').decode().strip(),
            parent_tracked_blobs_verified=parent_count,parent_status=status,submodules=modules,
            external='Uninitialized as at entry; outside the required local gate population',
            reviewer_product_edits=False,reviewer_builds=0)
(OUT/'final-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(data,indent=2))
print(json.dumps(result,indent=2))
print('R219 final tracked/submodule integrity: PASS')
