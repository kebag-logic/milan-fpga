"""Four independent single-site restorations, tested by the default self-test."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
edits={
 'shared-decoder':('check_merge_containment.py','os.fsdecode(p.stdout)', 'p.stdout.decode("utf-8", "surrogateescape")'),
 'patch-inverse':('check_merge_containment.py','os.fsencode(patch)', 'patch.encode("utf-8", "surrogateescape")'),
 'retention-decoder':('merge_containment_replay.py','os.fsdecode(name)', 'name.decode("utf-8", "surrogateescape")'),
 'returned-name':('merge_containment_replay.py','os.fsencode(path)', 'path.encode("utf-8", "surrogateescape")'),
}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)

def run(item):
    name,(filename,before,after)=item
    with tempfile.TemporaryDirectory(prefix='r251-restore-') as td:
        dest=Path(td)
        for source in (a.checkout/'scripts').glob('*containment*.py'):
            (dest/source.name).write_bytes(source.read_bytes())
        target=dest/filename
        content=target.read_text()
        assert content.count(before)==1, (name,before)
        target.write_text(content.replace(before,after))
        (a.output/(name+'.diff.txt')).write_text(f'{filename}\n- {before}\n+ {after}\n')
        cmd=['rtk','proxy','python3','-B',str(dest/'check_merge_containment.py'),'--selftest']
        start=time.monotonic()
        r=subprocess.run(cmd,env=env,capture_output=True)
        (a.output/(name+'.stdout')).write_bytes(r.stdout)
        (a.output/(name+'.stderr')).write_bytes(r.stderr)
        failures=[s for s in r.stdout.decode(errors='backslashreplace').splitlines() if 'FAIL' in s]
        record={'name':name,'argv':cmd,'exit':r.returncode,'seconds':time.monotonic()-start,
                'failed_assertions':failures,'detected':r.returncode!=0 and bool(failures)}
        assert record['detected'],record
        print(name,'detected; exit',r.returncode,'failure lines',len(failures),flush=True)
        return record

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    rows=list(pool.map(run,edits.items()))
(a.output/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS: default self-test detects all four restorations.')
