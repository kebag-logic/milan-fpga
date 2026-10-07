#!/usr/bin/env python3
"""Build a pinned test dependency in scratch and exercise both library profiles."""
import concurrent.futures
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parents[1]
scratch=packet/'scratch/upstream'
scratch.mkdir(exist_ok=True)
rev='91ba387904d7f43c6564486690386e76d4f8bc76'
url=f'https://codeload.github.com/cgreen-devs/cgreen/tar.gz/{rev}'
data=urllib.request.urlopen(url,timeout=60).read()
with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tar:
    tar.extractall(scratch,filter='data')
source=scratch/f'cgreen-{rev}'
prefix=scratch/'prefix'
(packet/'receipts/unit-dependency.json').write_text(json.dumps({'revision':rev,'url':url,'archive_sha256':hashlib.sha256(data).hexdigest()},indent=2)+'\n')
def run(cmd,cwd=repo,env=None):
    print('ARGV',json.dumps([str(x) for x in cmd]),flush=True)
    subprocess.run(cmd,cwd=cwd,env=env,check=True)
run(['cmake','-S',source,'-B',scratch/'cgreen-build',f'-DCMAKE_INSTALL_PREFIX={prefix}','-DCMAKE_BUILD_TYPE=Release'])
run(['make','-C',scratch/'cgreen-build','-j16'])
run(['cmake','--install',scratch/'cgreen-build'])
def profile(mode):
    out=scratch/mode
    log=packet/'receipts'/f'upstream-{mode}.log'
    env=dict(os.environ,LD_LIBRARY_PATH=str(prefix/'lib'),SHLAN_LIBRARY=str(out/'libshlan.so'))
    cmds=[['cmake','-S',repo/'third_party/lwSRP','-B',out,'-DCMAKE_BUILD_TYPE=Debug',
           f'-DCMAKE_PREFIX_PATH={prefix}',f'-DLWSRP_MILAN={mode}'],
          ['make','-C',out,'-j8','unit_tests'],[out/'unit_tests'],
          ['behave'],
          [sys.executable,packet/'scripts/note_reversals.py',repo,mode,prefix]]
    with log.open('w') as stream:
        for cmd in cmds:
            print('ARGV',json.dumps([str(x) for x in cmd]),file=stream,flush=True)
            r=subprocess.run(cmd,cwd=repo/'third_party/lwSRP',env=env,stdout=stream,stderr=subprocess.STDOUT)
            if r.returncode:
                (packet/'receipts'/f'upstream-{mode}.rc').write_text(str(r.returncode)+'\n')
                return r.returncode
    (packet/'receipts'/f'upstream-{mode}.rc').write_text('0\n')
    return 0
# The two profiles share a cap of sixteen compilation jobs.
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(profile,('OFF','ON')))
raise SystemExit(int(any(results)))
