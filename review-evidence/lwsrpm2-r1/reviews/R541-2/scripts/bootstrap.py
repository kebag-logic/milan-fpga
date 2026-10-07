# SPDX-License-Identifier: Apache-2.0
"""Install only the pinned unit dependency inside the packet scratch directory."""
import argparse
from pathlib import Path
import subprocess
import json
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True)
a=p.parse_args();packet=a.packet.resolve();scratch=packet/'scratch';scratch.mkdir(exist_ok=True)
(packet/'receipts').mkdir(exist_ok=True)
source=scratch/'cgreen-source';build=scratch/'cgreen-build';prefix=scratch/'deps'
commands=[]
if not source.exists():
    commands.append(['git','clone','--depth','1','--branch','1.6.3',
                     'https://github.com/cgreen-devs/cgreen.git',str(source)])
commands.extend([
    ['cmake','-S',str(source),'-B',str(build),'-DCMAKE_POLICY_VERSION_MINIMUM=3.5',
     '-DCMAKE_INSTALL_PREFIX='+str(prefix),'-DCGREEN_WITH_UNIT_TESTS=OFF','-DCGREEN_WITH_EXAMPLES=OFF'],
    ['make','-C',str(build),'-j16','install']])
for n,cmd in enumerate(commands):
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=480)
    (packet/'receipts'/f'dependency-{n}.log').write_text((r.stdout+r.stderr).replace(str(packet),'$PACKET'))
    (packet/'receipts'/f'dependency-{n}.rc').write_text(str(r.returncode)+'\n')
    assert r.returncode==0
commit=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
assert commit=='abb74b39545fd7006a44e7b763605b7796e05a6e'
(packet/'receipts/dependency-pin.txt').write_text('Unit dependency 1.6.3: '+commit+'\n')
