#!/usr/bin/env python3
"""Reproduce fresh-draw sensitivity without modifying the reviewed checkout.

Usage: PKG_CONFIG_PATH=<gtest-1.14-prefix>/lib/pkgconfig python3 probe.py REPO PACKET
"""
import concurrent.futures as cf
import io
import json
import os
from pathlib import Path
import shlex
import subprocess as sp
import sys
import tarfile

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
scratch = packet / 'scratch' / 'probe'
receipts = packet / 'probe'
receipts.mkdir(parents=True, exist_ok=True)
head = '55852269db3554900d2b71e6f9a7b153cff69e14'
old = '61a504eec3ec3de828ccd80076212533ef58644b'
env = {k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}
assert sp.check_output(['pkg-config','--modversion','gtest'], env=env, text=True).strip() == '1.14.0'
flags = shlex.split(sp.check_output(['pkg-config','--cflags','--libs','gtest','gmock'], env=env, text=True))
flags = [('-isystem'+f[2:]) if f.startswith('-I') else f for f in flags]
registry = json.loads(sp.check_output(['git','show',head+':tests/mutations.json'],cwd=repo))
plants = {p['name']:p for p in registry}
needle = 'A2 GM_CHANGE in WAITING: DELAY with a 0..4 s draw (5.6.3.5.7)'

def run_one(spec):
    ref, kind, plant = spec
    name = ('head' if ref == head else 'old')+'-'+kind+'-'+(plant or 'clean')
    root = scratch/name
    root.mkdir(parents=True, exist_ok=True)
    data = sp.check_output(['git','archive',ref],cwd=repo)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(root, filter='data')
    if plant:
        p = plants[plant]
        path = root/p['path']
        source = path.read_text()
        assert source.count(p['old']) == 1
        path.write_text(source.replace(p['old'], p['new']))
    lines=[]
    def command(argv):
        result=sp.run(argv,cwd=root,env=env,text=True,stdout=sp.PIPE,stderr=sp.STDOUT,timeout=180)
        lines.append('$ '+shlex.join(argv)+'\n'+result.stdout+'\nrc='+str(result.returncode)+'\n')
        if result.returncode and argv[0] in ('gcc','g++'):
            print(result.stdout, flush=True)
        return result
    opt = ['-O0','-g'] if kind=='Debug' else ['-O3','-DNDEBUG']
    assert command(['gcc','-std=c11','-Wall','-Wextra','-Werror','-DNDEBUG','-DCTRL_REENTRY_ASSERT',*opt,'-Iinclude','-c','src/adp.c','-o','adp.o']).returncode == 0
    assert command(['g++','-std=c++20','-Wall','-Wextra','-Werror',*opt,'-Iinclude','tests/test_adp.cpp','tests/main.cpp','adp.o',*flags,'-o','adp_tests']).returncode == 0
    focused=command(['./adp_tests','--gtest_filter=AdpCore.A0toA2Schedule'])
    full=command(['./adp_tests'])
    expected_failure=bool(plant and ref==head)
    assert focused.returncode == (1 if expected_failure else 0)
    assert full.returncode == (1 if expected_failure else 0)
    if expected_failure:
        assert needle in focused.stdout
    raw=''.join(lines).replace(str(repo),'<checkout>').replace(str(packet),'<packet>')
    for flag in flags:
        if flag.startswith(('-isystem','-L')):
            raw=raw.replace(flag,('-isystem' if flag.startswith('-isystem') else '-L')+'<test-dependency>')
    (receipts/(name+'.log')).write_text(raw)
    row=dict(name=name,head=ref,configuration=kind,plant=plant,focused_rc=focused.returncode,full_adp_rc=full.returncode,expected_failure=expected_failure,needle_observed=needle in focused.stdout)
    print(json.dumps(row),flush=True)
    return row

specs=[]
for kind in ('Debug','Release'):
    specs += [(head,kind,None),(old,kind,'gm-change-rearms-without-a-draw'),(head,kind,'gm-change-rearms-without-a-draw'),(head,kind,'gm-change-draws-startup-kind')]
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(run_one,specs))
(receipts/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
