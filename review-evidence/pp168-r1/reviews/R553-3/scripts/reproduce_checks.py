#!/usr/bin/env python3
"""Repeat the two required foreground checks with logs; scratch owns dependencies.
Usage: reproduce_checks.py CHECKOUT PACKET
Requires the repository's diagram renderer in PATH and a Python package index.
"""
import concurrent.futures, os, shutil, subprocess, sys
from pathlib import Path
checkout, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
scratch = packet / "scratch"
scratch.mkdir(parents=True, exist_ok=True)
venv = scratch / "docs-venv"
assert shutil.which("mmdc"), "Install/provide mmdc before running documentation checks"
if not (venv / "bin/python3").exists():
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
subprocess.run([str(venv/"bin/python3"), "-m", "pip", "install",
    "wavedrom==2.0.3.post3", "svgwrite==1.4.3", "six==1.17.0", "pyyaml==6.0.3"], check=True)
env = dict(os.environ, PATH=str(venv/"bin") + os.pathsep + os.environ["PATH"],
    TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
capture = Path(__file__).with_name("capture.py")
def one(item):
    label, command = item
    return subprocess.run([sys.executable, str(capture), str(packet), label,
        str(checkout), *command], env=env).returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    statuses = list(pool.map(one, [("make-check-reproduced", ["make", "-j16", "check"]),
        ("matrix-check-reproduced", ["python3", "scripts/gen_matrix.py", "--check"])]))
subprocess.run([sys.executable, str(capture), str(packet), "integrity-reproduced",
    str(checkout), sys.executable, str(Path(__file__).with_name("verify_checkout.py")), str(checkout)], check=True)
sys.exit(0 if statuses == [0, 0] else 1)
