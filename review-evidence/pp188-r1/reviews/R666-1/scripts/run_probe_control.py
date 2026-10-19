#!/usr/bin/env python3
"""Run the same compiled probe with transmission available as a positive control."""
import os
from pathlib import Path
import subprocess
import sys

packet=Path(sys.argv[1])
with (packet/'receipts/probe-pp_top-no-stall.log').open('w') as log:
    rc=subprocess.run(['./obj_dir/Vpp_top_sim','--acmp-only'],
        cwd=packet/'scratch/probes/tb/pp_top',
        env=dict(os.environ,REVIEW_NO_TX_STALL='1'),stdout=log,
        stderr=subprocess.STDOUT).returncode
(packet/'receipts/probe-pp_top-no-stall.rc').write_text(str(rc)+'\n')
print('no-stall control rc',rc)
sys.exit(rc)
