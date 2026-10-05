"""Reproduce offline review receipts after fetching public evidence objects.

Usage: python3 -B reproduce.py REPO OUTPUT_DIRECTORY
Requires evidence commit 871fc1ae68e2fcdfa7abb134956973b455c8bee5 in REPO.
Only OUTPUT_DIRECTORY/scratch receives extracted evidence or build files.
Independent bounded commands run concurrently; the foreground driver waits.
"""
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path

repo,out=map(lambda x:Path(x).resolve(),sys.argv[1:])
out.mkdir(exist_ok=True,parents=True);scratch=out/'scratch';scratch.mkdir(exist_ok=True)
rev='871fc1ae68e2fcdfa7abb134956973b455c8bee5'
prefix='review-evidence/653-b12-r1/'
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'))
for folder,dest in [('author','evidence'),('author-r2','evidence-r2')]:
    target=scratch/dest;target.mkdir(exist_ok=True)
    for name in git('ls-tree','-r','--name-only',rev,prefix+folder+'/').decode().splitlines():
        (target/Path(name).name).write_bytes(git('show',rev+':'+name))
manifest=json.loads(git('show',rev+':'+prefix+'MANIFEST.json'))
mf=scratch/'publication-manifest.json'
mf.write_text(json.dumps([r for r in manifest if r['file'].startswith('author-r2/')],indent=2)+'\n')
scripts=Path(__file__).resolve().parent
p=scratch/'evidence-r2'
tasks={
    'startup-replay':[sys.executable,'-B',str(p/'check_startup.py'),str(p)],
    'restore-controls':[sys.executable,'-B',str(p/'check_restore.py'),str(p),str(scratch/'restore-controls')],
    'independent-audit':[sys.executable,'-B',str(scripts/'independent_audit.py'),str(p),str(scratch/'evidence'),str(repo),str(mf)],
    'focused-probes':[sys.executable,'-B',str(scripts/'focused_probes.py'),str(p),str(scratch/'focused')],
}
def run(item):
    name,cmd=item
    result=subprocess.run(cmd,cwd=repo,capture_output=True,text=True,timeout=120)
    (out/(name+'.log')).write_text(result.stdout+result.stderr)
    (out/(name+'.rc')).write_text(str(result.returncode)+'\n')
    safe=[a.replace(str(scratch),'SCRATCH').replace(str(repo),'REPO').replace(str(scripts),'SCRIPTS') for a in cmd]
    return dict(name=name,argv=safe,rc=result.returncode)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,tasks.items()))
results.append(run(('integrity',[sys.executable,'-B',str(scripts/'check_integrity.py'),str(repo)])))
(out/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
sys.exit(0 if all(r['rc']==0 for r in results) else 1)
