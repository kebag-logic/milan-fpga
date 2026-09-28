#!/usr/bin/env python3
"""Run the supplied first-probe harness from scratch with its fixed-behavior oracle.

Usage: run_parent_probe.py DONOR PARENT ANALYSIS SCRATCH
Only SCRATCH is written by the harness. PARENT and ANALYSIS stay read-only.
"""
import difflib
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Copy the minimum build inputs and require success on the first probe."""
    donor, parent, analysis, scratch = [Path(arg).resolve() for arg in sys.argv[1:]]
    scratch.mkdir(parents=True, exist_ok=True)
    pp = scratch / "parent/protocol-processor"
    for folder in ("hdl/common", "hdl/srp", "hdl/acmp", "tb/acmp_talker", "tb/common"):
        shutil.copytree(donor / folder, pp / folder, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))
    shim = scratch / "parent/hdl/milan/KL_pp_maap_shim.sv"
    shim.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(parent / "hdl/milan/KL_pp_maap_shim.sv", shim)
    for filename in ("run_first_probe.py", "reproduce_first_probe.cpp"):
        shutil.copy2(analysis / filename, scratch / filename)
    cpp = scratch / "reproduce_first_probe.cpp"
    original = cpp.read_text()
    fixed = original.replace('h.run(2000)', 'h.run(N_SRC * (MAAP_TMO + 64))')
    fixed = fixed.replace('h.mreqs.size()==requests,"unexpected retry on block becoming available"',
                          'h.mreqs.size()==requests+N_SRC,"automatic retry sweep missing"')
    fixed = fixed.replace('block later valid, no automatic re-allocation',
                          'block later valid; retry interval and bounded sweep elapsed')
    fixed = fixed.replace('h.resps[0].status==3,"first probe did not reproduce status 3"',
                          'h.resps[0].status==0,"first probe failed after acquisition bound"')
    fixed = fixed.replace('h.resps[0].da==0 && h.resps[0].sid==0 && h.resps[0].vlan==0,"failed response unexpectedly carries valid tuple"',
                          'h.resps[0].da==0x91e0f0006818ULL && h.resps[0].sid==sid_of(1) && h.resps[0].vlan==VID,"first response tuple wrong"')
    fixed = fixed.replace('h.mreqs.size()==requests+1,"probe did not trigger allocation retry"',
                          'h.mreqs.size()==requests+N_SRC,"first probe unexpectedly reallocates"')
    fixed = fixed.replace('FIRST_PROBE reproduced: first response status=3 and zero tuple; same probe queues ALLOC, later opens declaration gate',
                          'FIRST_PROBE fixed: status=0, DA=91e0f0006818, source SID and VID valid; no probe-triggered ALLOC')
    fixed = fixed.replace('successful deferred allocation did not open DA gate',
                          'first probe did not open the acquired DA gate')
    fixed = fixed.replace('allocation-availability mechanism reproduced',
                          'late availability recovered within the acquisition bound')
    cpp.write_text(fixed)
    (scratch / "harness-oracle.diff").write_text(''.join(difflib.unified_diff(
        original.splitlines(True), fixed.splitlines(True),
        fromfile="original/reproduce_first_probe.cpp", tofile="fixed/reproduce_first_probe.cpp")))
    head = subprocess.check_output(["git", "-C", str(donor), "rev-parse", "HEAD"], text=True).strip()
    print(f"Donor HEAD: {head}", flush=True)
    for path in (pp / "hdl/acmp/KL_acmp_talker.sv", shim, cpp):
        data = path.read_bytes()
        print(f"{path.relative_to(scratch)} size={len(data)} sha256={hashlib.sha256(data).hexdigest()}", flush=True)
    result = subprocess.run([sys.executable, str(scratch / "run_first_probe.py"),
                             str(scratch / "parent"), str(scratch / "build")],
                            timeout=900, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
