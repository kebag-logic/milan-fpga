#!/usr/bin/env python3
"""A three-entry stand-in for an engine mutation arm, for probing
tb/mutation_jobs_test.py's own checks in seconds.

usage: fake_arm.py --jobs N   (FAKE_MODE in the environment picks a defect)

Each entry compiles one small C unit, in a new temporary directory and by
relative name, through $OBJCACHE when it is set and nonempty, then prints a
[PASS] verdict line; a tally follows. FAKE_MODE:
  good       - as above
  jobsdiff   - at --jobs > 1 the second verdict line reads differently
  nocache    - ignores OBJCACHE: every compile is plain
  alwayscache- ignores an empty OBJCACHE: every compile goes through ccache
"""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MUTATIONS = [("m0", "", "", "", "b0"), ("m1", "", "", "", "b1"), ("m2", "", "", "", "b2")]


def compile_unit(index: int, mode: str) -> bool:
    """Compile entry `index`'s unit in a new temporary directory."""
    objcache = os.environ.get("OBJCACHE", "")
    if mode == "nocache":
        objcache = ""
    if mode == "alwayscache":
        objcache = "ccache"
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "unit.c"
        src.write_text(f"int entry_{index}(void) {{ return {index}; }}\n")
        cmd = ([objcache] if objcache else []) + ["cc", "-O1", "-c", "-o", "unit.o", "unit.c"]
        return subprocess.run(cmd, cwd=td, capture_output=True).returncode == 0


def main() -> int:
    """Print one verdict per entry and a tally."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    mode = os.environ.get("FAKE_MODE", "good")
    print("[PASS] the unmutated engine still passes the harness")
    for i, m in enumerate(MUTATIONS):
        ok = compile_unit(i, mode)
        word = "caught" if not (mode == "jobsdiff" and args.jobs > 1 and i == 1) else "CAUGHT"
        print(f"[{'PASS' if ok else 'FAIL'}] mutant {word}: {m[0]}")
    total = 1 + len(MUTATIONS)
    print(f"\n{total} checks: {total} PASS, 0 FAIL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
