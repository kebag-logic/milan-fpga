#!/usr/bin/env python3
"""Run focused gates concurrently, wait in the foreground, retain individual logs/rc.

Usage: python3 run_focused.py --repo /path/to/clone --packet /path/to/packet \
  --compiler /path/to/pinned-verilator-5.050/verilator --jobs 4
No synthesis or full simulation bank is run.
"""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--compiler", type=Path, required=True)
    p.add_argument("--jobs", type=int, default=4)
    a = p.parse_args()
    assert 1 <= a.jobs <= 4
    repo, packet, compiler = a.repo.resolve(), a.packet.resolve(), a.compiler.absolute()
    gates = packet / "receipts" / "resumed_gates"
    gates.mkdir(parents=True, exist_ok=True)
    tmp = packet / "scratch" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PATH=str(compiler.parent) + os.pathsep + os.environ["PATH"],
               TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
    identity = subprocess.check_output([str(compiler), "--version"], env=env, text=True)
    assert "Verilator 5.050" in identity, identity
    (gates / "compiler_identity.txt").write_text(str(compiler) + "\n" + identity)
    commands = [
        ("contract", ["make", "-j16", "contract"]),
        ("lint", ["make", "-j16", "lint"]),
        ("docs", ["make", "-j16", "docs"]),
        ("ooc_static", [sys.executable, "syn/ooc/check_ooc_clock.py"]),
        ("probes", [sys.executable, str(packet / "review_probes.py"), "--repo", str(repo),
                    "--packet", str(packet), "--jobs", "4"]),
    ]

    def run(item):
        name, command = item
        with (gates / (name + ".log")).open("w") as log:
            result = subprocess.run(command, cwd=repo, env=env, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=540)
        (gates / (name + ".rc")).write_text(str(result.returncode) + "\n")
        return name, result.returncode

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results = list(pool.map(run, commands))
    for name, rc in results:
        print(f"{name}: rc {rc}")
    return int(any(rc != 0 for _, rc in results))


if __name__ == "__main__":
    sys.exit(main())
