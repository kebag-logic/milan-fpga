#!/usr/bin/env python3
"""Witness: the head's prefix suite passes under ASan; the restored `end` bound
(nvm_mutants erased_payload_end_bound) gives an ASan heap-buffer-overflow READ.

Usage: python3 asan_end_bound.py REPO WORK
"""
import os, sys
from pathlib import Path
R, W = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(R / "sw/firmware/ctrl_nvm/test"), str(R / "sw/firmware/gtest")]
import fw_gtest, nvm_bench, nvm_mutants
cfg = R / "configs/endstation_ax7101_1x1_tdm8.yaml"
inputs = nvm_bench.shape_inputs(cfg, W / "inputs")
binary = next(b for b in nvm_bench.UNITS if b.name == "prefix")
b = fw_gtest.Build(jobs=4)
fail = 0
exe = nvm_bench.build_suite(inputs, W / "head", b, binary)
ok, log = nvm_bench.run_suite(exe, W / "none")
print(f"head prefix suite under ASan: {'PASS' if ok else 'FAIL'}"); print(log[-600:])
fail += not ok
m = next(m for m in nvm_mutants.MUTANTS if m.name == "erased_payload_end_bound")
nvm_mutants.plant(m, W / "mut")
exe = nvm_bench.build_suite(inputs, W / "mutbuild", b, binary, tree=W / "mut")
env = {**os.environ, "NVM_FIXTURE": str(W / "none"), "ASAN_OPTIONS": "abort_on_error=1"}
import subprocess
res = subprocess.run([str(exe)], env=env, capture_output=True, text=True)
text = res.stdout + res.stderr
hit = res.returncode != 0 and "heap-buffer-overflow" in text and "READ of size" in text and "nvm_all_erased" in text
print(f"restored end bound: rc={res.returncode} {'PASS: ASan heap-buffer-overflow READ in nvm_all_erased' if hit else 'FAIL'}")
for ln in text.splitlines():
    if "ERROR: AddressSanitizer" in ln or "READ of size" in ln or "nvm_all_erased" in ln or "SUMMARY" in ln:
        print("  " + ln.strip()[:200])
fail += not hit
sys.exit(1 if fail else 0)
