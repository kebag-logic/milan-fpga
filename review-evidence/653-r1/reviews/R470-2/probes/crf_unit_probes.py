#!/usr/bin/env python3
"""Reviewer probes for the #653 KL_crf_rx unbind arm, graded by the crf_rx unit suite.

Run from a DISPOSABLE copy of the repository (never the reviewed clone):
    python3 crf_unit_probes.py <tree> <dev_KL_crf_rx.sv> <out_dir>
Each probe writes a mutated KL_crf_rx copy under <out_dir>, builds and runs
`make -C <tree>/tb/verilator/crf_rx unit RX_RTL=<copy>` and records the log
and the [FAIL] lines. A probe is CAUGHT when every expected check id fails.
The clean head RTL runs first as the positive control (must be 0 failures).
"""
import re
import subprocess
import sys
from pathlib import Path

tree, dev_rtl, out = (Path(a).resolve() for a in sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)
head_rtl = tree / "hdl/ieee1722/crf/KL_crf_rx.sv"
head = head_rtl.read_text()

ARM = "      if (w_bind_fall_w && locked_o) begin\n"
ARM_DROP = ARM + "        locked_o       <= 1'b0;\n"
ARM_TAIL = ("        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n"
            "        dirty_p_o      <= 1'b1;\n"
            "      end\n\n"
            "      //! not-bound -> bound")
ARM_INC = ARM_DROP + "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n"
TOUT_HIT = "(tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0])"

# name -> (rtl text, expected failing check ids)
PROBES = {
    "P0_clean_head": (head, []),
    "P2_dev_rtl_fea346e7": (dev_rtl.read_text(),
                            ["[UNB-a1]", "[UNB-a2]", "[UNB-a4]", "[UNB-a5]", "[5t-g3b]"]),
    "P3_no_lock_gate": (head.replace(ARM, "      if (w_bind_fall_w) begin\n"),
                        ["[UNB-c1]", "[UNB-c2]"]),
    "P4_keeps_lock": (head.replace(ARM_DROP, ARM), ["[UNB-a1]", "[UNB-b1]"]),
    "P5_no_dirty": (head.replace(ARM_TAIL, ARM_TAIL.replace(
        "        dirty_p_o      <= 1'b1;\n", "", 1)), ["[UNB-a5]"]),
    "P6_shared_edge_double": (head.replace(ARM_INC, ARM_DROP +
        f"        cnt_unlocked_o <= cnt_unlocked_o + ({TOUT_HIT} ? 32'd2 : 32'd1);\n"),
        ["[UNB-d2]"]),
}

rc_all = 0
summary = []
for name, (text, expect) in PROBES.items():
    if name != "P0_clean_head" and name != "P2_dev_rtl_fea346e7" and text == head:
        summary.append(f"{name}: REFUSED (pattern did not match; nothing mutated)")
        rc_all = 1
        continue
    rtl = out / f"{name}.sv"
    rtl.write_text(text)
    r = subprocess.run(["make", "-C", str(tree / "tb/verilator/crf_rx"), "unit",
                        f"RX_RTL={rtl}"], capture_output=True, text=True, check=False)
    log = r.stdout + r.stderr
    (out / f"{name}.log").write_text(log)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    tally = re.findall(r"KL_crf_rx: (\d+) checks, (\d+) failures", log)
    missed = [e for e in expect if not any(e in f for f in fails)]
    if not expect:
        ok = r.returncode == 0 and not fails and tally and tally[-1][1] == "0"
        verdict = "PASS (positive control clean)" if ok else "FAIL (clean control not clean)"
    else:
        ok = not missed and bool(fails)
        verdict = "CAUGHT" if ok else f"SURVIVED/MISSED {missed}"
    rc_all |= 0 if ok else 1
    summary.append(f"{name}: rc={r.returncode} tally={tally[-1] if tally else None} "
                   f"fails={len(fails)} -> {verdict}")
    for f in fails[:12]:
        summary.append(f"    {f[:200]}")
(out / "SUMMARY.txt").write_text("\n".join(summary) + f"\nrc={rc_all}\n")
print("\n".join(summary))
sys.exit(rc_all)
