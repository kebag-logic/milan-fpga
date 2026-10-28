#!/usr/bin/env python3
"""Run one shard of the engine mutation arm of a FPGA-gPTP tree.

Usage: engine_arm_shard.py <tree> <shard> <nshards> [build_jobs]

Imports <tree>/tb/verilator/engine/mutants.py unchanged and runs its own
stage/build/run/verdict code: the unmutated control, then every mutant whose
index i satisfies i % nshards == shard. Prints the arm's own verdict lines
plus a per-shard tally; exit 0 only when the control passes and every mutant
in the shard is caught on every check it names.
"""
import sys
import tempfile
import importlib.util
from pathlib import Path


def main() -> int:
    tree, shard, nshards = Path(sys.argv[1]).resolve(), int(sys.argv[2]), int(sys.argv[3])
    jobs = sys.argv[4] if len(sys.argv) > 4 else "2"
    path = tree / "tb/verilator/engine/mutants.py"
    spec = importlib.util.spec_from_file_location("engine_mutants", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    i = m.VFLAGS.index("-j")
    m.VFLAGS[i + 1] = jobs
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix=f"eng-shard{shard}-") as td:
        work = Path(td)
        clean_src = m.stage(work, "clean")
        clean_run = work / "run_clean"
        clean_exe = m.build(clean_src, work, "clean")
        if clean_exe is None or not m.generate_image(clean_src, clean_run):
            print("[FAIL] control did not build")
            return 1
        ans = m.verdict(*m.run_harness(clean_exe, clean_run))
        print(f"[{'PASS' if ans == 'pass' else 'FAIL'}] shard {shard} control: {ans}")
        passes, fails = (1, 0) if ans == "pass" else (0, 1)
        for idx, mut in enumerate(m.MUTATIONS):
            if idx % nshards != shard:
                continue
            print(f"--- mutant #{idx}: {mut[0]}", flush=True)
            if m.run_mutant(work, clean_exe, mut):
                passes += 1
            else:
                fails += 1
            sys.stdout.flush()
    print(f"\nshard {shard}/{nshards}: {passes + fails} checks: {passes} PASS, {fails} FAIL "
          f"(of {len(m.MUTATIONS)} mutants total in arm)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
