#!/usr/bin/env python3
"""Scoped fabric test, RV32 size comparison, and YAML physical-removal control."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

p=argparse.ArgumentParser()
p.add_argument('source',type=Path)
p.add_argument('packet',type=Path)
p.add_argument('--verilator',required=True)
a=p.parse_args()
source,packet=a.source.resolve(),a.packet.resolve()

def command(name,argv,cwd=source):
    with (packet/'receipts'/f'{name}.log').open('w') as log:
        result=subprocess.run(argv,cwd=cwd,stdout=log,stderr=subprocess.STDOUT)
    (packet/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
    print(name,result.returncode,flush=True)
    return result.returncode

def archive(ref,target):
    target.mkdir(exist_ok=True)
    data=subprocess.check_output(['git','archive',ref],cwd=source)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(target,filter='data')

def sizes():
    root=packet/'scratch/base'
    archive('1ba273540abbdf51ea5d235c0a7e81c0bcb5d475',root)
    build=packet/'scratch/rv32-base'
    rc=command('rv32-base',['python3','scripts/baremetal.py','--work',str(build),'--jobs','2'],root)
    if rc: return
    rows=[]
    for kind in ['debug','release']:
        counts={}
        for label,directory in [('base',build),('head',packet/'scratch/rv32')]:
            target=packet/'scratch'/f'{label}-{kind}.bin'
            subprocess.run(['riscv64-elf-objcopy','-O','binary',str(directory/kind/'rv32_smoke.elf'),str(target)],check=True)
            counts[label]=target.stat().st_size
        rows.append({'configuration':kind,**counts,'delta':counts['head']-counts['base']})
    (packet/'receipts/rv32-size.json').write_text(json.dumps(rows,indent=2)+'\n')
    command('base-static-analysis',['python3','scripts/static_analysis.py'],root)

def rtl():
    directory=packet/'scratch/pp/tb/acmp_talker'
    flags='--cc --exe --build -j 8 --top-module KL_acmp_talker -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -I'+str(directory)+' -Wall -Wextra"'
    command('rtl-talker',['make','-j16','run','VERILATOR='+a.verilator,'VFLAGS='+flags],directory)

def yaml():
    root=packet/'scratch/yaml-control'
    archive('HEAD',root)
    f=root/'scripts/entity_yaml.py'
    text=f.read_text()
    old="integer(acmp['da_fresh_ms'], 15000, 15000, 'acmp.da_fresh_ms')"
    assert text.count(old)==1
    f.write_text(text.replace(old,"integer(acmp['da_fresh_ms'], 15000, 15001, 'acmp.da_fresh_ms')"))
    rc=command('yaml-range-caught',['python3','scripts/entity_selftest.py','--work',str(root/'caught')],root)
    assert rc==1
    f=root/'scripts/entity_selftest.py'
    text=f.read_text()
    text,n=re.subn(r'    def test_dafresh_configuration\(self\):.*?(?=    def test_missing_golden_file)', '',text,flags=re.S)
    assert n==1
    f.write_text(text)
    rc=command('yaml-range-removed',['python3','scripts/entity_selftest.py','--work',str(root/'removed')],root)
    assert rc==0

with ThreadPoolExecutor(max_workers=3) as pool:
    futures=[pool.submit(fn) for fn in [sizes,rtl,yaml]]
    for f in futures:f.result()
