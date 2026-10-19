#!/usr/bin/env python3
"""Run a slice of a tree's engine mutation arm with that tree's own code.

usage: mutslice.py <tree> <start> <end>
       mutslice.py <tree> list <i,j,k>   (exactly those indices)

Imports <tree>/tb/verilator/engine/mutants.py and runs exactly what its
main() runs (the unmutated positive control, then run_mutant for each
listed mutation), but only for MUTATIONS[start:end], so several slices can
run side by side under one foreground time limit. Prints the same tally
line main() prints.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    if sys.argv[2] == "list":
        picks = [int(x) for x in sys.argv[3].split(",")]
        start, end = 0, 0
    else:
        start, end = int(sys.argv[2]), int(sys.argv[3])
        picks = None
    path = tree / "tb/verilator/engine/mutants.py"
    spec = importlib.util.spec_from_file_location("engine_mutants", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="engine-mutants-",
                                     dir="<scratch>") as td:
        work = Path(td)
        clean_src = mod.stage(work, "clean")
        clean_run = work / "run_clean"
        clean_exe = mod.build(clean_src, work, "clean")
        if clean_exe is None or not mod.generate_image(clean_src, clean_run):
            print("[FAIL] the unmutated sources did not build")
            return 1
        answer = mod.verdict(*mod.run_harness(clean_exe, clean_run))
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated engine still passes the harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated engine does NOT pass ({answer})")
        chosen = (mod.MUTATIONS[start:end] if picks is None
                  else [mod.MUTATIONS[i] for i in picks])
        for mutation in chosen:
            if mod.run_mutant(work, clean_exe, mutation):
                passes += 1
            else:
                fails += 1
    print(f"slice {picks if picks is not None else [start, end]} "
          f"of {len(mod.MUTATIONS)}")
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
