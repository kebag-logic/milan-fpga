#!/usr/bin/env python3
"""Foreground coordinator: independent focused runs concurrently, bounded to 12 workers."""
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
receipts = packet / "receipts"
pin = Path(sys.argv[2]).resolve()
version = subprocess.check_output([str(pin), "--version"], text=True).strip()
assert version.startswith("Verilator 5.050 "), version
(receipts / "compiler-identity.txt").write_text(version + "\n")
os.environ["PINNED_VERILATOR"] = str(pin)
os.environ["TMPDIR"] = str(scratch)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["MAKEFLAGS"] = "-j16"
wrapper = packet / "scripts/bounded_verilator.py"
wrapper.chmod(0o755)
mutants = ["avb_domain_term_dropped", "avb_link_term_dropped", "asp_takes_domain",
           "avb_notify_not_interface", "domain_same_readopted", "adoption_no_strobe",
           "revert_strobes_at_defaults", "registry_never_claims", "restore_never_done"]

def execute(name, command, cwd):
    start = time.monotonic()
    with (receipts / (name + ".log")).open("w") as log:
        rc = subprocess.run(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
    (receipts / (name + ".rc")).write_text(str(rc) + "\n")
    print(json.dumps({"task": name, "rc": rc, "seconds": round(time.monotonic() - start, 2)}), flush=True)
    return rc

def campaign():
    return execute("domain-campaign", [sys.executable, str(root / "tb/pp_top/notify_mutants.py"),
                   "--output", str(receipts / "domain-mutants"), "--verilator", str(wrapper),
                   "--jobs", "2", "--only", *mutants], root)

def focused():
    dest = scratch / "focused"
    for directory in ("hdl", "tb/common", "tb/pp_top"):
        shutil.copytree(root / directory, dest / directory,
                        ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    cwd = dest / "tb/pp_top"
    rc = execute("focused-build", ["make", "-j16", "gsi-build", "VERILATOR=" + str(wrapper)], cwd)
    if rc:
        return rc
    for name, flag in (("domain-golden", "--domain-notify-only"),
                       ("existing-gsi", "--gsi-internal-only"),
                       ("counter-spacing", "--spacing-only")):
        rc |= execute(name, ["./obj_dir/Vpp_top_sim", flag], cwd)
    return rc

with concurrent.futures.ThreadPoolExecutor(2) as pool:
    futures = [pool.submit(campaign), pool.submit(focused)]
    codes = [future.result() for future in futures]
sys.exit(any(codes))
