#!/usr/bin/env python3
"""Spot-check the changed measurement and invalid-anchor arms in disposable files."""
import ast
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
text=(root/'tb/tools/torture_campaign.py').read_text()
previous=(out/'public/reviews/R699-2/scripts/reviewer_mutants_r2.py').read_text()
tree=ast.parse(previous)
old=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and
         isinstance(n.targets[0],ast.Attribute) and n.targets[0].attr=='MUTANTS')
chosen=[(m[0].split()[0],m[1],m[2],'test_audio_capture_losses_advance_the_clocks') for m in old
        if m[0].startswith(('N07 ','N30 ','N31 '))]
spec=importlib.util.spec_from_file_location('shipped_mutants',root/'tb/tools/torture_release_mutants.py')
driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver)
names={"qualified interval runs to the capture's end",'required duration not enforced',
       'constant-mask track adopted as a slip','a run fits whole or not at all',
       'departures after a slip not judged again'}
chosen += [(f'D{i}',old,new,test) for i,(name,old,new,test) in enumerate(driver.MUTANTS) if name in names]

def run(m):
    name,old,new,test=m
    assert text.count(old)==1,(name,text.count(old))
    folder=out/'scratch'/name;folder.mkdir(exist_ok=True)
    src=folder/'torture_campaign.py';src.write_text(text.replace(old,new))
    command=[sys.executable,'-B',str(src),'--self-test']
    result=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=300)
    (out/'receipts'/f'{name}.log').write_text(result.stdout+result.stderr)
    (out/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
    failures=re.findall(r'^FAIL: (\w+)',result.stderr,re.M)
    killed=result.returncode==1 and test in failures
    print(name,'KILLED' if killed else 'NOT KILLED',failures,flush=True)
    return dict(name=name,rc=result.returncode,expected_failure=test,failures=failures,killed=killed)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(run,chosen))
(out/'spot-mutants.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(not all(r['killed'] for r in results))
