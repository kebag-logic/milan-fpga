import json, os, pathlib, subprocess, sys, time
out = pathlib.Path("$MANAGEMENT/2026-09-23/545-a305")
name, *cmd = sys.argv[1:]
start = time.monotonic()
with (out / (name + ".log")).open("w") as log:
    log.write("COMMAND: " + repr(cmd) + "\n")
    log.flush()
    try:
        result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=21600, check=False)
        rc = result.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    elapsed = time.monotonic() - start
    log.write(f"\nEXIT: {rc}; WALL_SECONDS: {elapsed:.3f}\n")
row = dict(name=name, command=cmd, rc=rc, seconds=round(elapsed,3))
with (out / "gates.jsonl").open("a") as f:
    f.write(json.dumps(row) + "\n")
print(json.dumps(row), flush=True)
sys.exit(rc)
