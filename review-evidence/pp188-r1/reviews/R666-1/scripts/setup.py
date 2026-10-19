#!/usr/bin/env python3
"""Prepare isolated exact-head sources and bounded build wrappers.

Usage: setup.py SOURCE PACKET SIMULATOR
SIMULATOR must report version 5.050. No source checkout bytes are modified.
"""
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

root,packet,simulator=map(lambda s:Path(s).resolve(),sys.argv[1:])
head='cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==head
identity=subprocess.check_output([str(simulator),'--version'],text=True)
assert '5.050' in identity
for directory in ['scripts','receipts','scratch/bin']:(packet/directory).mkdir(parents=True,exist_ok=True)
(packet/'receipts/simulator-identity.txt').write_text(identity)
source=packet/'scratch/source';source.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',head],cwd=root))) as archive:
    archive.extractall(source,filter='data')
subprocess.run(['git','init','-q',str(source)],check=True)
subprocess.run(['git','-C',str(source),'fetch','-q',str(root),head],check=True)
subprocess.run(['git','-C',str(source),'reset','--mixed','FETCH_HEAD'],check=True)
wrapper=packet/'scratch/bin/verilator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\nargs=sys.argv[1:]\n'
                   'for i,a in enumerate(args[:-1]):\n'
                   " if a=='-j': args[i+1]='2'\n"
                   f'os.execv({str(simulator)!r},["verilator",*args])\n')
wrapper.chmod(0o755)
wrapper=packet/'scratch/bin/make'
wrapper.write_text('#!/bin/sh\nexec /usr/bin/make -j16 "$@"\n');wrapper.chmod(0o755)
print('Prepared',source)
