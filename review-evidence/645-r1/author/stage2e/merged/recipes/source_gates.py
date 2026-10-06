import os,json,subprocess,concurrent.futures
from pathlib import Path
repo=Path(os.environ['REPO']); work=Path(os.environ['STAGE_ROOT'])/'source';work.mkdir(exist_ok=True)
evidence=Path(os.environ['EVIDENCE'])
prior=json.loads((evidence.parent/'stage2d/source-final/commands.json').read_text())['commands']
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
def run(item):
    argv=item['argv'][:];name=item['name']
    if argv[0]=='python3':argv[0]=os.environ['DOC_PYTHON'] if name in ['anchors','docs','paths','punctuation','style','toc'] else 'python3'
    if name=='punctuation':argv[-1]='28f9666f'
    if name=='diff-check':argv=['git','diff','--check','28f9666f']
    with (work/(name+'.log')).open('w') as log:
        rc=subprocess.run(argv,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (work/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,rc,flush=True)
    return {'name':name,'argv':argv,'rc':rc}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,prior))
(work/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
rc=int(any(r['rc'] for r in results));(work/'all.rc').write_text(str(rc)+'\n');raise SystemExit(rc)
