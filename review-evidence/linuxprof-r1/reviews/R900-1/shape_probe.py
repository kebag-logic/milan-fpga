#!/usr/bin/env python3
"""Preprocess exact base/head scheduler headers for all existing FPGA shapes.

Usage: python3 shape_probe.py REPO PACKET
Also compile the unchanged loop translation unit with the host shape.
All generated headers and object files remain under PACKET/scratch.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo,packet = map(lambda s:Path(s).resolve(),sys.argv[1:3])
scratch=packet/'scratch'/'shape'
scratch.mkdir(parents=True,exist_ok=True)
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(packet/'scratch'))
base='854bd7236792ce1adbd10c43b13a6a5002ad3bb6'
head='677d605f37c3a80654df1dd2cde053b57242845b'
for tag,revision in [('base',base),('head',head)]:
    directory=scratch/tag
    directory.mkdir(exist_ok=True)
    (directory/'ctrl_loop.h').write_bytes(subprocess.check_output(
        ['git','show',revision+':sw/firmware/ctrl/loop/ctrl_loop.h'],cwd=repo))
probe=scratch/'probe.c'
probe.write_text('#include "ctrl_loop.h"\n')
configs=list(sorted((repo/'configs').glob('endstation_*.yaml')))+[repo/'configs/host/endstation_host_example.yaml']
headers={}
for config in configs:
    dest=scratch/(config.stem+'.h')
    subprocess.run(['python3','-B',str(repo/'sw/firmware/ctrl/srp/srp_entity.py'),str(config),'-o',str(dest)],
                   cwd=repo,env=env,check=True)
    headers[config.stem]=dest

def case(item):
    name, header, interfaces = item
    records={}
    for tag in ('base','head'):
        records[tag]={}
        for mode in ('-P','-dM'):
            command=['cc','-E',mode,'-I'+str(scratch/tag),
                '-I'+str(repo/'sw/firmware/ctrl/mbx'),'-DMBX_N_IF='+str(interfaces),
                *(['-include',str(header)] if header else []),str(probe)]
            result=subprocess.run(command,capture_output=True,env=env)
            records[tag][mode]=dict(rc=result.returncode,sha256=hashlib.sha256(result.stdout).hexdigest(),
                                   shape_refusal=b'THE SHAPES:' in result.stderr)
    assert records['base']==records['head'],(name,interfaces,records)
    return dict(shape=name,interfaces=interfaces,results=records['head'],identical=True)
items=[('default',None,1),('default',None,2)]
items += [(name,path,n) for name,path in headers.items() if 'host' not in name for n in (1,2)]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(case,items))
host=headers['endstation_host_example']
command=['cc','-std=c11','-Wall','-Wextra','-Werror','-pedantic','-DCTRL_HOST_PLATFORM',
         '-include',str(host),*[ '-I'+str(repo/'sw/firmware/ctrl'/part) for part in ('loop','mbx','port')],
         '-I'+str(repo/'third_party/tsn-c-stack/include'),
         '-c',str(repo/'sw/firmware/ctrl/loop/ctrl_loop.c'),'-o',str(scratch/'host-loop.o')]
compiled=subprocess.run(command,capture_output=True,env=env)
rows.append(dict(case='host loop C translation unit including static assertions',rc=compiled.returncode,
                 stderr=compiled.stderr.decode()))
assert compiled.returncode==0,compiled.stderr.decode()
(packet/'shape-result.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
