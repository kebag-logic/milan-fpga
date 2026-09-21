import json,os,subprocess,time
from runner import ROOT,TMP
commands=[
['scripts/docs_check.py'],['scripts/check_doc_style.py'],['scripts/check_doc_paths.py'],['scripts/gen_toc.py','--check'],['scripts/check_em_dash.py','--base','07294a76e833f1831d9fcbceb8123b8380c4ae76'],['scripts/check_feature_status.py'],['scripts/check_solution_docs.py'],['scripts/check_baremetal_only.py','--check','--selftest'],['scripts/pp_srcs.py','--check','--selftest'],['scripts/check_py_idiom.py'],['scripts/check_cpp_idiom.py'],['scripts/check_nvm_record_space.py'],['docs/traceability/gen_module_matrix.py','--check'],['sw/firmware/nvm_hosttest/test_nvm_firmware.py','--self-test']]
rows=[]
for i,args in enumerate(commands):
 cmd=['python3','-B',*args];start=time.monotonic()
 log=TMP/('check-%02d.log'%i)
 with log.open('w') as out: result=subprocess.run(cmd,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
 row=dict(command=cmd,exit=result.returncode,seconds=round(time.monotonic()-start,2),log=log.name);rows.append(row);print(row,flush=True)
(TMP/'focused-checks.json').write_text(json.dumps(rows,indent=2))
assert all(r['exit']==0 for r in rows)
