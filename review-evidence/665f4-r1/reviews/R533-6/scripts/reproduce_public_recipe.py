#!/usr/bin/env python3
"""Reproduce the published mailbox export failure without running a build."""
import json
import subprocess
import sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parents[1]
cmd=['git','-C',str(repo),'archive','--format=tar','--output',str(packet/'scratch/public-mailbox-inputs.tar'),
     'HEAD','tb/verilator/mbx','tb/common','hdl/milan/mailbox','sw/firmware/ctrl','sw/mailbox','scripts/mutant_run.py']
r=subprocess.run(cmd,capture_output=True,text=True)
print(r.stdout+r.stderr,end='')
print('export exit:',r.returncode)
(packet/'receipts/public-recipe-reproduction.json').write_text(json.dumps({'argv':cmd,'rc':r.returncode,
 'output':r.stdout+r.stderr,'expected_missing_path':'scripts/mutant_run.py'},indent=2)+'\n')
raise SystemExit(0 if r.returncode==128 and 'scripts/mutant_run.py' in r.stderr else 1)
