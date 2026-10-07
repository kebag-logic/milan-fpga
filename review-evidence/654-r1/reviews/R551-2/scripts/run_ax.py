#!/usr/bin/env python3
"""Reproduce raw equality for both product shapes in isolated clones."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
python = sys.argv[2]
packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TMPDIR=str(scratch),
           OMP_NUM_THREADS="1", MAKEFLAGS="-j16")
installed = subprocess.check_output([python, "-c", "import pythondata_cpu_vexiiriscv as p;print(p.data_location)"], env=env, text=True).strip()
data = scratch / "vex-data"
with (scratch / "ax-prepare.log").open("w") as log:
    subprocess.run(["cp", "-a", "--reflink=auto", installed, str(data)], check=True, stdout=log, stderr=log)
    for shape in ("ax7101_1x1_tdm8", "ax7101_8x8"):
        clone = scratch / ("ax-" + shape)
        subprocess.run(["git", "clone", "--shared", "--no-hardlinks", str(root), str(clone)], check=True, stdout=log, stderr=log)
        for sub in ("third_party/verilog-axis", "protocol-processor", "gptp-processor"):
            subprocess.run(["git", "-C", str(clone), "-c", "protocol.file.allow=always", "-c",
                            f"submodule.{sub}.url={root / sub}", "submodule", "update", "--init", sub],
                           check=True, stdout=log, stderr=log)

def campaign(shape):
    clone = scratch / ("ax-" + shape)
    measure = scratch / ("measure-" + shape)
    runenv = dict(env, MEASURE_DIR=str(measure), VEX_DATA_DIR=str(data))
    for phase in ("baseline-fixed", "candidate-fixed"):
        name = "ax-" + shape + "-" + phase
        with (scratch / (name + ".raw.log")).open("w") as log:
            run = subprocess.run([python, str(packet / "scripts/export_compare.py"), phase, shape],
                                 cwd=clone, env=runenv, stdout=log, stderr=subprocess.STDOUT, timeout=300)
        (packet / "receipts" / (name + ".rc")).write_text(str(run.returncode) + "\n")
        print(name, run.returncode, flush=True)
        assert run.returncode == 0, name
    a = json.loads((measure / ("baseline-fixed-" + shape + ".json")).read_text())["files"]
    b = json.loads((measure / ("candidate-fixed-" + shape + ".json")).read_text())["files"]
    assert a == b and len(a) == 32
    compared = []
    for path, info in a.items():
        first = measure / "snapshots/baseline-fixed" / shape / path
        second = measure / "snapshots/candidate-fixed" / shape / path
        assert first.read_bytes() == second.read_bytes(), path
        compared.append({"path": path, **info, "byte_identical": True})
    return {"config": shape, "files": compared, "count": len(compared), "raw_equal": True}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(campaign, ("ax7101_1x1_tdm8", "ax7101_8x8")))
(packet / "receipts/ax-equivalence.json").write_text(json.dumps(results, indent=2) + "\n")
print("PASS: both AX7101 configurations retain 32/32 raw artifacts")
