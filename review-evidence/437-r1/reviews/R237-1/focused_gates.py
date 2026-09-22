import json,os,subprocess,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
OUT=Path(__file__).resolve().parent
REPO=Path('$VALIDATION_STORAGE/reviews/r237-437-r1')
commands=[('toc-selftest',['scripts/gen_toc.py','--selftest']),('toc-check',['scripts/gen_toc.py','--check']),('toc-anchors',['scripts/gen_toc.py','--verify-anchors']),('em-dash-selftest',['scripts/check_em_dash.py','--selftest']),('em-dash-base',['scripts/check_em_dash.py','--base','88e9276b2a220c716f64a843f7e1eb8f9265e896']),('docs',['scripts/docs_check.py']),('python-idiom',['scripts/check_py_idiom.py'])]
def run(row):
 name,args=row;cmd=['rtk','proxy','python3','-B',*args];start=time.time()
 p=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',MAX_JOBS='8'))
 (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
 return {'name':name,'command':cmd,'head':'65df1df50a80cd5f540a93d8f0cfabc97da3da75','exit':p.returncode,'seconds':round(time.time()-start,3),'output':p.stdout+p.stderr}
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,commands))
(OUT/'focused-gates.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
assert all(r['exit']==0 for r in results)
