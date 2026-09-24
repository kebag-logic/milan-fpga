#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R276-6 reviewer probe: grade gmstep_mutants.is_fresh() for both positive
legs from inside a parent make recipe, with whichever `make` is first on PATH.

Loads the runner under test from a given file (the head's, or an older copy
for the control), so nothing in the tree is edited. Prints the make version
the subprocess sees, MAKEFLAGS/MAKELEVEL, the raw `print-srcs` output of both
invocations (with and without --no-print-directory) with any token that is
not an existing file, and is_fresh() for each leg.

Usage: fresh_probe.py <milan_dp dir> <gmstep_mutants.py to load> <label>
Exit 0 when every leg is fresh, 1 otherwise.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    here = Path(sys.argv[1]).resolve()
    runner = Path(sys.argv[2]).resolve()
    label = sys.argv[3]
    # the runner imports suite_tally from the tree's scripts/
    sys.path.insert(0, str(here / "../../../scripts"))
    spec = importlib.util.spec_from_file_location(f"gm_{label}", runner)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # the module computes HERE from its own file; point it at the suite
    mod.HERE = here
    legs = {k: v._replace(clean_mdir=here / v.clean_mdir.name) for k, v in mod.LEGS.items()}
    ver = subprocess.run(["make", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    print(f"[{label}] make on PATH: {ver}")
    print(f"[{label}] MAKELEVEL={os.environ.get('MAKELEVEL')!r} MAKEFLAGS={os.environ.get('MAKEFLAGS')!r}")
    for argv in (["make", "-s", "-C", str(here), "print-srcs"],
                 ["make", "--no-print-directory", "-s", "-C", str(here), "print-srcs"]):
        out = subprocess.run(argv, capture_output=True, text=True)
        bad = [t for t in out.stdout.split() if not (here / t).is_file()]
        print(f"[{label}] {' '.join(argv[:-3])} ... print-srcs: rc={out.returncode} "
              f"tokens={len(out.stdout.split())} non-file tokens={bad[:6]}")
    ok = True
    for key, leg in legs.items():
        exe = leg.clean_mdir / leg.exe_name
        fresh = mod.is_fresh(leg, exe)
        print(f"[{label}] leg {key}: exe exists={exe.is_file()} is_fresh: {fresh}")
        ok &= fresh
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
