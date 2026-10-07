#!/usr/bin/env python3
"""Validate mailbox/co-simulation from tracked inputs in a disposable export."""
import argparse, os, subprocess, sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--verilator',type=Path,required=True);a=ap.parse_args()
p=Path(__file__).resolve().parent;work=p/'scratch/mailbox';work.mkdir(exist_ok=True)
version=subprocess.check_output([str(a.verilator),'--version'],text=True);assert 'Verilator 5.050' in version
archive=p/'scratch/mailbox.tar'
subprocess.run(['git','-C',str(a.repo),'archive','--format=tar','--output',str(archive),'HEAD','tb/verilator/mbx','tb/common','hdl/milan/mailbox','sw/firmware/ctrl','sw/firmware/ctrl_nvm','sw/mailbox'],check=True)
subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
env=dict(os.environ,VERILATOR=str(a.verilator),TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1')
with (p/'mailbox.log').open('w') as log:
    log.write(version);log.flush()
    r=subprocess.run(['make','-C',str(work/'tb/verilator/mbx'),'-j16','VBUILD_JOBS=1'],stdout=log,stderr=subprocess.STDOUT,env=env,timeout=580)
(p/'mailbox.rc').write_text(str(r.returncode)+'\n');print('mailbox rc',r.returncode)
sys.exit(r.returncode)
