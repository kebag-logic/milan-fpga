#!/usr/bin/env python3
"""Run independent lightweight gates concurrently; retain raw stdout and exits."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(__file__).resolve().parent
scratch=out/'scratch'; scratch.mkdir(exist_ok=True)
md=sys.argv[2]
py=sys.executable
jobs=[('selftest',[py,'-B','tb/tools/torture_campaign.py','--self-test'],root),
      ('behave',[py,'-B','-m','behave','--no-capture','-f','plain'],root/'tests'),
      ('coverage',[py,'-B','tb/tools/torture_campaign.py','--coverage-by-area','--areas','soak,audio,power'],root)]
for name,script,args in [('docs_check','docs_check.py',[]),('doc_paths','check_doc_paths.py',[]),
 ('toc','gen_toc.py',['--check']),('anchors','gen_toc.py',['--verify-anchors']),
 ('em_dash','check_em_dash.py',['--base','e76a755a']),('doc_style','check_doc_style.py',[]),
 ('py_idiom','check_py_idiom.py',[]),('feature_status','check_feature_status.py',[]),
 ('feature_status_selftest','check_feature_status.py',['--self-test'])]:
 jobs.append((name,[md,'-B','scripts/'+script,*args],root))
jobs.append(('diff_check',['git','diff','--check','e76a755a','HEAD'],root))
def run(job):
 name,cmd,cwd=job; start=time.monotonic()
 with (out/(name+'.log')).open('w') as log:
  try:
   r=subprocess.run(cmd,cwd=cwd,env=dict(os.environ,TMPDIR=str(scratch)),stdout=log,stderr=subprocess.STDOUT,timeout=550)
   rc=r.returncode
  except subprocess.TimeoutExpired: rc=124
 (out/(name+'.rc')).write_text(str(rc)+'\n')
 row=dict(name=name,command=cmd,cwd='tests' if cwd.name=='tests' else '.',rc=rc,seconds=round(time.monotonic()-start,2))
 print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 rows=list(pool.map(run,jobs))
(out/'checks.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(any(r['rc'] for r in rows))
