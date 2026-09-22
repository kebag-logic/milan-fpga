#!/usr/bin/env python3
"""Run the original leg with its otherwise identical flags and eight build jobs."""
from pathlib import Path
import subprocess
import sys

root=Path('$VALIDATION_STORAGE/reviews/r240-372-r1')
here=root/'tb/verilator/ptp_ts'
make=(here/'Makefile').read_text().replace('\\\n',' ')
flags=next(s.split('=',1)[1].strip() for s in make.splitlines() if s.startswith('VFLAGS ='))
assert flags.count('-j 0')==1
flags=flags.replace('-j 0','-j 8')
argv=['rtk','proxy','make','-C',str(here),'run',
      'VERILATOR=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator',
      'VFLAGS='+flags]
print(repr(argv),flush=True)
sys.exit(subprocess.run(argv,cwd=root).returncode)
