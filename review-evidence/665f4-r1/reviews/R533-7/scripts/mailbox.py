#!/usr/bin/env python3
"""Export exact tracked mailbox inputs and run the two bus controls."""
import argparse
import subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('repo',type=Path)
p.add_argument('--hdl',required=True)
a=p.parse_args()
packet=Path(__file__).resolve().parents[1]
scratch=packet/'scratch/mailbox'
scratch.mkdir(exist_ok=True)
version=subprocess.check_output([a.hdl,'--version'],text=True)
print(version,flush=True)
assert '5.050' in version and 'rev v5.050' in version
archive=packet/'scratch/mailbox.tar'
with archive.open('wb') as out:
    subprocess.run(['git','-C',str(a.repo),'archive','HEAD','tb/verilator/mbx','tb/common',
                    'hdl/milan/mailbox','sw/firmware/ctrl','sw/mailbox'],
                   stdout=out,check=True)
subprocess.run(['tar','-xf',str(archive),'-C',str(scratch)],check=True)
subprocess.run(['make','-C',str(scratch/'tb/verilator/mbx'),'-j16',
                'VBUILD_JOBS=2','VERILATOR='+a.hdl],check=True)
