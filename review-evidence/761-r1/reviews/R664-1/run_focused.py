#!/usr/bin/env python3
"""Run the two changed receiver campaigns concurrently in a disposable tree.

Usage: python3 run_focused.py SOURCE_ROOT PINNED_SIMULATOR
All builds stay below this packet's scratch directory. No source is edited.
"""
import concurrent.futures
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile

packet = Path(__file__).resolve().parent
source = Path(sys.argv[1]).resolve()
simulator = Path(sys.argv[2]).resolve()
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
archive = subprocess.check_output(["git", "-C", str(source), "archive", "HEAD", "hdl", "tb", "scripts"])
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
    tf.extractall(scratch, filter="data")
(scratch / "tmp").mkdir(exist_ok=True)
wrapper = scratch / "bounded-simulator"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\n"
                   "for i,x in enumerate(a[:-1]):\n    if x == '-j': a[i+1]='4'\n"
                   f"os.execv({str(simulator)!r}, [{str(simulator)!r}]+a)\n")
wrapper.chmod(0o755)
env = dict(os.environ, VERILATOR=str(wrapper), TMPDIR=str(scratch / "tmp"), MAKEFLAGS="-j16")

def run(name, relative, args):
    with (packet / (name + ".log")).open("w") as log:
        log.write("exact head: " + subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True))
        log.write("command: " + " ".join(args) + "\n")
        log.flush()
        result = subprocess.run(args, cwd=scratch / relative, env=env, stdout=log, stderr=subprocess.STDOUT)
    (packet / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(name, "rc", result.returncode, flush=True)
    return result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(run, "receiver-lockstep-campaign", "tb/verilator/avtp_rxmon", [sys.executable, "lockstep_mutants.py"]),
            pool.submit(run, "crf-counter-campaign", "tb/verilator/crf_rx", [sys.executable, "mutants.py"])]
    results = [f.result() for f in jobs]
sys.exit(any(results))
