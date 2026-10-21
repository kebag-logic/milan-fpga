#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #443 controls through the real milan_dp AXI-Lite path.

The clean leg exercises RENDER_STAT (0x8DC) through reset, the lead queued
ahead of the first presentation, convergence, the refused PDUs and reset
again. Wrong-lead and bit-9 selector mutants must fail named comparisons.
The absent-stage control removes the instance and ties every output to zero;
it still accepts AAF ingress but its CSR must remain structural zero.
Control sources leave the working tree unchanged. Every simulation is cycle-bounded by
sim_aclk.cpp's loops and existing AXI/ingress guards. No host-time verdict.

Run through `make render-csr-controls`, or after building `make aclk-build`.
"""

import sys
import tempfile
from pathlib import Path

from render_mutants import CLEAN_EXE, DP_RTL, build, run_leg, verdict

CSR_RTL = Path(__file__).resolve().parents[3] / "hdl/common/csr/milan_csr.sv"


def without_stage(source: str) -> str:
    """Remove the real stage; explicit ties are the integration contract."""
    start = source.index("  KL_render_queue #(\n")
    end = source.index("  //! the whole render map", start)
    outputs = (
        "rq_tdata_w", "rq_tvalid_w", "rq_tlast_w", "rq_tuser_w",
        "rq_wire_chans_w", "rq_render_tick_p_w", "rq_pop_p_w",
        "rq_lead_w", "rq_idle_w", "rq_converged_w", "rq_late_w",
        "rq_early_w", "rq_untimed_w", "rq_slips_w",
    )
    ties = "".join(f"  assign {name} = '0;\n" for name in outputs)
    return source[:start] + ties + source[end:]


def main() -> int:
    """Require a clean pass, named mutant failures and an absent-stage pass."""
    if not CLEAN_EXE.is_file():
        print("[FAIL] build the clean leg with make aclk-build first")
        return 1
    rc, log = run_leg(CLEAN_EXE, "--render-csr-only")
    print(log)
    if verdict(rc, log, None) != "pass":
        print("[FAIL] clean render CSR control")
        return 1
    source = DP_RTL.read_text()
    pattern = "rq_lead_w[s*8 +: 8]};"
    if source.count(pattern) != 1:
        print("[FAIL] wrong-lead mutation anchor must occur exactly once")
        return 1
    csr_source = CSR_RTL.read_text()
    selector = "if (!strm_dir_r && (32'(strm_idx_r) == s))"
    if csr_source.count(selector) != 1:
        print("[FAIL] selector mutation anchor must occur exactly once")
        return 1
    cases = (
        ("wrong_lead", "DP_SRC", source.replace(pattern, "8'd0};"),
         "--render-csr-only", "RENDER-CSR: queued mirrors taps"),
        ("bit9_window_selection", "CSR_SRC", csr_source.replace(
            selector, "if (strm_lsn0_r ? (s == 0) : "
            "(!strm_dir_r && (32'(strm_idx_r) == s)))"),
         "--render-csr-only", "RENDER-CSR: bit 9 preserves talker rejection"),
        ("absent_stage", "DP_SRC", without_stage(source), "--render-csr-absent", None),
    )
    failures = 0
    with tempfile.TemporaryDirectory(prefix="render-csr-controls-") as temp:
        work = Path(temp)
        for name, override, changed, mode, named_check in cases:
            rtl = work / f"{name}.sv"
            rtl.write_text(changed)
            exe = build(override, rtl, work / f"obj_{name}")
            if exe is None:
                print(f"[FAIL] {name}: build failed; no control evidence")
                failures += 1
                continue
            rc, log = run_leg(exe, mode)
            answer = verdict(rc, log, named_check)
            expected = "caught" if named_check else "pass"
            if named_check:
                for line in log.splitlines():
                    if line.strip().startswith("[FAIL]") and named_check in line:
                        print(line.replace("[FAIL]", "[EXPECTED MUTANT FAILURE]"))
            else:
                print(log)
            ok = answer == expected
            print(f"[{'PASS' if ok else 'FAIL'}] {name}: rc={rc}, {answer}; "
                  f"named check={named_check}")
            failures += not ok
    print(f"render_csr_controls: {1 + len(cases)} checks, {failures} failures")
    return int(failures != 0)


if __name__ == "__main__":
    sys.exit(main())
