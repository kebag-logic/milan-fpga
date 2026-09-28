"""Run a foreground command and retain a bounded receipt."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

name = sys.argv[1]
command = sys.argv[2:]
out = Path(__file__).resolve().parent
scratch = Path("$VALIDATION_STORAGE/606-a412")
log = scratch / (name + ".log")
env = dict(os.environ)
env["PATH"] = (str(scratch / "bin") + ":$WORKSPACE_HOME/litex-milan/venv/bin:"
               "$WORKSPACE_HOME/br-milan-rv32/host/bin:" + env["PATH"])
env["XVLOG"] = "$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin/xvlog"
env["PYTHONUNBUFFERED"] = "1"
env["PYTHONHASHSEED"] = "0"
sub = Path.cwd() / "protocol-processor"
if (sub / ".git").exists():
    top = subprocess.check_output(["git", "-C", str(sub), "rev-parse", "--show-toplevel"], text=True).strip()
    if Path(top).resolve() != sub.resolve():
        raise RuntimeError("processor directory is not its repository root")
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
with log.open("w") as stream:
    result = subprocess.run(command, env=env, stdout=stream, stderr=subprocess.STDOUT,
                            timeout=14400, check=False)
data = log.read_bytes()
record = dict(command=command, cwd=str(Path.cwd()), head=head, rc=result.returncode,
              bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), log=str(log))
(out / (name + ".json")).write_text(json.dumps(record, indent=2) + "\n")
if len(data) <= 200000:
    (out / (name + ".log")).write_bytes(data)
print(json.dumps(record), flush=True)
print(data[-6000:].decode(errors="replace"), flush=True)
raise SystemExit(result.returncode)
