#!/usr/bin/env python3
"""Witness: fw_rv32_selftest's header case fails when rv32_include/assert.h is absent.

Usage: MILAN_RV32_CC=<cc> python3 selftest_header_witness.py REPO WORK
"""
import shutil, sys
from pathlib import Path
from unittest.mock import patch
R, W = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(R / "sw/firmware/gtest")]
import fw_rv32, fw_rv32_selftest
cc = fw_rv32.compiler()
shutil.rmtree(W, ignore_errors=True)
(W / "pos").mkdir(parents=True)
print("positive control checks:", fw_rv32_selftest.header_and_abi_cases(cc, W / "pos"))
alt = W / "gtest"
shutil.copytree(R / "sw/firmware/gtest/rv32_include", alt / "rv32_include")
(alt / "rv32_include/assert.h").unlink()
(W / "neg").mkdir()
with patch.object(fw_rv32, "HERE", alt):
    try:
        fw_rv32_selftest.header_and_abi_cases(cc, W / "neg")
    except AssertionError as exc:
        ok = "assert.h" in str(exc)
        print(("PASS" if ok else "FAIL") + ": self-test fails without rv32_include/assert.h:", str(exc).strip().splitlines()[0])
        sys.exit(0 if ok else 1)
print("FAIL: self-test passed without rv32_include/assert.h"); sys.exit(1)
