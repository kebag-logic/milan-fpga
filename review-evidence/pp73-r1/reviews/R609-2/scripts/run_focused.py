#!/usr/bin/env python3
"""Run bounded, independent review checks; every child is awaited in the foreground."""
import argparse
import concurrent.futures
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--verilator", type=Path, required=True)
    a = ap.parse_args()
    a.root, a.packet = a.root.resolve(), a.packet.resolve()
    scratch = a.packet / "scratch"
    scratch.mkdir(exist_ok=True)
    rec = a.packet / "receipts"
    rec.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
    identity = subprocess.check_output([str(a.verilator), "--version"], text=True)
    assert identity.startswith("Verilator 5.050 "), identity
    (rec / "compiler-identity.txt").write_text(identity)
    tree = scratch / "focused-head"
    tree.mkdir()
    archive = subprocess.check_output(["git", "archive", "9975764846e7e63bccf0b68a5188d5cc7f23f890"], cwd=a.root)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        tf.extractall(tree, filter="data")
    # The repository recipes request -j 0. Bound each compiler invocation to two
    # build workers; four mutation workers plus the other suite stay below 16.
    wrapper = scratch / "bounded-compiler"
    wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\n"
                       "for i in range(len(a)-1):\n"
                       " if a[i]=='-j': a[i+1]='2'\n"
                       f"os.execv({str(a.verilator)!r}, [{str(a.verilator)!r}]+a)\n")
    wrapper.chmod(0o755)
    chosen = ["q1-set-clock-source-to-gclks", "q2-set-clock-source-decoded-on-get",
              "mvu-sub-decode-other-command-type", "gdi-record-length"]
    tasks = [
        ("gate-and-docs", ["make", "-j16", "aecpcmd", "links", "matrix", "modmatrix", "params"], tree),
        ("ucpu", ["make", "-j16", "VERILATOR=" + str(wrapper)], tree / "tb/ucpu"),
        ("decode-controls", ["python3", "-B", "tb/aecp_cmds/mutants.py", "--jobs", "4",
                             "--verilator", str(wrapper), "--output", str(rec / "decode-controls"),
                             "--only", *chosen], tree),
    ]

    def run(task):
        name, cmd, cwd = task
        start = time.monotonic()
        with (rec / (name + ".log")).open("w") as log:
            log.write(json.dumps({"command": cmd, "cwd": str(cwd)}) + "\n")
            log.flush()
            p = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=2400)
        (rec / (name + ".rc")).write_text(str(p.returncode) + "\n")
        result = {"name": name, "rc": p.returncode, "seconds": round(time.monotonic() - start, 2)}
        print(json.dumps(result), flush=True)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, tasks))
    (rec / "focused-results.json").write_text(json.dumps(results, indent=2) + "\n")
    return int(any(r["rc"] for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
