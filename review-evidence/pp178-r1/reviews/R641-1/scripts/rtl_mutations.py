#!/usr/bin/env python3
"""Run only the two configuration-related RTL controls; no complete bank."""
import os,pathlib,subprocess,sys
packet=pathlib.Path(__file__).resolve().parents[1]
source=pathlib.Path(sys.argv[1]).resolve()
env=os.environ.copy();env['TMPDIR']=str(packet/'scratch');env['PYTHONDONTWRITEBYTECODE']='1';env['MAKEFLAGS']='-j16'
with (packet/'receipts/rtl-mutations.log').open('w') as f:
 rc=subprocess.run([sys.executable,'-B',str(source/'tb/pp_top/notify_mutants.py'),'--output',str(packet/'receipts/rtl-mutations'),'--verilator',str(packet/'scripts/simulator.py'),'--jobs','2','--only','configuration_running_route_dropped','requester_not_excluded'],env=env,stdout=f,stderr=subprocess.STDOUT).returncode
(packet/'receipts/rtl-mutations.rc').write_text(str(rc)+'\n')
print('RTL configuration mutation campaign rc:',rc)
sys.exit(rc)
