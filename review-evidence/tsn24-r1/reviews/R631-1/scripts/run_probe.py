#!/usr/bin/env python3
"""Compile and execute the independent public-API state-model probe."""
import argparse
import os
from pathlib import Path
import subprocess

p=argparse.ArgumentParser()
p.add_argument('source',type=Path)
p.add_argument('packet',type=Path)
p.add_argument('--cc',default='gcc')
a=p.parse_args()
source,packet=a.source.resolve(),a.packet.resolve()
binary=packet/'scratch/freshness-probe'
commands=[
    [a.cc,'-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',
     '-I'+str(source/'include'),str(source/'src/acmp.c'),str(packet/'scripts/freshness_probe.c'),'-o',str(binary)],
    [str(binary)]
]
env=dict(os.environ,ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',UBSAN_OPTIONS='halt_on_error=1')
with (packet/'receipts/freshness-probe.log').open('w') as log:
    for command in commands:
        result=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:break
(packet/'receipts/freshness-probe.rc').write_text(str(result.returncode)+'\n')
raise SystemExit(result.returncode)
