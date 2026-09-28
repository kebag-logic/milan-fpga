"""Run donor entry points in the foreground and preserve bounded receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
scratch = Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
gates = [
    ("suites", ["./scripts/run_suites.sh"], 14400),
    ("lint", ["./scripts/lint_hdl.sh"], 3600),
    ("check", ["make", "check"], 3600),
    ("matrix", ["python3", "scripts/gen_matrix.py", "--check"], 600),
    ("nvm-figures", ["make", "-C", "tb/nvm_port", "figures"], 7200),
    ("portability", ["./syn/yosys/run.sh"], 7200),
]
results = []
for name, command, limit in gates:
    log = scratch / (name + ".log")
    with log.open("w") as stream:
        result = subprocess.run(command, cwd=repo, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=limit, check=False)
    data = log.read_bytes()
    record = dict(gate=name, command=command, rc=result.returncode,
                  bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                  scratch_log=str(log))
    if len(data) <= 200000:
        (out / (name + ".log")).write_bytes(data)
    else:
        (out / (name + "-tail.log")).write_bytes(data[-150000:])
    results.append(record)
    (out / "gate-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{name}: rc={result.returncode} bytes={len(data)}", flush=True)
    if result.returncode:
        print(data[-5000:].decode(errors="replace"), flush=True)
raise SystemExit(any(r["rc"] for r in results))
