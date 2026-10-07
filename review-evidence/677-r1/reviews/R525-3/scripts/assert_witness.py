#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer witness for the round-3 RV32 assertion interface (PR #684).

Usage: MILAN_RV32_CC=<pinned riscv32-linux-gcc> python3 assert_witness.py REPO WORK

REPO is a checkout at the head under review; WORK is a disposable directory.
Every probe runs on a copy of the ctrl tree or with an in-process patch; the
checkout is never written. Exit 0 only when every expectation holds.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

REPO = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path[:0] = [str(REPO / "sw/firmware/gtest"), str(REPO / "sw/firmware/ctrl/test")]

import ctrl_arms  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

failures = 0


def expect(name: str, ok: bool, log: str) -> None:
    global failures
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
    if not ok:
        failures += 1
        print(log)


def undefined(log: str) -> set[str]:
    line = next((ln for ln in log.splitlines() if ln.strip().startswith("undefined:")), "")
    return {s.strip() for s in line.split(":", 1)[-1].split(",") if s.strip()}


def fresh(tag: str) -> tuple[Tree, Path]:
    src = WORK / tag / "ctrl"
    shutil.rmtree(WORK / tag, ignore_errors=True)
    shutil.copytree(CTRL, src)
    return Tree(src, WORK / tag / "build", WORK / tag / "reuse"), src


print(f"compiler: {fw_rv32.compiler()}")
print(f"RV32_LIBC: {sorted(ctrl_arms.RV32_LIBC)}")
expect("allowance adds exactly one name to #679's set",
       ctrl_arms.RV32_LIBC == frozenset({"memset", "memcpy", "vsnprintf", "__assert_fail"}), str(ctrl_arms.RV32_LIBC))

# W0: the head as shipped passes, and the debug build references the handler.
tree, _ = fresh("w0")
got = ctrl_arms.arm_rv32(tree, True)
print(got.log)
expect("W0 head arm passes", got.rc == 0, got.log)
expect("W0 debug build leaves __assert_fail open", "__assert_fail" in undefined(got.log), got.log)

# W1: without rv32_include/assert.h the arm fails (no hosted fallback).
alt = WORK / "w1-gtest"
shutil.rmtree(alt, ignore_errors=True)
shutil.copytree(REPO / "sw/firmware/gtest/rv32_include", alt / "rv32_include")
(alt / "rv32_include/assert.h").unlink()
tree, _ = fresh("w1")
with patch.object(fw_rv32, "HERE", alt):
    got = ctrl_arms.arm_rv32(tree, True)
expect("W1 arm fails without assert.h", got.rc != 0 and "assert.h" in got.log, got.log)

# W2: without the allowed name the arm fails on __assert_fail.
tree, _ = fresh("w2")
with patch.object(ctrl_arms, "RV32_LIBC", ctrl_arms.RV32_LIBC - {"__assert_fail"}):
    got = ctrl_arms.arm_rv32(tree, True)
expect("W2 arm fails on __assert_fail without the name",
       got.rc != 0 and "symbols outside the C library" in got.log and "__assert_fail" in got.log, got.log)

# W3: an NDEBUG build references no handler, and passes even without the name.
tree, _ = fresh("w3")
with patch.object(ctrl_arms, "RV32_FLAGS", (*ctrl_arms.RV32_FLAGS, "-DNDEBUG")), \
        patch.object(ctrl_arms, "RV32_LIBC", ctrl_arms.RV32_LIBC - {"__assert_fail"}):
    got = ctrl_arms.arm_rv32(tree, True)
print(got.log)
expect("W3 NDEBUG build passes and references no assertion handler",
       got.rc == 0 and not any("assert" in s for s in undefined(got.log)), got.log)

# W4: the allowance is one exact name, not a prefix or a family.
for symbol in ("malloc", "__unexpected_service", "__assert_func", "__assert", "__assert_failx", "abort"):
    tree, src = fresh(f"w4-{symbol}")
    source = src / "port/shlan_port.c"
    original = source.read_text()
    planted = original.replace("return ctrl_pool_alloc(port_pool, size);", f"return {symbol}(size);")
    assert planted != original, "plant site moved"
    source.write_text(f"extern void *{symbol}(__SIZE_TYPE__);\n" + planted)
    got = ctrl_arms.arm_rv32(tree, True)
    expect(f"W4 rejects {symbol}",
           got.rc != 0 and "symbols outside the C library" in got.log and symbol in got.log, got.log)

print(f"assert witness: failures {failures}")
sys.exit(1 if failures else 0)
