#!/usr/bin/env python3
"""Reproduce the published consumer leg using only the exact E_SINFO splice."""
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
p = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1]).resolve()
parent = p/'scratch/parent'
pp = parent/'protocol-processor'
gen = pp/'hdl/aecp/ucode/gen_ucode.py'
cwd = parent/'tb/verilator/milan_dp'
env = dict(os.environ, TMPDIR=str(p/'scratch'), PYTHONDONTWRITEBYTECODE='1', MAKEFLAGS='-j16', VERILATOR=str(p/'scripts/limited-simulator.py'), VERILATOR_JOBS='2')
def run(tag, argv, where=cwd):
    with (p/'receipts'/f'{tag}.log').open('w') as f:
        f.write(repr(argv)+'\n'); f.flush()
        rc = subprocess.run(argv, cwd=where, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
    (p/'receipts'/f'{tag}.rc').write_text(str(rc)+'\n')
    print(tag, rc, flush=True)
    return rc
pin = subprocess.check_output(['git','show','HEAD:hdl/aecp/ucode/gen_ucode.py'],cwd=pp)
assert gen.read_bytes() == pin
pattern = re.compile(r'^place\(E_SINFO, \[\n.*?^\]\)\n(?:assert rom\[E_SINFO[^\n]*\n)*', re.M|re.S)
head_text = (root/'hdl/aecp/ucode/gen_ucode.py').read_text()
assert len(pattern.findall(head_text)) == len(pattern.findall(pin.decode())) == 1
try:
    assert run('consumer-pin-rom', [sys.executable,'-B',str(gen),'-o',str(p/'scratch/pin.hex')]) == 0
    gen.write_text(pattern.sub(lambda m: pattern.findall(head_text)[0],pin.decode()))
    (p/'receipts/consumer-applied.diff').write_bytes(subprocess.check_output(['git','diff'],cwd=pp))
    assert run('consumer-spliced-rom', [sys.executable,'-B',str(gen),'-o',str(p/'scratch/spliced.hex')]) == 0
    a=(p/'scratch/pin.hex').read_bytes(); b=(p/'scratch/spliced.hex').read_bytes()
    diff=[i for i,(x,y) in enumerate(zip(a.splitlines(),b.splitlines())) if x!=y]
    assert diff==list(range(1859,1874))
    assert hashlib.sha256(b).hexdigest()=='f9954a76e75994d3f68e4e274c68d9dddbf35ca9121f805e62264fd00e4052d6'
    (p/'receipts/consumer-rom.txt').write_text('Changed words: '+str(diff)+'\nPin SHA256: '+hashlib.sha256(a).hexdigest()+'\nSpliced SHA256: '+hashlib.sha256(b).hexdigest()+'\n')
    assert b.splitlines()[1856:1874] == (p/'scratch/head.hex').read_bytes().splitlines()[1856:1874]
    rc=run('consumer-notify', ['make','-j16','notify','VERILATOR='+env['VERILATOR'],'VERILATOR_JOBS=2'])
    if rc == 0:
        rc=run('consumer-control', [sys.executable,'-B','gsi_mutants.py','9'])
finally:
    gen.write_bytes(pin)
    run('consumer-restored-rom', [sys.executable,'-B',str(gen),'-o','ucode.hex'])
    (p/'receipts/consumer-restored.txt').write_bytes(subprocess.check_output(['git','status','--short'],cwd=pp))
raise SystemExit(rc)
