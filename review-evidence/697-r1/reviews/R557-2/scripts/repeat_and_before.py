#!/usr/bin/env python3
"""Repeat the campaign and compare hosted test results across comment removal."""
import concurrent.futures as cf
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET
repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3])
work=packet/'scratch/supplement'
source=work/'before'
source.mkdir(parents=True,exist_ok=True)
out=packet/'receipts/supplement';out.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive','086e5d37c19fbb6f4a628c376ce8f9f20e51df14'],cwd=repo))) as a:
    a.extractall(source,filter='data')
env={k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}
env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(work),ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',UBSAN_OPTIONS='halt_on_error=1')
def clean(s):return s.replace(str(packet),'<PACKET>').replace(str(repo),'<REPO>').replace(str(Path.home()),'<HOME>')
def run(name,cmd,cwd):
    p=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=570)
    (out/(name+'.log')).write_text('COMMAND: '+clean(' '.join(map(str,cmd)))+'\n'+clean(p.stdout))
    (out/(name+'.rc')).write_text(str(p.returncode)+'\n')
    print(name,p.returncode,flush=True)
    assert p.returncode==0,p.stdout
    return p.stdout
def native(kind,cc,cxx,flag):
    b=work/kind
    run(kind+'-configure',['cmake','-S',source,'-B',b,'-DCMAKE_BUILD_TYPE=Debug','-DCMAKE_C_COMPILER='+cc,'-DCMAKE_CXX_COMPILER='+cxx,flag],source)
    run(kind+'-build',['cmake','--build',b,'-j4'],source)
    comparisons=[]
    for binary in ('adp_tests','acmp_tests','maap_tests','port_tests','adp_release','adp_debug','maap_debug'):
        outcomes=[]
        for label,d in (('before',b),('after',packet/'scratch/runs'/kind)):
            xml=work/(kind+'-'+binary+'-'+label+'.xml')
            xml.unlink(missing_ok=True)
            run(kind+'-'+binary+'-'+label,[d/binary,'--gtest_output=xml:'+str(xml)],source if label=='before' else repo)
            root=ET.parse(xml).getroot()
            cases=[(c.get('classname')+'.'+c.get('name'),c.get('status'),c.get('result'),len(c.findall('failure')),len(c.findall('skipped'))) for c in root.iter('testcase')]
            outcomes.append(sorted(cases))
            assert len(cases)==int(root.get('tests')) and cases and not any(x[3] or x[4] for x in cases)
        assert outcomes[0]==outcomes[1],binary
        comparisons.append({'binary':binary,'instances':len(outcomes[0]),'same_completed_outcomes':True})
    return {kind:comparisons}
def campaign():
    dest=work/'mutations-repeat'
    run('mutation-repeat',[sys.executable,repo/'scripts/mutation.py','--work',dest,'--jobs','4'],repo)
    results=json.loads((dest/'results.json').read_text())
    table=json.loads((repo/'tests/mutations.json').read_text())
    assert {x['name'] for x in results}=={x['name'] for x in table}
    assert len(results)==311 and all(x['status']=='CAUGHT' for x in results)
    (out/'mutation-repeat-results.json').write_text(clean(json.dumps(results,indent=2))+'\n')
    # Reuse the same work directory to prove ordinary repeated runs stay valid.
    run('mutation-reused',[sys.executable,repo/'scripts/mutation.py','--work',dest,'--jobs','4'],repo)
    results=json.loads((dest/'results.json').read_text())
    assert len(results)==311 and all(x['status']=='CAUGHT' for x in results)
    (out/'mutation-reused-results.json').write_text(clean(json.dumps(results,indent=2))+'\n')
    return {'mutations_fresh':311,'mutations_reused':311}
def rv32():
    run('before-rv32',[sys.executable,source/'scripts/baremetal.py','--work',work/'rv32','--jobs','1'],source)
    (out/'before-rv32-results.json').write_text((work/'rv32/results.json').read_text())
    return {'before_rv32_configurations':2}
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    fs=[pool.submit(native,'gcc','gcc','g++','-DTSN_COVERAGE=ON'),
        pool.submit(native,'clang-sanitizers','clang','clang++','-DTSN_SANITIZERS=ON'),
        pool.submit(campaign),pool.submit(rv32)]
    results=[f.result() for f in fs]
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
