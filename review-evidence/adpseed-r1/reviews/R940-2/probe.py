#!/usr/bin/env python3
"""Focused ADP controls. Usage: probe.py SOURCE PACKET GTEST_PREFIX"""
import concurrent.futures
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET

src, packet, sdk = map(lambda p: Path(p).resolve(), sys.argv[1:])
work = packet / 'scratch' / 'probes'
out = packet / 'receipts'
work.mkdir(parents=True, exist_ok=True)
out.mkdir(exist_ok=True)
env = os.environ.copy()
env['PKG_CONFIG_PATH'] = str(sdk / 'lib/pkgconfig')
for k in list(env):
    if k.startswith('GTEST_'): del env[k]
def pkg(arg):
    return subprocess.check_output(['pkg-config', arg, 'gmock', 'gtest'], env=env, text=True).strip()
assert pkg('--modversion').splitlines() == ['1.14.0', '1.14.0']
flags, libs = shlex.split(pkg('--cflags')), shlex.split(pkg('--libs'))
flags = [v for f in flags for v in (['-isystem',f[2:]] if f.startswith('-I') else [f])]
def run(cmd, log):
    r = subprocess.run(cmd, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)
    return r.returncode
with (out/'probe-build.log').open('w') as log:
    for source, name in [('tests/test_adp.cpp','tests.o'),('tests/main.cpp','main.o')]:
        assert run(['g++','-std=c++20','-O0','-g','-Wall','-Wextra','-Werror',*flags,'-I'+str(src/'include'),'-c',str(src/source),'-o',name], log)==0
    (out/'probe-build.rc').write_text('0\n')
plants = json.loads((src/'tests/mutations.json').read_text())
names = ['seed-left-at-zero','adp-seed-end-around-carry-added','adp-discover-draw-sampled','adp-seed-interface-low-bit-only','adp-seed-without-interface']
selected = [p for p in plants if p['name'] in names]
assert len(selected)==5
original = (src/'src/adp.c').read_text()
def arm(p):
    name = p['name'] if p else 'baseline'
    d=work/name; d.mkdir(exist_ok=True)
    text=original
    if p:
        assert text.count(p['old'])==1
        text=text.replace(p['old'],p['new'])
    (d/'adp.c').write_text(text)
    with (out/(name+'.log')).open('w') as log:
        assert run(['gcc','-std=c11','-O0','-g','-Wall','-Wextra','-Werror','-DNDEBUG','-I'+str(src/'include'),'-c',str(d/'adp.c'),'-o',str(d/'adp.o')],log)==0
        assert run(['g++','tests.o','main.o',str(d/'adp.o'),*libs,'-o',str(d/'test')],log)==0
        xml=out/(name+'.xml')
        rc=run([str(d/'test'),'--gtest_output=xml:'+str(xml)],log)
    (out/(name+'.rc')).write_text(str(rc)+'\n')
    root=ET.parse(xml).getroot()
    cases=list(root.iter('testcase'))
    assert cases and not list(root.iter('skipped'))
    failures={c.get('classname')+'.'+c.get('name'):'\n'.join(f.get('message','') for f in c.findall('failure')) for c in cases if c.findall('failure')}
    if p:
        assert rc==1 and all(k['needle'] in failures.get(k['test'],'') for k in p['kills'])
    else:
        assert rc==0 and not failures
    return dict(name=name,rc=rc,tests=len(cases),failures=list(failures),named_killer_verified=bool(p))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results=list(pool.map(arm,[None,*selected]))
(out/'probe-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
