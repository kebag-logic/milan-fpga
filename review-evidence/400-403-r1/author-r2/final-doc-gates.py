import json, subprocess, sys
from pathlib import Path
p=Path(__file__).resolve().parent
for name,cmd in json.loads((p/'final-doc-gates.json').read_text()):
 rc=subprocess.run([sys.executable,str(p/'run_gate.py'),name,*cmd],timeout=14400).returncode
 if rc:sys.exit(rc)
