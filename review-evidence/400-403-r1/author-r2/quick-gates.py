import json, os, subprocess, sys
from pathlib import Path
p=Path(__file__).resolve().parent
env=os.environ.copy()
env["PATH"]="$VALIDATION_TOOLS/verilator-v5.050/bin:"+env["PATH"]
failed=[]
for name,cmd in json.loads((p/"quick-gates.json").read_text()):
 r=subprocess.run([sys.executable,"-u",str(p/"run_gate.py"),name,*cmd],env=env,timeout=14400)
 if r.returncode: failed.append(name)
print("FAILED",failed,flush=True)
sys.exit(bool(failed))
