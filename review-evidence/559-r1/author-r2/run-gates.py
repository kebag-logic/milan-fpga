from pathlib import Path
import json,os,subprocess,time
out=Path(__file__).parent
commands=[
 ('baremetal',['python3','scripts/check_baremetal_only.py','--check']),
 ('docs',['python3','-B','scripts/docs_check.py']),
 ('docs-no-git',['env','GIT_DIR=/dev/null','python3','-B','scripts/docs_check.py']),
 ('doc-style',['python3','scripts/check_doc_style.py']),
 ('toc',['python3','scripts/gen_toc.py','--check']),
 ('anchors',['python3','scripts/gen_toc.py','--verify-anchors']),
 ('doc-paths',['python3','scripts/check_doc_paths.py']),
 ('module-matrix',['python3','docs/traceability/gen_module_matrix.py','--check']),
 ('xvlog',['python3','scripts/xvlog_gate.py','--check']),
 ('sv-idiom',['python3','scripts/check_sv_idiom.py']),
 ('cpp-idiom',['python3','scripts/check_cpp_idiom.py']),
 ('py-idiom',['python3','scripts/check_py_idiom.py']),
 ('ports',['python3','scripts/check_port_contracts.py']),
 ('naming',['python3','scripts/measure_naming.py','--check']),
 ('test-evidence',['python3','scripts/measure_test_evidence.py','--check']),
 ('diff',['git','diff','--check'])]
results=[]
for name,argv in commands:
 start=time.monotonic()
 with (out/(name+'.log')).open('w') as log:
  p=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
 row=dict(name=name,argv=argv,returncode=p.returncode,seconds=round(time.monotonic()-start,2))
 results.append(row)
 (out/'gate-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(row,flush=True)
