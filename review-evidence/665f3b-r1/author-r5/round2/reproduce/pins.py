import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()/'sw/firmware/ctrl/test'))
from ctrl_pin import pin_controls, proof_census
from ctrl_configs import makefiles
work=Path(os.environ['WORK']) / 'pins'
work.mkdir(exist_ok=True)
findings=proof_census()
print('census',findings,flush=True)
bad,count=pin_controls(work, makefiles())
print(f'pin controls: {count}, failed {bad}',flush=True)
raise SystemExit(bool(findings or bad))
