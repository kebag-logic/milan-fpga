#!/usr/bin/env python3
"""Compile the untouched core and independent wire probe, then retain its result."""
from pathlib import Path
import subprocess
import sys
p=Path(__file__).resolve().parent
(p/"scratch").mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode=True
r=Path(sys.argv[1]).resolve()
cmd=['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-I'+str(r/'sw/firmware/ctrl/gptp'),str(p/'probe_protocol.c'),str(r/'sw/firmware/ctrl/gptp/gptp.c'),'-o',str(p/'scratch/probe_protocol')]
with (p/'protocol.log').open('w') as log:
 log.write('COMMAND: '+repr(cmd)+'\n');log.flush()
 subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
 result=subprocess.run([str(p/'scratch/probe_protocol')],stdout=log,stderr=subprocess.STDOUT)
(p/'protocol.rc').write_text(str(result.returncode)+'\n')
print((p/'protocol.log').read_text())
sys.exit(result.returncode)
