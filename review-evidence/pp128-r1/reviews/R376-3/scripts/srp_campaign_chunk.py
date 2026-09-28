#!/usr/bin/env python3
"""Run tb/srp_top/mutants.py in --only chunks and aggregate its coverage.

The processor runner enforces its K/L/M/N/O assertion coverage only on an
unrestricted run. A single unrestricted run exceeds one foreground call here,
so this driver runs the runner itself, unchanged, on consecutive slices of its
own MUTANTS list, and then re-applies the runner's coverage rule to the union
of the per-arm tags printed for KILLED arms.

Usage:
  srp_campaign_chunk.py <exported-tree> run <chunk-index> <chunk-size> <out-dir>
  srp_campaign_chunk.py <exported-tree> aggregate <chunk-size> <out-dir>
Needs `verilator` on PATH (the pinned tool through verilator_j8.sh).
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

tree, mode = Path(sys.argv[1]).resolve(), sys.argv[2]
spec = importlib.util.spec_from_file_location("srpm", tree / "tb/srp_top/mutants.py")
srpm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srpm)
labels = [m[0] for m in srpm.MUTANTS]

if mode == "run":
    ix, size, out = int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5])
    chunk = labels[ix * size:(ix + 1) * size]
    out.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, str(tree / "tb/srp_top/mutants.py"),
                        "--output", str(out / f"logs-{ix}"), "--only", ",".join(chunk)],
                       capture_output=True, text=True, check=False)
    (out / f"chunk-{ix}.txt").write_text(r.stdout + r.stderr + f"runner rc={r.returncode}\n")
    print(r.stdout[-1500:] + f"runner rc={r.returncode}")
    sys.exit(r.returncode)

size, out = int(sys.argv[3]), Path(sys.argv[4])
nchunks = (len(labels) + size - 1) // size
covered, killed, rcs = set(), set(), []
for ix in range(nchunks):
    text = (out / f"chunk-{ix}.txt").read_text()
    rcs.append(int(re.search(r"runner rc=(\d+)", text).group(1)))
    for label, tags in re.findall(r"^(\S+): rc=\d+ failures=\d+ KILLED tags=(.*)$", text, re.M):
        killed.add(label)
        covered.update(t for t in tags.split(",") if t)
expected = {f"{g}{i}" for g, n in [("K", 12), ("L", 4), ("M", 12), ("N", 13), ("O", 8)]
            for i in range(1, n + 1)}
missing = sorted(expected - covered)
unkilled = [l for l in labels if l not in killed]
print(f"chunks={nchunks} runner rcs={rcs}")
print(f"arms killed: {len(killed)}/{len(labels)}; not killed: {unkilled}")
print(f"assertion coverage: {len(expected) - len(missing)}/{len(expected)}; missing={missing}")
ok = not missing and not unkilled and not any(rcs)
print("AGGREGATE PASS" if ok else "AGGREGATE FAIL")
sys.exit(0 if ok else 1)
