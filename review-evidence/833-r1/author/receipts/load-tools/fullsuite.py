#!/usr/bin/env python3
"""usage: fullsuite.py <out> <rounds>  Scratch only. Each round runs the real gptp_shadow suite (make, so lifecycle then mutants) in 5 before clones
and 5 after clones at the same moment; those 10 real builds are the load. One log and one rc per run; the summary is the rc files."""
import os, subprocess, sys, time
from pathlib import Path
out, rounds = Path(sys.argv[1]), int(sys.argv[2])
S = Path("$VALIDATION_STORAGE/833-a726/full")
env = dict(os.environ, TMPDIR="$VALIDATION_STORAGE/833-a726/tmp", PYTHONDONTWRITEBYTECODE="1", MAKEFLAGS="-j2 --no-print-directory", VERILATOR_JOBS="2",
           VERILATOR="$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", PYTHONHASHSEED="0",
           PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin")
n = 0
for r in range(rounds):
    procs = []; began = time.monotonic(); loadavg = Path("/proc/loadavg").read_text().strip()
    for name in ("before", "after"):
        (out / name).mkdir(parents=True, exist_ok=True)
        for i in range(5):
            tree = S / f"{name}-{i}"
            subprocess.run(["git", "-C", str(tree), "clean", "-qfdx", "-e", "gptp-processor", "-e", "third_party", "-e", "protocol-processor"], check=True)
            head = subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            f = (out / name / f"{n + i:03d}.log").open("w")
            f.write(f"# tree {name} head {head} concurrent 10 loadavg-before {loadavg}\n# make -C tb/verilator/gptp_shadow\n"); f.flush()
            procs.append((name, n + i, subprocess.Popen(["make", "-C", "tb/verilator/gptp_shadow"], cwd=tree, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL), f))
    for name, k, p, f in procs:
        rc = p.wait(); f.close(); (out / name / f"{k:03d}.rc").write_text(f"{rc}\n")
    n += 5
    print(f"round {r}: {time.monotonic()-began:.0f}s rcs " + " ".join(f"{a[0]}{k}={p.returncode}" for a, k, p, f in procs), flush=True)
print("done")
