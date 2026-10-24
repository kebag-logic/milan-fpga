#!/usr/bin/env python3
"""Plant faults in KL_crf_tx.sv (in memory) and run the BDD step behind
features/crf_sr_class_a.feature "The tag replaces pad, it does not resize the
frame" (step_frame_len, n = 60) against each, with the step file unchanged.

usage: python3 bdd_frame_mutants.py <repo> <commit>
Exit 0 only if the clean source passes and every planted fault fails.
"""
import importlib.util
import subprocess
import sys
import types
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
commit = sys.argv[2]
spec = importlib.util.spec_from_file_location(
    "crf_class_a_steps", repo / "tests/steps/crf_class_a_steps.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
src = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:hdl/ieee1722/crf/KL_crf_tx.sv"],
                     check=True, capture_output=True, text=True).stdout

LINE = "localparam int CRF_PDU_C   = CRF_HDR_C + 32'(CRF_DLEN_C);"
assert src.count(LINE) == 1, "clean CRF_PDU_C line not found"
CASES = [
    ("clean", None, None, True),
    ("crf_data_length 12 resizes the frame to 64", "CRF_DLEN_C   = 16'd8;", "CRF_DLEN_C   = 16'd12;", False),
    ("header 24 resizes the frame to 64", "CRF_HDR_C   = 20;", "CRF_HDR_C   = 24;", False),
    ("the tag grows the frame (+ VTAG_C)", "ETH_HDR_C + CRF_PDU_C + 18;", "ETH_HDR_C + VTAG_C + CRF_PDU_C + 18;", False),
    ("round-1 type cast int'(...) the resolver does not read", LINE,
     "localparam int CRF_PDU_C   = CRF_HDR_C + int'(CRF_DLEN_C);", False),
    ("non-arithmetic $bits(...) in the frame size", LINE,
     "localparam int CRF_PDU_C   = CRF_HDR_C + $bits(CRF_DLEN_C) / 2;", False),
]
bad = 0
for name, old, new, want_pass in CASES:
    text = src
    if old is not None:
        assert text.count(old) == 1, f"{name}: anchor {old!r} not unique"
        text = text.replace(old, new)
    ctx = types.SimpleNamespace(crf_src=text)
    try:
        mod.step_frame_len(ctx, 60)
        got, words = True, "passed"
    except AssertionError as exc:
        got, words = False, f"ASSERT FAILED: {exc}"
    ok = got == want_pass
    bad += not ok
    verdict = ("PASS clean" if want_pass else "PASS mutant caught") if ok else "FAIL"
    print(f"[{verdict}] {name}: {words}")
print(f"{len(CASES)} checks: {len(CASES) - bad} PASS, {bad} FAIL")
sys.exit(1 if bad else 0)
