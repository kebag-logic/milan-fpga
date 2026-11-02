#!/usr/bin/env python3
"""Run named repository mutants against one control (review probe).

Usage: python3 stated_seconds_check.py <repo> <control> NAME ...
"""
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import process_test_support as pts  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

control, names = sys.argv[2], sys.argv[3:]
with OwnedProcesses():
    with tempfile.TemporaryDirectory(prefix="ss-check-",
                                     dir=str(Path(__file__).resolve().parent.parent / "scratch")) as scratch:
        for name in names:
            status, seconds, output = pts.run_mutant(pts.mutant_tree(Path(scratch), name), control)
            lines = [line for line in output.splitlines() if line.strip()]
            print(f"{name} / {control}: {'red' if status else 'green'} rc {status} {seconds:.1f} s: "
                  f"{lines[-1][:200] if lines else ''}", flush=True)
