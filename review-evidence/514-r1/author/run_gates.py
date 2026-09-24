import json
import os
from pathlib import Path
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
base='3d2f3e3131c9db5898e1db9dd3e2a35149843109'
commands=[
 ('containment-selftest', ['python3','scripts/check_merge_containment.py','--selftest']),
 ('docs-check', ['python3','scripts/docs_check.py']),
 ('docs-check-no-git', ['env','GIT_DIR=/dev/null','python3','scripts/docs_check.py']),
 ('em-dash', ['python3','scripts/check_em_dash.py','--base',base]),
 ('em-dash-selftest', ['python3','scripts/check_em_dash.py','--selftest']),
 ('doc-style', ['python3','scripts/check_doc_style.py']),
 ('doc-style-selftest', ['python3','scripts/check_doc_style.py','--selftest']),
 ('toc', ['python3','scripts/gen_toc.py','--check']),
 ('toc-selftest', ['python3','scripts/gen_toc.py','--selftest']),
 ('toc-anchors', ['python3','scripts/gen_toc.py','--verify-anchors']),
 ('doc-paths', ['python3','scripts/check_doc_paths.py']),
 ('python-idiom', ['python3','scripts/check_py_idiom.py']),
 ('python-idiom-selftest', ['python3','scripts/check_py_idiom.py','--selftest']),
 ('diff-check', ['git','diff','--check',base]),
 ('diff-check-worktree', ['git','diff','--check']),
]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
results=[]
for name,command in commands:
    path=out/'logs'/f'{name}.log'
    with path.open('wb') as stream:
        result=subprocess.run(command,cwd=root,stdout=stream,stderr=subprocess.STDOUT,timeout=900,check=False)
    results.append(dict(name=name,command=command,rc=result.returncode,head=head,log=str(path.relative_to(out))))
    print(name,'rc',result.returncode,flush=True)
    if result.returncode:
        print(path.read_text(errors='backslashreplace')[-6000:],flush=True)
(out/'logs/gates.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(row['rc'] for row in results))
