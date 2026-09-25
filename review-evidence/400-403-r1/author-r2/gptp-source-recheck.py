import json, os, shlex, subprocess, sys
from pathlib import Path
p=Path(__file__).resolve().parent
commands=json.loads((p/'milan-dp-commands.json').read_text())
env=os.environ.copy();env['PATH']='$VALIDATION_STORAGE/400-403-a313-tools/bin:'+env['PATH']
for i in (3,4):
 rc=subprocess.run([sys.executable,str(p/'run_gate.py'),f'milan-dp-final-{i:02}',*shlex.split(commands[i])],env=env,cwd='$LANES/400-403-declaration-truth/tb/verilator/milan_dp',timeout=14400).returncode
 if rc:sys.exit(rc)
