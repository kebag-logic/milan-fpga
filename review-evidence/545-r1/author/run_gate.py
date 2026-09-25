import json, os, subprocess, sys, time
from pathlib import Path
out = Path(__file__).resolve().parent
name, *cmd = sys.argv[1:]
os.environ["PATH"] = "$VALIDATION_TOOLS/verilator-v5.050/bin:" + os.environ["PATH"]
os.environ["VERILATOR"] = "$VALIDATION_TOOLS/verilator-v5.050/bin/verilator"
os.environ["VERILATOR_JOBS"] = "8"
os.environ["PYTHONPATH"] = "$VALIDATION_TOOLS/md-venv-40cdefe08ebd/lib/python3.14/site-packages"
start = time.time()
with (out / (name + ".log")).open("w") as log:
    proc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=14400)
row = {"name": name, "cwd": os.getcwd(), "command": cmd, "rc": proc.returncode, "seconds": round(time.time()-start, 2)}
with (out / "gates.jsonl").open("a") as f:
    f.write(json.dumps(row) + "\n")
print(json.dumps(row), flush=True)
print("".join((out / (name + ".log")).read_text(errors="replace").splitlines(keepends=True)[-18:]))
sys.exit(proc.returncode)
