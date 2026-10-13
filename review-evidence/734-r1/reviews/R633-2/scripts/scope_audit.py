#!/usr/bin/env python3
"""Independent YAML-extracted selector executions, using explicit path/verdict oracles."""
import json, os, pathlib, shutil, subprocess, sys, tempfile
import yaml
source, work = map(pathlib.Path, sys.argv[1:])
work.mkdir(parents=True, exist_ok=True)
steps = [('rtl.yml','full-ci-gate','gate'),('rtl-fast.yml','changes','scope'),('elaborate.yml','elaborate','scope')]
bodies = {}
for wf, job, sid in steps:
    doc=yaml.safe_load((source/'.github/workflows'/wf).read_text())
    checkout=doc['jobs'][job]['steps'][0]
    assert checkout['with']['fetch-depth']==0
    step=next(x for x in doc['jobs'][job]['steps'] if x.get('id')==sid)
    assert step['env']['PR_BASE_REF']=='${{ github.event.pull_request.base.ref }}'
    assert step['env']['PR_HEAD_SHA']=='${{ github.event.pull_request.head.sha }}'
    body=step['run']; assert body.count('python3 scripts/ci_scope.py --selftest')==1
    bodies[wf]=body.replace('python3 scripts/ci_scope.py --selftest', ':')

def git(root,*args):
    return subprocess.check_output(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-C',str(root),*args],stderr=subprocess.STDOUT,text=True).strip()

def commit(root,parent,path,text):
    git(root,'checkout','-q','--detach',parent)
    p=root/path; p.parent.mkdir(parents=True,exist_ok=True)
    if text is None: p.unlink()
    else: p.write_text(text)
    git(root,'add','--',path);git(root,'commit','-qm','Fixture change');return git(root,'rev-parse','HEAD')

def merge(root,base,head):
    git(root,'checkout','-q','--detach',base);git(root,'merge','--no-ff','--no-edit',head)
    m=git(root,'rev-parse','HEAD')
    if m==base:
        m=git(root,'commit-tree',base+'^{tree}','-p',base,'-p',head,'-m','Synthetic merge')
    assert git(root,'rev-parse',m+'^1')==base
    return m

count=0

def run(root,body,recorded,head,sha,extra=None):
    global count
    count+=1
    with tempfile.TemporaryDirectory(dir=work) as raw:
        env=dict(os.environ,EVENT_NAME='pull_request',PR_DRAFT='false',ACT='false',PR_BASE_SHA=recorded,PR_BASE_REF='dev',PR_HEAD_SHA=head,GITHUB_SHA=sha,PUSH_BEFORE_SHA=recorded,RUNNER_TEMP=raw,GITHUB_OUTPUT=raw+'/out')
        env.update(extra or {})
        result=subprocess.run(['bash','-euo','pipefail','-c',body],cwd=root,env=env,text=True,capture_output=True)
        changes=list(pathlib.Path(raw).glob('changed*')); out=pathlib.Path(raw)/'out'
        return {'rc':result.returncode,'files':changes[0].read_text().splitlines() if changes else None,'outputs':dict(l.split('=',1) for l in out.read_text().splitlines()) if out.exists() else {},'stderr':result.stderr.strip()}

def check(label,result,files=None,rtl=None,fail=False):
    if fail: assert result['rc']!=0 and result['outputs'].get('rtl')!='false',(label,result)
    else:
        assert result['rc']==0,(label,result)
        if files is not None: assert result['files']==files,(label,result,files)
        if rtl is not None: assert result['outputs']['rtl']==rtl,(label,result,rtl)
    print(json.dumps({'case':label,**result}),flush=True)

root=work/'repo';root.mkdir();git(root,'init','-q')
(root/'scripts').mkdir();shutil.copyfile(source/'scripts/ci_scope.py',root/'scripts/ci_scope.py')
for name,text in {'hdl/x.sv':'original\n','hdl/stable.sv':'stable\n','docs/a.md':'initial\n','.gitmodules':'[submodule "pointer"]\n path = docs/pointer.md\n url = https://example.invalid/pointer\n'}.items():
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
git(root,'add','.');git(root,'commit','-qm','Root'); initial=git(root,'rev-parse','HEAD')
git(root,'update-index','--add','--cacheinfo',f'160000,{initial},docs/pointer.md');git(root,'commit','-qm','Pointer'); r=git(root,'rev-parse','HEAD')
d=commit(root,r,'hdl/x.sv','new dev RTL\n'); e=commit(root,d,'hdl/unrelated.sv','later dev RTL\n')
docs=commit(root,r,'docs/a.md','docs change\n');rtl=commit(root,r,'hdl/pr.sv','own RTL\n');mixed=commit(root,rtl,'docs/a.md','mixed\n');deleted=commit(root,r,'hdl/stable.sv',None)
git(root,'checkout','-q','--detach',r);git(root,'mv','hdl/stable.sv','docs/renamed.md');git(root,'commit','-qm','Rename');renamed=git(root,'rev-parse','HEAD')
gated=commit(root,r,'docs/reference/REGISTER_MAP.md','gate input\n')
git(root,'checkout','-q','--detach',r);git(root,'update-index','--cacheinfo',f'160000,{d},docs/pointer.md');git(root,'commit','-qm','Move pointer');pointer=git(root,'rev-parse','HEAD')
git(root,'checkout','-q','--detach',docs);git(root,'merge','--no-ff','--no-edit',d);lane=git(root,'rev-parse','HEAD');rev=commit(root,lane,'hdl/x.sv','original\n');rev=commit(root,rev,'docs/a.md','final docs\n')
cases=[('docs',d,docs,['docs/a.md'],'false'),('RTL',d,rtl,['hdl/pr.sv'],'true'),('mixed',d,mixed,['docs/a.md','hdl/pr.sv'],'true'),('delete',d,deleted,['hdl/stable.sv'],'true'),('rename-into-docs',d,renamed,['docs/renamed.md','hdl/stable.sv'],'true'),('gate-read-doc',d,gated,['docs/reference/REGISTER_MAP.md'],'true'),('pointer',d,pointer,['docs/pointer.md'],'true'),('empty',d,r,[],'true'),('REV',d,rev,['docs/a.md','hdl/x.sv'],'true'),('REV+E',e,rev,['docs/a.md','hdl/x.sv'],'true')]
for label,base,head,files,answer in cases:
    m=merge(root,base,head)
    assert git(root,'diff','--no-renames','--name-only',base,m).splitlines()==files
    git(root,'update-ref','refs/remotes/origin/dev',base)
    for wf,body in bodies.items():
        check(label+'/'+wf+'/hosted',run(root,body,r,head,m),files,answer)
        check(label+'/'+wf+'/replay',run(root,body,r,head,head,{'ACT':'true'}),files,answer)
        if label=='REV+E':
            mutant=body.replace('"$GITHUB_SHA^1" "$GITHUB_SHA"','"$PR_BASE_SHA...$PR_HEAD_SHA"')
            broken=run(root,mutant,r,head,m);assert broken['outputs']['rtl']=='false'
            print(json.dumps({'case':label+'/'+wf+'/frozen-base-mutant-killed',**broken}))
        if label=='RTL' and wf=='rtl.yml':
            result=run(root,body,r,head,m,{'PR_DRAFT':'true'});check('draft',result,files,'true');assert result['outputs']['run_full']=='false'

left=commit(root,r,'docs/left.md','left\n');right=commit(root,r,'docs/right.md','right\n');m1=merge(root,left,right);m2=merge(root,right,left)
assert len(git(root,'merge-base','--all',m1,m2).splitlines())==2
orphan=git(root,'commit-tree',r+'^{tree}','-m','Unrelated')
for wf,body in bodies.items():
    git(root,'update-ref','refs/remotes/origin/dev',m1)
    check(wf+'/ambiguous',run(root,body,r,m2,m2,{'ACT':'true'}),fail=True)
    check(wf+'/unrelated',run(root,body,r,orphan,orphan,{'ACT':'true'}),fail=True)
    check(wf+'/missing-base',run(root,body,r,docs,docs,{'ACT':'true','PR_BASE_REF':'absent'}),fail=True)
    check(wf+'/missing-head',run(root,body,r,'0'*40,docs,{'ACT':'true'}),fail=True)
    check(wf+'/missing-merge',run(root,body,r,docs,'0'*40),fail=True)
    if wf=='rtl-fast.yml':
        check(wf+'/push-rewind',run(root,body,d,r,r,{'EVENT_NAME':'push'}),['hdl/x.sv'],'true')
        for before in ['', '0'*40,'bad-ref']:
            check(wf+'/push-unknown',run(root,body,before,docs,docs,{'EVENT_NAME':'push'}),rtl='true')
    else:
        for event in ['push','schedule','workflow_dispatch']:
            check(wf+'/'+event,run(root,body,'',docs,docs,{'EVENT_NAME':event}),rtl='true')

# B16: use real history, then execute both forms against the landing merge's live base.
b16head=git(source,'rev-parse','f1b2489f');bm=git(source,'rev-parse','6c810c45');base=git(source,'rev-parse',bm+'^1');rec=git(source,'rev-parse','49da9fd9')
expected=['docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md','docs/findings/README.md']
counts={'two_tree_default':len(git(source,'diff','--name-only',rec,b16head).splitlines()),'two_tree_no_renames':len(git(source,'diff','--no-renames','--name-only',rec,b16head).splitlines()),'recorded_merge_base':git(source,'diff','--no-renames','--name-only',rec+'...'+b16head).splitlines(),'live_base':base}
assert counts['two_tree_default']==64 and counts['two_tree_no_renames']==65 and counts['recorded_merge_base']==expected
print(json.dumps({'case':'B16-counts',**counts}))
for wf,body in bodies.items():
    check('B16/'+wf+'/hosted',run(source,body,rec,b16head,bm),expected,'false')
# Use a private ref in the fixture repository holding the actual public objects.
historical=work/'historical';git(work,'clone','-q','--no-hardlinks',str(source),str(historical));git(historical,'update-ref','refs/remotes/origin/dev',base)
for wf,body in bodies.items(): check('B16/'+wf+'/replay',run(historical,body,rec,b16head,b16head,{'ACT':'true'}),expected,'false')
print(json.dumps({'result':'PASS','executions':count,'head':git(source,'rev-parse','HEAD')}))
