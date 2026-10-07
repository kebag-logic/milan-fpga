#!/usr/bin/env python3
from public_text import toolchain_paths
"""Remove only the parent drain fix in the disposable clone; require its named failure."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
packet=Path(__file__).resolve().parent;scratch=packet/'scratch';tree=scratch/'parent-notify'
path=tree/'tb/verilator/milan_dp/sim_nxn.cpp';original=path.read_bytes()
before=b'c < cyc || (!cur.empty() && c < cyc + 2048)';assert original.count(before)==1
try:
    path.write_bytes(original.replace(before,b'c < cyc'))
    env=dict(os.environ,TMPDIR=str(scratch),VERILATOR=sys.argv[1],VERILATOR_JOBS='4',PYTHONDONTWRITEBYTECODE='1')
    r=subprocess.run(['make','-j16','notify','VERILATOR_JOBS=4'],cwd=path.parent,env=env,capture_output=True)
    raw=(r.stdout+r.stderr).replace(str(scratch).encode(),b'$SCRATCH').replace(sys.argv[1].encode(),b'$PINNED_VERILATOR')
    raw=toolchain_paths(raw)
    (packet/'parent-drain-control.log').write_bytes(raw);(packet/'parent-drain-control.rc').write_text(str(r.returncode)+'\n')
    lines=[line for line in raw.decode().splitlines() if '[FAIL]' in line or 'failures:' in line or 'RESULT:' in line]
    assert r.returncode==2 and any('[NOTIFY-CRF]' in line and 'nor to A' in line for line in lines),lines
    print(json.dumps({'only_change':'sim_nxn.cpp drain_tx loop bound restored to previous implementation','rc':r.returncode,'expected':2,'failure_lines':lines,'log_sha256':hashlib.sha256(raw).hexdigest()},indent=2))
finally:
    path.write_bytes(original)
