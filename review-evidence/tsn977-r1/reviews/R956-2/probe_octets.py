#!/usr/bin/env python3
"""Check each saved-ID comparison term using only the P4 public-input test.

Usage: probe_octets.py CHECKOUT MUTATION_WORK GTEST_PREFIX [--jobs N]
Reuses the completed campaign's compiled test objects; no checkout edits.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

p = argparse.ArgumentParser()
p.add_argument('checkout', type=Path)
p.add_argument('mutation_work', type=Path)
p.add_argument('gtest', type=Path)
p.add_argument('--jobs', type=int, default=3)
a = p.parse_args()
packet = Path(__file__).resolve().parent
work = packet / 'scratch/octet-probes'
work.mkdir(parents=True, exist_ok=True)
base = a.mutation_work.resolve() / 'baseline'
source = (a.checkout / 'src/acmp.c').read_text()
env = {k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}
env['PKG_CONFIG_PATH'] = str(a.gtest / 'lib/pkgconfig')
env['LD_LIBRARY_PATH'] = str(a.gtest / 'lib')
libs = subprocess.check_output(['pkg-config', '--libs', 'gtest', 'gmock'], env=env, text=True).split()
terms = {2: '(uint32_t)(p[2] ^ (unique >> 8))', 3: '(uint32_t)(p[3] ^ (unique & 0xFFu))'}
for start, variable in [(4, 'th'), (8, 'tl'), (12, 'ch'), (16, 'cl')]:
    terms[start] = f'(p[{start}] ^ ({variable} >> 24))'
    terms[start+1] = f'(p[{start+1}] ^ (({variable} >> 16) & 0xFFu))'
    terms[start+2] = f'(p[{start+2}] ^ (({variable} >> 8) & 0xFFu))'
    terms[start+3] = f'(p[{start+3}] ^ ({variable} & 0xFFu))'
plants = [('control', None, None)] + [(f'omit-octet-{n}', old, '0u') for n,old in terms.items()]
registry = json.loads((a.checkout / 'tests/mutations.json').read_text())
plants += [(m['name'], m['old'], m['new']) for m in registry if m['name'] in
           ('record-drop-unique','record-drop-talker','record-drop-controller')]

def run(plant):
    name, old, new = plant
    d = work / name
    d.mkdir(exist_ok=True)
    if old is not None:
        assert source.count(old) == 1, name
    (d/'acmp.c').write_text(source if old is None else source.replace(old,new))
    commands = [
        ['gcc','-std=c11','-O0','-g','-Wall','-Wextra','-Werror','-DNDEBUG','-DCTRL_REENTRY_ASSERT',
         '-I'+str(a.checkout/'include'),'-c',str(d/'acmp.c'),'-o',str(d/'acmp.o')],
        ['g++',str(d/'acmp.o'),str(base/'acmp.cpp.o'),str(base/'main.o'),*libs,'-o',str(d/'probe')],
        [str(d/'probe'),'--gtest_filter=AcmpCore.P4EachIdOctetChangedAloneIsSaved',
         '--gtest_output=xml:'+str(d/'result.xml')]]
    codes = []
    with (d/'run.log').open('w') as log:
        for cmd in commands:
            rc = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=120).returncode
            codes.append(rc)
            if rc and len(codes)<3:
                return {'name':name,'status':'ERROR','codes':codes}
    x = ET.parse(d/'result.xml').getroot()
    cases = list(x.iter('testcase'))
    complete = len(cases)==1 and x.get('tests')=='1' and x.get('errors')=='0' and x.get('disabled')=='0'
    complete = complete and all(c.get('status')=='run' and c.get('result')=='completed' and not c.findall('skipped') for c in cases)
    needle = "P4 a rebind changing one octet of the record's IDs alone is saved"
    caught = codes==[0,0,1] and complete and any(needle in f.get('message','') for c in cases for f in c.findall('failure'))
    passed = codes==[0,0,0] and complete and x.get('failures')=='0'
    return {'name':name,'status': 'PASS' if old is None and passed else 'CAUGHT' if old is not None and caught else 'ERROR',
            'codes':codes,'test': 'AcmpCore.P4EachIdOctetChangedAloneIsSaved', 'complete':complete}

with ThreadPoolExecutor(max_workers=min(a.jobs,16)) as pool:
    results = list(pool.map(run,plants))
(work/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({s:sum(r['status']==s for r in results) for s in ('PASS','CAUGHT','ERROR')}))
raise SystemExit(any(r['status']=='ERROR' for r in results))
