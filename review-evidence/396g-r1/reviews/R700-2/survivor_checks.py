#!/usr/bin/env python3
"""Retain named failures for the three formerly surviving public mutations."""
import concurrent.futures, importlib.util, json, os, pathlib, re, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent;scratch=out/'scratch'
source=(root/'tb/tools/torture_campaign.py').read_text()
script=out/'prior-reviewer-mutants.py'
spec=importlib.util.spec_from_file_location('prior_mutants',script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def run(mutant):
 name,old,new=mutant;ident=name.split()[0];assert source.count(old)==1
 p=scratch/(ident+'.py');p.write_text(source.replace(old,new))
 r=subprocess.run([sys.executable,'-B',str(p),'--self-test'],cwd=root,capture_output=True,text=True,timeout=120,
                  env=dict(os.environ,TMPDIR=str(scratch)))
 (out/(ident+'.log')).write_text(r.stdout+r.stderr);(out/(ident+'.rc')).write_text(str(r.returncode)+'\n')
 failures=sorted(set(re.findall(r'^FAIL: (\w+)',r.stderr,re.M)))
 assert r.returncode==1 and failures
 return dict(mutant=name,rc=r.returncode,named_failures=failures)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 rows=list(pool.map(run,[x for x in m.MUTANTS if x[0].split()[0] in ('G07','G12','R03')]))
(out/'survivor-checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
