#!/usr/bin/env python3
"""Build the shared mailbox harness in a disposable source export.

Usage: python3 mailbox_check.py CHECKOUT PACKET PINNED_VERILATOR
The outer make uses -j16; each of its three independent builds uses two
compiler jobs, keeping this suite to six alongside the firmware campaigns.
"""
import hashlib
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile

root, packet, simulator = map(lambda p: Path(p).resolve(),sys.argv[1:4])
work=packet/'scratch/mailbox'
work.mkdir(parents=True,exist_ok=True)
version=subprocess.check_output([str(simulator),'--version'],text=True)
assert 'Verilator 5.050' in version
print(version.strip(),flush=True)
print('executable sha256:',hashlib.sha256(simulator.read_bytes()).hexdigest(),flush=True)
archive=packet/'scratch/mailbox-source.tar'
with archive.open('wb') as f:
    subprocess.run(['git','-C',str(root),'archive','HEAD','hdl/milan/mailbox','tb/verilator/mbx',
                    'tb/common','sw/firmware/ctrl'],stdout=f,check=True)
with tarfile.open(archive) as t:
    t.extractall(work,filter='data')
cwd=work/'tb/verilator/mbx'
env=dict(os.environ, TMPDIR=str(packet/'scratch'), PYTHONDONTWRITEBYTECODE='1', PYTHON_CPU_COUNT='2')
flags=subprocess.check_output(['make','-s','print-vflags',f'VERILATOR={simulator}'],cwd=cwd,text=True).splitlines()
assert flags[0]==str(simulator)
flags=flags[1:]
assert flags[flags.index('-j')+1]=='0'
flags[flags.index('-j')+1]='2'
command=['make','-j16',f'VERILATOR={simulator}','VFLAGS='+shlex.join(flags)]
r=subprocess.run(command,cwd=cwd,env=env,check=False)
print('mailbox scoped gate rc:',r.returncode,flush=True)
raise SystemExit(r.returncode)
