#!/usr/bin/env python3
"""Run unchanged published probes, then grade their functions for round 3."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys

C=Path('/candidate'); W=Path('/work'); P=Path('/packet/prior-probes')

def module(name):
    s=importlib.util.spec_from_file_location(name,P/(name+'.py'))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

mode=sys.argv[1]
if mode=='round1':
    repo=W/'clone';subprocess.run(['git','clone','-q','--shared',str(C),str(repo)],check=True)
    print('UNCHANGED historical probe',flush=True)
    subprocess.run([sys.executable,str(P/'probe_scope.py'),str(repo),str(W/'legacy')],check=True)
    m=module('probe_scope');m.PARENT=m.HEAD;m.HEAD='97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab'
    sys.argv=['probe_scope.py',str(repo),str(W/'current')]
    out=io.StringIO()
    with contextlib.redirect_stdout(out): assert m.main()==0
    print('UNCHANGED functions with explicit current revision',flush=True);print(out.getvalue())
    rows=[json.loads(x) for x in out.getvalue().splitlines() if json.loads(x).get('bodies')=='head']
    assert len(rows)==9
    for row in rows:
        assert row['rc']==0,row
        if row['case'].startswith('B16'): assert row['rtl']=='false' and row['n']==2,row
        else: assert row['rtl']=='true' and 'hdl/x.sv' in row['files'],row
    print('PASS: nine current-head outcomes; unchanged historical script is observational')
elif mode=='round2':
    print('UNCHANGED round-2 probe retains its historical divergence oracle',flush=True)
    result=subprocess.run([sys.executable,str(P/'probe_r632_2.py'),str(C),str(W/'unchanged')],capture_output=True,text=True)
    print(result.stdout);print(result.stderr)
    misses=[l for l in result.stdout.splitlines() if l.startswith('MISS')]
    assert result.returncode==1 and len(misses)==3 and all('identical-on-dev' in l for l in misses),misses
    # Do not edit the published file or its historical expected result.
    # Grade the unchanged builders and executors against the round-3 requirement.
    m=module('probe_r632_2');root=W/'current';root.mkdir();repo=m.Repo(root,C);cases=m.build(repo);count=0
    for wf,job,sid in m.SCOPES:
        body=m.step_body(C,wf,job,sid)
        for label,(recorded,live,head,want) in cases.items():
            h=m.hosted(repo,body,recorded,live,head);r=m.replay(repo,body,recorded,live,head)
            verdict='false' if label=='identical-on-dev' else want
            assert h==r and h[0]==verdict,(wf,label,h,r,verdict)
            print('CURRENT',wf,label,h);count+=1
    print(f'PASS: {count} current-head hosted/replay pairs; three historical-oracle mismatches are resolved divergence')
elif mode=='rename':
    root=W/'rename';root.mkdir()
    print('UNCHANGED formula demonstration (hardcoded old replay formula)',flush=True)
    subprocess.run(['bash',str(P/'rename_divergence_r632_2.sh'),str(C),str(root)],check=True)
    m=module('probe_r632_2')
    head=m.git(root,'rev-parse','HEAD');recorded=m.git(root,'rev-parse',head+'^')
    live=m.git(root,'rev-parse','main') if m.git(root,'branch','--list','main') else m.git(root,'rev-parse','master')
    # Preserve the original fixture and use a thin instance for its executors.
    repo=object.__new__(m.Repo);repo.root=root
    for wf,job,sid in m.SCOPES:
        body=m.step_body(C,wf,job,sid)
        h=m.hosted(repo,body,recorded,live,head);r=m.replay(repo,body,recorded,live,head)
        assert h==r==('true',['docs/reference/REGISTER_MAP.md']),(wf,h,r)
        print('CURRENT',wf,'hosted = replay =',h)
    print('PASS: current shipping selectors resolve all three rename divergences')
else:
    raise SystemExit('unknown mode')
