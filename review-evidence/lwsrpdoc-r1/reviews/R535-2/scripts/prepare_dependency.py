#!/usr/bin/env python3
"""Build the test dependency in a packet-local prefix; never install system-wide."""
import os
from pathlib import Path
import subprocess
import sys

packet=Path(sys.argv[1]).resolve()
(packet/'receipts').mkdir(parents=True,exist_ok=True)
scratch=packet/'scratch'
scratch.mkdir(exist_ok=True)
(scratch/'temporary').mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(scratch/'temporary'))
src=scratch/'cgreen-source'
build=scratch/'cgreen-build'
sdk=scratch/'sdk'
commands=[]
if not src.exists():
    commands.append(('dependency-fetch',['git','clone','--depth','1','--branch','1.6.5',
        'https://github.com/cgreen-devs/cgreen.git',str(src)]))
commands += [
    ('dependency-configure',['cmake','-S',str(src),'-B',str(build),
      '-DCGREEN_WITH_UNIT_TESTS=OFF','-DCGREEN_WITH_STATIC_LIBRARY=OFF',
      '-DCGREEN_WITH_LIBXML2=OFF','-DCMAKE_INSTALL_PREFIX='+str(sdk)]),
    ('dependency-build',['make','-C',str(build),'-j16']),
    ('dependency-install',['cmake','--install',str(build)]),
]
for name,command in commands:
    result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=540)
    (packet/'receipts'/f'{name}.log').write_text((result.stdout+result.stderr).replace(str(packet),'$PACKET'))
    (packet/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
    assert result.returncode==0,name
identity=subprocess.check_output(['git','rev-parse','HEAD'],cwd=src,text=True).strip()
assert identity=='4fd4b9336ac813db3d7d6ef74ab6d91a159ff4ae',identity
print('Dependency prefix ready. Source identity:',identity)
