#!/usr/bin/env python3
"""Disposable staging isolation, scheduling and preflight propagation probes."""
import importlib, json, os, pathlib, subprocess, sys, tempfile
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parents[1]
scratch=packet/'scratch/probes'; scratch.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(scratch); tempfile.tempdir=str(scratch)
sys.path.insert(0,str(root/'scripts'))
import mutant_stage as stage
import ci_make_cases as cases
import yaml

def emit(name,**data): print(json.dumps(dict(probe=name,**data)),flush=True)
# Independent process, same parent and UID, different TMPDIR. The first lock remains held.
parent=scratch/'shared-parent'; parent.mkdir(exist_ok=True)
other=scratch/'other-temp'; other.mkdir(exist_ok=True)
child="import sys,pathlib;sys.path.insert(0,sys.argv[1]);import mutant_stage as s; p=s.mkdtemp('split-mutants-',parent=sys.argv[2]);pathlib.Path(p,'second-marker').write_text('second');print(p)"
with stage.directory('split-mutants-',parent=parent) as first:
 marker=pathlib.Path(first)/'first-marker'; marker.write_text('first')
 ran=subprocess.run([sys.executable,'-c',child,str(root/'scripts'),str(parent)],env=dict(os.environ,TMPDIR=str(other)),capture_output=True,text=True,check=True)
 second=ran.stdout.strip()
 emit('different-TMPDIR-in-tree-collision',same_path=first==second,first_marker_preserved=marker.exists(),second_marker_visible=pathlib.Path(first,'second-marker').exists())
 assert first==second and not marker.exists()
# Positive exclusivity control with same TMPDIR; fallback at 8 held slots.
with stage.directory('ordinary-') as first:
 code="import sys;sys.path.insert(0,sys.argv[1]);import mutant_stage as s;\nwith s.directory('ordinary-') as p: print(p)"
 ran=subprocess.run([sys.executable,'-c',code,str(root/'scripts')],capture_output=True,text=True,check=True)
 assert ran.stdout.strip()!=first
 emit('same-TMPDIR-exclusivity',distinct=True)
# Real production preflight entry point with deliberately red first self-test.
fixture=scratch/'preflight-failure'; (fixture/'scripts').mkdir(parents=True,exist_ok=True)
(fixture/'scripts/run_all_suites.sh').write_bytes((root/'scripts/run_all_suites.sh').read_bytes())
(fixture/'scripts/test_suite_cancellation.py').write_text("print('PLANTED: preflight self-test failure'); raise SystemExit(7)\n")
(fixture/'scripts/owned_process.py').write_bytes((root/'scripts/owned_process.py').read_bytes())
logs=fixture/'logs'; ran=subprocess.run(['bash',str(fixture/'scripts/run_all_suites.sh'),str(logs),'--preflight-only'],capture_output=True,text=True)
assert ran.returncode==2 and 'ABORTING' in ran.stderr
emit('planted-preflight-failure',returncode=ran.returncode,stdout=ran.stdout,stderr=ran.stderr)
workflow=yaml.safe_load((root/'.github/workflows/rtl.yml').read_text())
job=workflow['jobs']['verilator-suites']
step=next(s for s in job['steps'] if s.get('name')=="Require the preflight to have passed for this run's SHA")
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
record=scratch/'suite-preflight'; record.mkdir(exist_ok=True)
for label,result,sha in [('valid','success',head),('planted-failure','failure',head),('cancelled','cancelled',head),('skipped','skipped',head),('wrong-sha','success','0'*40),('missing-sha','success',None)]:
 target=record/'TARGET_SHA'; target.unlink(missing_ok=True)
 if sha: target.write_text(sha+'\n')
 ran=subprocess.run(['bash','--noprofile','--norc','-eo','pipefail','-c',step['run']],cwd=root,env=dict(os.environ,RUNNER_TEMP=str(scratch),GITHUB_SHA=head,GATE_SHA=head,PREFLIGHT_RESULT=result),capture_output=True,text=True)
 emit('aggregate-'+label,returncode=ran.returncode,stdout=ran.stdout,stderr=ran.stderr)
 assert (ran.returncode==0)==(label=='valid')
assert 'verilator-preflight' in job['needs']
watch=workflow['jobs']['ci-fail-fast']; expected=next(s['env']['EXPECTED_JOBS'] for s in watch['steps'] if s.get('name')=='Observe the first failed job')
assert 'Verilator preflight' in json.loads(expected)
emit('preflight-graph',aggregate_needs_preflight=True,watcher_expects_preflight=True,fork_guard=watch['if'])
# Unknown/missing/extra cost entries never select the case population. Real make and grader.
directory=scratch/'make-cases'; directory.mkdir(exist_ok=True)
names=['short','bad','unmeasured','long']
(directory/'Makefile').write_text(''.join('exec-'+n+':\n\t@echo '+n+' >> started\n\t@printf "'+n+' checks: 1 failures: '+('1' if n=='bad' else '0')+'\\n"\n' for n in names))
forms=dict.fromkeys(names,'tally'); results=[]
for table in ({},{'long':999,'short':1,'nonexistent':99999}):
 cases.CASE_SECONDS['fixture']=table
 (directory/'started').unlink(missing_ok=True)
 result=cases.execute_all(directory,'fixture',names,forms,1)
 emit('cost-table-population',table=table,started=(directory/'started').read_text().split(),returned=[r[2].split()[0] for r in result],outcomes=[r[0] for r in result])
 assert [r[2].split()[0] for r in result]==names
 assert [r[0] for r in result]==['pass','failed','pass','pass']
 results.append(result)
assert results[0]==results[1]
emit('scheduling-output-identity',identical=True)
