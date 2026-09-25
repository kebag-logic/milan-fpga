import os, subprocess, sys
from pathlib import Path
p=Path(__file__).resolve().parent
env=os.environ.copy(); env['PATH']='$VALIDATION_STORAGE/400-403-a313-tools/bin:'+env['PATH'];env['PYTHONUNBUFFERED']='1'
for mode in ('sdk','absent'):
 rc=subprocess.run([sys.executable,str(p/'run_gate.py'),f'builder-{mode}-final',sys.executable,'-u',str(p/f'builder-{mode}-final.py')],env=env,timeout=14400).returncode
 if rc:sys.exit(rc)
