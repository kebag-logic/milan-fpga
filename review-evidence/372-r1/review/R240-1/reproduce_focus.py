#!/usr/bin/env python3
"""Bounded replay of all three focused suite legs; no source edits.

Invoke through rtk proxy python3, optionally using run_receipt.py to capture it.
This replay helper is supplied for reproduction; the original measured commands
are in focused-default.json and legacy-bounded.json.
"""
import os
from pathlib import Path
import subprocess
import sys

root=Path('$VALIDATION_STORAGE/reviews/r240-372-r1')
here=root/'tb/verilator/ptp_ts'
make=(here/'Makefile').read_text().replace('\\\n',' ')
flags=next(s.split('=',1)[1].strip() for s in make.splitlines() if s.startswith('VFLAGS ='))
assert flags.count('-j 0')==1
flags=flags.replace('-j 0','-j 8')
argv=['rtk','proxy','make','-C',str(here),
      'VERILATOR=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator',
      'VFLAGS='+flags]
print(repr(argv),flush=True)
sys.exit(subprocess.run(argv,cwd=root,env=dict(os.environ,MAKEFLAGS='-j1',PYTHONDONTWRITEBYTECODE='1')).returncode)
