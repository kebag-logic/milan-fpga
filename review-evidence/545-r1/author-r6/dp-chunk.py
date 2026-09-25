import importlib.util
import json
from pathlib import Path
import sys
out=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("g",out/"run-gates.py")
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
commands=json.loads((out/"dp-commands.json").read_text())
start,end=map(int,sys.argv[1:])
for i in range(start,end+1):
    rc=g.run(f"dp-{i:02d}",["taskset","-c","10-15"]+commands[i-1],g.ROOT/"tb/verilator/milan_dp")
    if rc:
        sys.exit(rc)
print(f"CHUNK {start}-{end}: all rc 0",flush=True)
