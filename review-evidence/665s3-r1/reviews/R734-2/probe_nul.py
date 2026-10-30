#!/usr/bin/env python3
"""Repeat the published malformed-command probe on fixed and reverted source copies."""
from pathlib import Path
import os
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
work = packet/'scratch/nul'
work.mkdir(parents=True,exist_ok=True)
plat = root/'sw/firmware/ctrl/plat'
source = (plat/'ctrl_plat_console.c').read_text()
guard = "command[n] != '\\0' && "
assert source.count(guard) == 1
(work/'reverted.c').write_text(source.replace(guard,''))
env = dict(os.environ, ASAN_OPTIONS='abort_on_error=1')
for label, src in [('fixed',plat/'ctrl_plat_console.c'),('reverted',work/'reverted.c')]:
    cmd = ['gcc','-std=c11','-g','-O1','-fsanitize=address','-fno-omit-frame-pointer',
           '-no-pie','-I'+str(plat),str(packet/'r733_console_nul.c'),str(src),
           str(plat/'ctrl_plat_csr.c'),'-o',str(work/label)]
    print(repr(cmd),flush=True)
    subprocess.run(cmd,check=True)
    result = subprocess.run([str(work/label)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print(f'{label} rc={result.returncode}\n'+result.stdout.decode(),flush=True)
    if label == 'fixed':
        assert result.returncode == 0
    else:
        assert result.returncode != 0 and b'global-buffer-overflow' in result.stdout
print('PASS: fixed source is clean and the revert trips AddressSanitizer')
