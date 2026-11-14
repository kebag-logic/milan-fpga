#!/usr/bin/env python3
"""Run from the exact-head checkout; requires the public archive commit locally.

Needs repository Python dependencies, host C/C++ compilers and test libraries.
No full banks, target simulations, network writes or source edits are performed.
"""
import io
from pathlib import Path
import subprocess
import sys
import tarfile

OUT=Path(__file__).resolve().parent
archive='f3320c19d0d394ee7dd4a835e81c7a390df3fedb'
scratch=OUT/'scratch'
scratch.mkdir(exist_ok=True)
data=subprocess.check_output(['git','archive',archive,'review-evidence/894-r1/author-r11'])
with tarfile.open(fileobj=io.BytesIO(data)) as tar:
    tar.extractall(scratch,filter='data')
for script in ('run_checks.py','probe_maps.py','audit_evidence.py','verify_checkout.py'):
    subprocess.run([sys.executable,'-B',str(OUT/script)],check=True)
cmd=[sys.executable,'-B','tb/verilator/ctrl_service_budget/flip_grade.py','--check','--point','8x8/2if']
with (OUT/'receipts/flip-8x8.log').open('w') as log:
    result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
(OUT/'receipts/flip-8x8.rc').write_text(str(result.returncode)+'\n')
assert result.returncode==1,'The reported 8x8 point is expected to fail.'
