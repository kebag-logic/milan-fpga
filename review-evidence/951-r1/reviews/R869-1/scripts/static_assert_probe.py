#!/usr/bin/env python3
"""Reviewer probe of srp_mbx.c's compile-time refusal of a hold-off past held_cs (#951).

Usage: python3 -B static_assert_probe.py <head-repo-root> <work-dir>

Copies the head's sw/firmware/ctrl into <work-dir>/<case>/ctrl, replaces SRP_REDECLARE_CS's definition with each
case's value, and compiles srp_mbx.c at 1x1/1if with the split hart's RV32IM flags and with the host compiler
(unsigned long 64 bits there, 32 on RV32). Prints whether each compile refuses with the assertion's words.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(ROOT / "sw/firmware/gtest"))

import fw_rv32  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, C_FLAGS, SPLIT_RV32_FLAGS, Tree  # noqa: E402

OLD = "#define SRP_REDECLARE_CS (2u * SRP_LEAVEALL_LONGEST_CS + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)\n"
CASES = {"head": None, "65535": "65535u", "65536": "65536u", "leaveall-30000": "LEAVEALL"}
CONFIG = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"


def main() -> int:
    cc = fw_rv32.compiler()
    lw = ROOT / "third_party/lwSRP/src"
    for case, value in CASES.items():
        base = WORK / case
        if base.exists():
            shutil.rmtree(base)
        src = base / "ctrl"
        shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        target = src / "srp/srp_mbx.c"
        text = target.read_text()
        assert text.count(OLD) == 1
        if value == "LEAVEALL":
            text = text.replace("#define SRP_LEAVEALL_CS 1000u\n", "#define SRP_LEAVEALL_CS 30000u\n")
        elif value is not None:
            text = text.replace(OLD, f"#define SRP_REDECLARE_CS {value}\n")
        target.write_text(text)
        _, inc = srp_arms.prepared(Tree(src, base / "build", base / "reuse"), 1, base, CONFIG)
        lwinc = ["-DLWSRP_MILAN=1", f"-I{lw / 'include'}", f"-I{lw}"]
        for label, argv in (("rv32im", [cc, *SPLIT_RV32_FLAGS, *fw_rv32.includes(cc)]),
                            ("host", ["gcc", *C_FLAGS])):
            res = subprocess.run([*argv, *inc, *lwinc, "-c", str(target), "-o", str(base / f"{label}.o")],
                                 capture_output=True, text=True)
            refused = "held_cs holds the hold-off" in res.stderr
            print(f"{case:15s} {label:7s} rc={res.returncode} refused-by-assert={refused}")
            if res.returncode and not refused:
                print(res.stderr[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
