#!/usr/bin/env python3
"""Independent histories execute the three shipping selector bodies."""
import os
from pathlib import Path
import shutil
import subprocess
import json
import yaml

C = Path('/candidate')
W = Path('/work')
E = dict(os.environ, GIT_AUTHOR_NAME='Review fixture', GIT_AUTHOR_EMAIL='review@example.invalid',
         GIT_COMMITTER_NAME='Review fixture', GIT_COMMITTER_EMAIL='review@example.invalid',
         GIT_AUTHOR_DATE='2000-01-01T00:00:00Z', GIT_COMMITTER_DATE='2000-01-01T00:00:00Z')

def git(root, *args):
    return subprocess.check_output(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false',
                                    '-c','gc.auto=0','-C',str(root),*args],env=E,stderr=subprocess.PIPE,text=True).strip()

def write(root, path, content):
    target=root/path; target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)

def commit(root, parent, changes):
    if parent: git(root,'checkout','-q','--detach',parent)
    for path,content in changes.items():
        if content is None: (root/path).unlink()
        else: write(root,path,content)
    git(root,'add',*changes) if parent else git(root,'add','-A')
    git(root,'commit','-qm','Fixture revision')
    return git(root,'rev-parse','HEAD')

def merge(root, live, head):
    git(root,'checkout','-q','--detach',live)
    git(root,'merge','--no-ff','--no-edit',head)
    tree=git(root,'rev-parse','HEAD^{tree}')
    return git(root,'commit-tree',tree,'-p',live,'-p',head,'-m','Hosted composition')

selectors={}
for workflow,job,step in [('rtl.yml','full-ci-gate','gate'),('rtl-fast.yml','changes','scope'),('elaborate.yml','elaborate','scope')]:
    doc=yaml.safe_load((C/'.github/workflows'/workflow).read_text())
    checkout=next(s for s in doc['jobs'][job]['steps'] if s.get('uses','').startswith('actions/checkout'))
    assert checkout['with']['fetch-depth']==0
    body=next(s['run'] for s in doc['jobs'][job]['steps'] if s.get('id')==step)
    assert body.count('python3 scripts/ci_scope.py --selftest')==1
    selectors[workflow]=body.replace('python3 scripts/ci_scope.py --selftest',':')

def run(root, body, recorded, live, head, replay, event='pull_request', before=None, checked=None):
    git(root,'reset','--hard')
    git(root,'update-ref','refs/remotes/origin/dev',live)
    target=checked or (head if replay else merge(root,live,head))
    git(root,'checkout','-q','--detach',target)
    # The candidate selector is the code under test, even with historical data.
    shutil.copyfile(C/'scripts/ci_scope.py',root/'scripts/ci_scope.py')
    out=W/'out';out.mkdir(exist_ok=True)
    for p in out.iterdir(): p.unlink()
    env=dict(E,ACT='true' if replay else 'false',EVENT_NAME=event,PR_DRAFT='false',
             PR_BASE_SHA=recorded,PR_BASE_REF='dev',PR_HEAD_SHA=head,GITHUB_SHA=target,
             PUSH_BEFORE_SHA=before or recorded,GITHUB_OUTPUT=str(out/'output'),RUNNER_TEMP=str(out))
    result=subprocess.run(['bash','-euo','pipefail','-c',body],cwd=root,env=env,text=True,capture_output=True)
    if result.returncode: return {'rc':result.returncode,'error':result.stderr.strip()}
    values=dict(x.split('=',1) for x in (out/'output').read_text().splitlines())
    paths=next(out.glob('changed*'),None)
    return {'rc':0,'rtl':values['rtl'],'paths':paths.read_text().splitlines() if paths else None,'run_full':values.get('run_full')}

root=W/'history';root.mkdir();git(root,'init','-q')
write(root,'scripts/ci_scope.py',(C/'scripts/ci_scope.py').read_text())
base=commit(root,None,{'hdl/anchor.sv':'// retained RTL\n','hdl/filter.sv':'// old\n','docs/notes.md':''.join(f'line {i}\n' for i in range(80)),'.gitmodules':'[submodule "data"]\n path = docs/data.md\n url = https://example.invalid/data\n'})
git(root,'update-index','--add','--cacheinfo',f'160000,{base},docs/data.md');git(root,'commit','-qm','Pointer baseline');base=git(root,'rev-parse','HEAD')
live=commit(root,base,{'hdl/base.sv':'// live only\n'})
docs=commit(root,base,{'docs/pr.md':'PR text\n'})
rtl=commit(root,base,{'hdl/filter.sv':'// changed by PR\n','docs/pr.md':'PR text\n'})
git(root,'checkout','-q','--detach',base);git(root,'update-index','--cacheinfo',f'160000,{live},docs/data.md');git(root,'commit','-qm','Pointer move');pointer=git(root,'rev-parse','HEAD')
dev=commit(root,base,{'hdl/filter.sv':'// newer dev\n'})
merged=merge(root,dev,docs)
rev=commit(root,merged,{'hdl/anchor.sv':'// retained RTL\n','hdl/filter.sv':'// old\n','docs/pr.md':'After restore\n'})
extra=commit(root,dev,{'hdl/extra.sv':'// extra\n'})
git(root,'checkout','-q','--detach',live);(root/'docs/reference').mkdir(exist_ok=True);git(root,'mv','docs/notes.md','docs/reference/REGISTER_MAP.md');git(root,'commit','-qm','Move to gate input');renamed=git(root,'rev-parse','HEAD')
edit=commit(root,base,{'docs/notes.md':''.join(f'line {i}\n' if i!=40 else 'changed line\n' for i in range(80))})
same_live=commit(root,live,{'hdl/shared.sv':'// shared\n'});same_head=commit(root,docs,{'hdl/shared.sv':'// shared\n'})
moved=commit(root,base,{'hdl/filter.sv':None,'docs/filter.md':'// old\n'})
cases=[('stale docs',live,docs,['docs/pr.md'],'false'),('stale RTL',live,rtl,['docs/pr.md','hdl/filter.sv'],'true'),('pointer',live,pointer,['docs/data.md'],'true'),('empty',live,base,[],'true'),('REV',dev,rev,['docs/pr.md','hdl/filter.sv'],'true'),('REV+E',extra,rev,['docs/pr.md','hdl/filter.sv'],'true'),('base rename',renamed,edit,['docs/reference/REGISTER_MAP.md'],'true'),('identical edits',same_live,same_head,['docs/pr.md'],'false'),('RTL moved to docs',live,moved,['docs/filter.md','hdl/filter.sv'],'true')]
count=0
for label,l,h,expected,verdict in cases:
    for name,body in selectors.items():
        for replay in (False,True):
            result=run(root,body,base,l,h,replay)
            assert result['rc']==0 and result['paths']==expected and result['rtl']==verdict,(label,name,replay,result)
            print(json.dumps({'case':label,'workflow':name,'mode':'replay' if replay else 'hosted',**result}));count+=1
# Preserve push comparisons and non-PR dispatch policy.
for event in ('push','workflow_dispatch'):
    for name,body in selectors.items():
        result=run(root,body,base,live,docs,False,event=event,before=base,checked=docs)
        expected='false' if name=='rtl-fast.yml' else 'true'
        assert result['rc']==0 and result['rtl']==expected,(event,name,result)
        print(json.dumps({'case':event,'workflow':name,**result}));count+=1
for before in ('','0'*40,'f'*40):
    result=run(root,selectors['rtl-fast.yml'],base,live,docs,False,event='push',before=before or '0'*40,checked=docs)
    assert result['rtl']=='true',result
    print(json.dumps({'case':'unknown push before','before':before,**result}));count+=1
# Historical issue #734 reproduction, using a disposable clone and real commits.
b16=W/'b16';subprocess.run(['git','clone','-q','--shared','--no-checkout',str(C),str(b16)],check=True,env=E)
b='49da9fd974e8805d56c90e29dcfcb67994c2c430';h='f1b2489f5b1c929e81eeae79a469b2b27c47e340'
old=git(b16,'diff','--name-only',b,h).splitlines();old_no=git(b16,'diff','--no-renames','--name-only',b,h).splitlines();own=git(b16,'diff','--no-renames','--name-only',b+'...'+h).splitlines()
assert len(old)==64 and len(old_no)==65 and len(own)==2,(len(old),len(old_no),own)
print(json.dumps({'case':'historical B16 counts','two_dot_default':len(old),'two_dot_no_renames':len(old_no),'merge_base':own}))
for l in (b,'e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c','a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0'):
    for name,body in selectors.items():
        for replay in (False,True):
            result=run(b16,body,b,l,h,replay)
            expected_paths=[] if l.startswith('a0f39ad4') else own
            expected_rtl='true' if not expected_paths else 'false'
            assert result['rc']==0 and result['rtl']==expected_rtl and result['paths']==expected_paths,(name,replay,l,result)
            print(json.dumps({'case':'historical B16','live_base':l,'workflow':name,'mode':'replay' if replay else 'hosted',**result}));count+=1
print(f'PASS: {count} independent selector executions; historical B16 counts reproduced')
