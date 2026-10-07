#!/usr/bin/env python3
"""R524-3 witness probes for the #679/#678 merge resolution (34475e77).

Usage: witness_probes.py <head-copy> <merge-copy> <work>
<head-copy>/<merge-copy> are `git archive` extractions of 34475e77 and 232970db.
MILAN_RV32_CC must name the pinned SDK compiler. Every probe runs in a fresh
copy under <work>; nothing is written to a checkout. Prints one PASS/FAIL line
per expectation and exits non-zero if any expectation is not met.
"""
from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

HEAD, MERGE, WORK = (Path(p).resolve() for p in sys.argv[1:4])
CC = os.environ["MILAN_RV32_CC"]
failures = 0


def expect(name: str, ok: bool, detail: str) -> None:
    global failures
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}: {name}: {detail}", flush=True)


def fresh(src: Path, name: str) -> Path:
    dst = WORK / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, symlinks=True)
    return dst


def load(root: Path):
    """Import the copy's ctrl_arms with module state isolated from other copies."""
    for mod in ("ctrl_arms", "ctrl_build", "fw_rv32", "fw_gtest", "ctrl_mutants"):
        sys.modules.pop(mod, None)
    sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
    try:
        arms = importlib.import_module("ctrl_arms")
        build = importlib.import_module("ctrl_build")
    finally:
        del sys.path[:2]
    return arms, build


def rv32(root: Path, tag: str, libc=None, flags=None):
    arms, build = load(root)
    if libc is not None:
        arms.RV32_LIBC = libc
    if flags is not None:
        arms.RV32_FLAGS = flags
    tree = build.Tree(root / "sw/firmware/ctrl", WORK / f"{tag}-out", WORK / f"{tag}-reuse")
    out = arms.arm_rv32(tree, True)
    (WORK / f"{tag}.log").write_text(out.log + "\n")
    print(f"--- {tag} rc={out.rc}\n{out.log}", flush=True)
    return out, arms


def plant(root: Path, text: str) -> None:
    app = root / "sw/firmware/ctrl/app/ctrl_app.c"
    app.write_text(app.read_text() + "\n" + text + "\n")


# W1 the merge commit (no assert.h for -nostdinc) fails the ctrl rv32 arm.
out, _ = rv32(fresh(MERGE, "merge"), "w1-merge")
expect("W1 merge commit 232970db fails rv32 on assert.h", out.rc == 1 and "assert.h" in out.log, f"rc={out.rc}")

# W2 the head passes and leaves __assert_fail as an open runtime interface.
out, arms = rv32(fresh(HEAD, "head"), "w2-head")
expect("W2 head passes rv32 with __assert_fail open", out.rc == 0 and "__assert_fail" in out.log, f"rc={out.rc}")
expect("W2b RV32_LIBC is exactly four names", arms.RV32_LIBC == {"memset", "memcpy", "vsnprintf", "__assert_fail"},
       str(sorted(arms.RV32_LIBC)))

# W3 header removed: the arm fails.
root = fresh(HEAD, "noheader")
(root / "sw/firmware/gtest/rv32_include/assert.h").unlink()
out, _ = rv32(root, "w3-noheader")
expect("W3 without rv32_include/assert.h rv32 fails", out.rc == 1 and "assert.h" in out.log, f"rc={out.rc}")

# W4 name removed: the arm fails on the stray __assert_fail.
out, _ = rv32(fresh(HEAD, "noname"), "w4-noname", libc=frozenset({"memset", "memcpy", "vsnprintf"}))
expect("W4 without the __assert_fail name rv32 fails", out.rc == 1 and "outside the C library" in out.log
       and "__assert_fail" in out.log.split("outside the C library")[-1], f"rc={out.rc}")

# W5..W8 the allowance is exactly one name: other dependencies stay refused.
for tag, sym in (("w5-malloc", "malloc"), ("w6-unexpected", "__unexpected_service"),
                 ("w7-newlib-handler", "__assert_func"), ("w8-prefix-sibling", "__assert_fail2")):
    root = fresh(HEAD, tag)
    plant(root, f"extern void {sym}(void);\nvoid r524_probe_{tag.replace('-', '_')}(void) {{ {sym}(); }}")
    out, _ = rv32(root, tag)
    expect(f"{tag.upper()} {sym} still refused", out.rc == 1 and sym in out.log.split("outside the C library")[-1],
           f"rc={out.rc}")

# W9 an NDEBUG build references no handler: passes without the name, and nm shows none.
root = fresh(HEAD, "ndebug")
arms0, _ = load(root)
out, _ = rv32(root, "w9-ndebug", libc=frozenset({"memset", "memcpy", "vsnprintf"}),
              flags=tuple(arms0.RV32_FLAGS) + ("-DNDEBUG",))
undefined = out.log.split("undefined:")[-1].splitlines()[0] if "undefined:" in out.log else ""
expect("W9 NDEBUG build passes without the name and leaves no __assert_fail",
       out.rc == 0 and "__assert_fail" not in out.log, f"rc={out.rc} undefined:{undefined}")

# W10 fw_rv32_selftest fails when the header is absent (the header case needs it).
root = fresh(HEAD, "selftest-noheader")
(root / "sw/firmware/gtest/rv32_include/assert.h").unlink()
res = subprocess.run([sys.executable, str(root / "sw/firmware/gtest/fw_rv32_selftest.py"), "--require-rv32"],
                     capture_output=True, text=True, cwd=root)
(WORK / "w10-selftest-noheader.log").write_text(res.stdout + res.stderr)
expect("W10 fw_rv32_selftest fails without assert.h", res.returncode != 0 and "assert.h" in res.stdout + res.stderr,
       f"rc={res.returncode}")

print(f"== witness probes: failures {failures} ==")
sys.exit(1 if failures else 0)
