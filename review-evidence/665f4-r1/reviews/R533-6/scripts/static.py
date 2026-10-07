#!/usr/bin/env python3
"""Capture exact-head merge, pin, exclusion and focused documentation evidence."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parents[1]
out=packet/'receipts'
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'))
head=git('rev-parse','HEAD').decode().strip()
assert head=='cce554f64f6bdab1f6d26e5c4d7b46d54d228c52'
(out/'scope-diff.txt').write_bytes(git('diff','--stat','db9aa8c9','HEAD'))
(out/'history.txt').write_bytes(git('log','--format=%H %s','--first-parent','db9aa8c9..HEAD'))
(out/'merge-resolution.diff').write_bytes(git('show','--remerge-diff','--format=%H %P %s','069874955'))
dev='e21c1ca024d37ea188ad15b5c8f9c2dae18628df'
paths=git('ls-tree','-r','--name-only',dev,'sw/firmware/ctrl/maap').decode().splitlines()
paths+=['sw/firmware/ctrl/app/ctrl_app.c','sw/firmware/ctrl/test/ctrl_build.py','tb/verilator/mbx/Makefile']
paths+=git('ls-tree','-r','--name-only',dev,'sw/firmware/ctrl/test').decode().splitlines()
paths=[p for p in paths if '/test/' not in p or 'maap' in p or p.endswith('ctrl_build.py')]
same={p:git('rev-parse',dev+':'+p).decode().strip()==git('rev-parse','HEAD:'+p).decode().strip() for p in paths}
assert all(same.values()),same
imported_rtl=git('diff','--name-only',dev,'HEAD','hdl').decode().splitlines()
assert not imported_rtl
lw=repo/'third_party/lwSRP'
def lwgit(*args):return subprocess.check_output(['git','-C',str(lw),*args]).decode().strip()
assert not lwgit('diff','a4cbe41..9197193','--','src')
result={'head':head,'dev':dev,'F2_blobs_preserved':same,'RTL_delta_from_dev':imported_rtl,
        'lwSRP_head':lwgit('rev-parse','HEAD'),'lwSRP_production_delta_from_round5':'empty',
        'coverage_exclusion_code_delta_from_round5':git('diff','500b8f64..HEAD','--','sw/firmware/gtest/fw_coverage.py').decode(),
        'probe_sha256':hashlib.sha256((packet/'scripts/independent.cpp').read_bytes()).hexdigest()}
(out/'source-checks.json').write_text(json.dumps(result,indent=2)+'\n')
commands=[['python3','sw/mailbox/gen_mailbox.py','--check'],
          ['python3','scripts/check_submodule_docs.py'],
          ['python3','scripts/check_cpp_idiom.py'],
          ['python3','scripts/check_py_idiom.py'],
          ['git','diff','--check','500b8f64','HEAD']]
results=[]
for index,cmd in enumerate(commands):
    r=subprocess.run(cmd,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (out/f'static-{index}.log').write_text(r.stdout)
    results.append({'argv':cmd,'rc':r.returncode})
    print(cmd,r.returncode,flush=True)
(out/'static.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(int(any(r['rc'] for r in results)))
