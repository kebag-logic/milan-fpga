#!/usr/bin/env python3
"""Run the original 4x4 integration leg, including every GET_COUNTERS column."""
import os
from pathlib import Path
import re
import subprocess
import sys
import time
packet = Path(sys.argv[1]).resolve()
v = sys.argv[2] if len(sys.argv)>2 else '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
scratch = packet/'scratch'
root = scratch/'execution'
cmd = ['make', '-j16', '-f', 'Makefile', '-f', str(packet/'scripts/nxn.mk'),
       'reviewer-nxn', 'VERILATOR_JOBS=4', 'VERILATOR='+v]
start = time.monotonic()
with (scratch/'datapath-nxn.raw.log').open('w') as log:
    log.write('COMMAND: '+repr(cmd)+'\n'); log.flush()
    rc = subprocess.run(cmd, cwd=root/'tb/verilator/milan_dp',
                        env=dict(os.environ, TMPDIR=str(scratch)),
                        stdout=log, stderr=subprocess.STDOUT).returncode
    log.write(f'\nEXIT_STATUS={rc}\nELAPSED_SECONDS={time.monotonic()-start:.3f}\n')
text = (scratch/'datapath-nxn.raw.log').read_text()
text = text.replace(str(scratch), '<scratch>').replace(str(packet), '<packet>')
text = re.sub(r'/home/[^/\s]+/[^\s\"\']*?(?=[\s\"\']|$)', '<compiler-runtime-path>', text)
(packet/'receipts/datapath-nxn.log').write_text(text)
(packet/'receipts/datapath-nxn.rc').write_text(str(rc)+'\n')
print('datapath-nxn rc',rc,'elapsed',round(time.monotonic()-start,1),flush=True)
raise SystemExit(rc)
