#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Probe the fabric freshness expiry at 14999 and 15000 ms."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--processor',type=Path,required=True)
p.add_argument('--work',type=Path,required=True)
p.add_argument('--simulator',required=True)
p.add_argument('--jobs',type=int,default=2)
a=p.parse_args()
a.work.mkdir(parents=True,exist_ok=True)
version=subprocess.check_output([a.simulator,'--version'],text=True)
assert '5.050' in version
flags='--cc --exe --build -j 4 --top-module KL_acmp_talker -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'

def one(age):
    directory=a.work/str(age)
    tree=directory/'processor'
    shutil.copytree(a.processor,tree,ignore=shutil.ignore_patterns('obj_dir'),dirs_exist_ok=True)
    source=tree/'tb/acmp_talker/sim_main.cpp'
    text=source.read_text()
    anchor='d->now_ms_i = t2 + T_DAFRESH + 1;'
    assert text.count(anchor)==1
    source.write_text(text.replace(anchor,'d->now_ms_i = t2 + '+str(age)+'u;'))
    with (directory/'run.log').open('w') as log:
        rc=subprocess.run(['make','-j16','run','VERILATOR='+a.simulator,'VFLAGS='+flags],cwd=source.parent,stdout=log,stderr=subprocess.STDOUT).returncode
    (directory/'run.rc').write_text(str(rc)+'\n')
    output=(directory/'run.log').read_text()
    if age==15000:
        assert rc==0 and '1342 PASS, 0 FAIL' in output
    else:
        assert rc!=0 and 'D2 freshness lapse' in output and 'FAIL' in output
    return dict(age_ms=age,rc=rc,expected='closed' if age==15000 else 'open; deliberately expecting closure is rejected',verified=True)

with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    rows=list(pool.map(one,[14999,15000]))
(a.work/'results.json').write_text(json.dumps(dict(version=version.strip(),cases=rows),indent=2)+'\n')
print(json.dumps(rows,indent=2))
