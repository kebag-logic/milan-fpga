#!/usr/bin/env python3
"""Isolated in-memory production mutations; no tracked file changes."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
out=pathlib.Path(__file__).resolve().parent; root=pathlib.Path(sys.argv[1]).resolve()
mutations=[
 ('i3-no-shared-budget','ci_runtime_evidence','API(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"], RETRY_BUDGET_SECONDS)','API(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"])','ci_runtime_evidence_selftest'),
 ('i1-conditional-prep-accepted','ci_suite_workflows','if body.strip() == preparation and "if" not in step and not step.get("continue-on-error"):','if body.strip() == preparation:','ci_gate_workflows_selftest'),
 ('watcher-client-observer','ci_fail_fast','if isinstance(exc, OSError) and not transient(exc):','if False:','ci_fail_fast_selftest'),
 ('collector-client-observer','ci_runtime_evidence','            if not transient(exc):\n                raise\n','','ci_runtime_evidence_selftest'),
 ('watcher-403-genuine','ci_fail_fast','error.code in (403, 429)','error.code in (429,)','ci_fail_fast_selftest'),
 ('collector-403-genuine','ci_fail_fast','error.code in (403, 429)','error.code in (429,)','ci_runtime_evidence_selftest'),
 ('builder-owner-refusal-removed','ci_builder_legs','            if gates:\n                raise ValueError(f"{flag} on the union','            if False:\n                raise ValueError(f"{flag} on the union','ci_gate_workflows_selftest'),
 ('builder-ledger-unjudged','ci_builder_legs','    if elaboration_verdict(ledger):','    if False:','ci_gate_workflows_selftest'),
 ('builder-receipt-inventory-trusted','ci_builder_legs','    if driver["inventory"] != names:','    if False:','ci_gate_workflows_selftest'),
]
child='''import pathlib,sys,types,runpy
root=pathlib.Path(sys.argv[1]); module,old,new,test=sys.argv[2:]
sys.path.insert(0,str(root/'scripts'))
path=root/'scripts'/(module+'.py'); source=path.read_text()
assert source.count(old)==1,(module,source.count(old))
m=types.ModuleType(module);m.__file__=str(path);sys.modules[module]=m
exec(compile(source.replace(old,new),str(path),'exec'),m.__dict__)
runpy.run_path(str(root/'scripts'/(test+'.py')),run_name='__main__')
'''
def run(m):
 name,module,old,new,test=m;start=time.monotonic()
 with (out/('mutation-'+name+'.log')).open('w') as f:
  rc=subprocess.run([sys.executable,'-c',child,str(root),module,old,new,test],cwd=root,env=dict(os.environ,TMPDIR=str(out/'scratch'),PYTHONDONTWRITEBYTECODE='1'),stdout=f,stderr=subprocess.STDOUT,timeout=120).returncode
 (out/('mutation-'+name+'.rc')).write_text(str(rc)+'\n')
 result={'mutation':name,'module':module,'old':old,'new':new,'selftest':test,'rc':rc,'seconds':round(time.monotonic()-start,3)}
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,mutations))
(out/'mutation-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['rc']==1 for r in results),results
