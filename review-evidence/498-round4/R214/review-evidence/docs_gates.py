import os,subprocess,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent.parent;tmp=Path(os.environ['REVIEW_TMP'])
commands=[['scripts/docs_check.py'],['scripts/check_doc_style.py'],['scripts/check_doc_paths.py'],['scripts/gen_toc.py','--check'],['scripts/check_em_dash.py','--base','07294a76e833f1831d9fcbceb8123b8380c4ae76'],['scripts/check_feature_status.py'],['scripts/check_solution_docs.py'],['scripts/check_baremetal_only.py','--check'],['scripts/check_baremetal_only.py','--selftest'],['scripts/pp_srcs.py','--check','--selftest'],['scripts/check_cpp_idiom.py'],['scripts/check_py_idiom.py'],['scripts/check_nvm_record_space.py'],['docs/traceability/gen_module_matrix.py','--check']]
results=[]
for i,args in enumerate(commands):
 cmd=['python3','-B']+args
 with (tmp/('docs-'+str(i)+'.log')).open('w') as out:r=subprocess.run(cmd,cwd=root,stdout=out,stderr=subprocess.STDOUT)
 results.append([cmd,r.returncode]);print('EXIT',r.returncode,' '.join(cmd),flush=True)
(tmp/'docs-results.json').write_text(json.dumps(results,indent=2))
assert all(r==0 for _,r in results)
