#!/usr/bin/env python3
"""Reviewer mutants of KL_ctrl_split's drop count, run through the split leg.

usage: python3 -I tap_reviewer_mutants.py <probe tree root> <work dir> <arm index>
Builds the split leg (make build-split, CTLS_SRC=<mutant copy>) into its own
directory and runs it; prints the FAIL lines and the tally. An arm with
expect "caught" must fail at least one [TAP] check; "characterise" arms only
report what the leg does.
"""
import subprocess
import sys
from pathlib import Path

root, work, idx = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
src = root / "hdl/milan/KL_ctrl_split.sv"
KEPT = "      last_kept_r <= (tap_r == TAP_BODY_S) || ((tap_r == TAP_HEAD1_S) && accept_w);"
DROP = "  assign drop_p_w = ff_overflow_w & last_kept_r;"
ARMS = [
    ("refused frames ending at beat 1 recorded as kept", KEPT,
     "      last_kept_r <= (tap_r == TAP_BODY_S) || (tap_r == TAP_HEAD1_S);", "caught"),
    ("runts ending at beat 0 recorded as kept", KEPT,
     "      last_kept_r <= (tap_r == TAP_BODY_S) || ((tap_r == TAP_HEAD1_S) && accept_w) || (tap_r == TAP_HEAD0_S);",
     "characterise"),
    ("the kept flag read one cycle early (combinational on the current state)", DROP,
     "  assign drop_p_w = ff_overflow_w & ((tap_r == TAP_BODY_S) || ((tap_r == TAP_HEAD1_S) && accept_w));",
     "caught"),
    ("a drop count that stops counting at 10 (a cap below the saturation)", DROP,
     "  assign drop_p_w = ff_overflow_w & last_kept_r & (rx_drops_o < 8'd10);", "caught"),
]
name, old, new, expect = ARMS[idx]
text = src.read_text()
assert text.count(old) == 1, f"anchor missing for {name}"
d = work / f"arm{idx}"
d.mkdir(parents=True, exist_ok=True)
(d / "KL_ctrl_split.sv").write_text(text.replace(old, new))
b = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(root / "tb/verilator/milan_dp"), "build-split",
                    f"SPLIT_MDIR={d / 'obj'}", f"CTLS_SRC={d / 'KL_ctrl_split.sv'}", "VERILATOR_JOBS=2"],
                   capture_output=True, text=True)
if b.returncode:
    print(f"BUILD-FAIL {name}\n{b.stdout[-2000:]}{b.stderr[-2000:]}")
    sys.exit(3)
r = subprocess.run([str(d / "obj/Vmilan_dp_split")], capture_output=True, text=True,
                   cwd=root / "tb/verilator/milan_dp")
out = r.stdout + r.stderr
fails = [ln for ln in out.splitlines() if ln.startswith("FAIL") or ln.startswith("[TAP] burst") or ln.startswith("checks:")]
caught = r.returncode != 0 and any(ln.startswith("FAIL [TAP]") for ln in out.splitlines())
print(f"arm {idx}: {name} (expect {expect}): rc {r.returncode}, {'caught' if caught else 'not caught'}")
print("\n".join(fails))
sys.exit(0 if (expect == "characterise" or caught) else 1)
