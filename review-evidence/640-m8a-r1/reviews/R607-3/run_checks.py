#!/usr/bin/env python3
"""Run bounded independent checks concurrently and wait for every foreground child."""
import argparse, concurrent.futures, json, os, pathlib, subprocess
ap=argparse.ArgumentParser();ap.add_argument('repo',type=pathlib.Path);ap.add_argument('--python',required=True);ap.add_argument('--markdown-python',required=True);ap.add_argument('--sdk-archive',required=True);a=ap.parse_args()
p=pathlib.Path(__file__).resolve().parent;s=p/'scratch';(s/'raw').mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(s),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
py=a.python;md=a.markdown_python
jobs=[('resource-baseline',[py,'syn/ooc/pp_resource_gate.py','check-baseline']),
 ('test-evidence',[py,'scripts/measure_test_evidence.py','--check']),
 ('fail-fast',[py,'scripts/measure_fail_fast.py','--check']),
 ('todo',[py,'scripts/check_todo_ownership.py']),
 ('integrity-before',['python3',str(p/'verify_checkout.py'),str(a.repo)]),
 ('scope-selftest',[py,'-I','scripts/ci_scope.py','--selftest']),
 ('scope-page',[py,'-I','scripts/ci_scope.py','docs/design/SPLIT_CONTROL_MEMORY.md']),
 ('events-check',[py,'scripts/ci_events.py','--check']),('events-selftest',[py,'scripts/ci_events.py','--selftest']),
 ('docs-check',[md,'scripts/docs_check.py']),('doc-paths',[md,'scripts/check_doc_paths.py']),
 ('doc-style',[md,'scripts/check_doc_style.py']),('contents',[md,'scripts/gen_toc.py','--check']),
 ('anchors',[md,'scripts/gen_toc.py','--verify-anchors']),('em-dash',[md,'scripts/check_em_dash.py','--base','e8454e2751d05b02ee8e5a571857589ab358ab86']),
 ('python-idiom',[py,'scripts/check_py_idiom.py']),('hygiene',[py,'scripts/check_hygiene.py','--check']),
 ('runner-selftest',['bash','scripts/run_litex_sims.sh','--selftest']),
 ('diff-check',['git','diff','--check','e8454e2751d05b02ee8e5a571857589ab358ab86..HEAD']),
 ('sdk',['python3','scripts/ci_rv32_sdk.py','--archive',a.sdk_archive,'--destination',str(s/'sdk')])]
def run(job):
 name,cmd=job
 with (s/'raw'/f'{name}.log').open('w') as log:
  print('COMMAND',json.dumps(cmd),file=log,flush=True)
  rc=subprocess.run(cmd,cwd=a.repo,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=540).returncode
 (s/'raw'/f'{name}.rc').write_text(str(rc)+'\n');print(name,rc,flush=True);return [name,rc,cmd]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(run,jobs))
(s/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
