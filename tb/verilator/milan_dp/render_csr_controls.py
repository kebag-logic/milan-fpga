#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #443 controls through the real milan_dp AXI-Lite path.

The clean leg exercises prefill, fill, convergence, a rail and reset.
Wrong-fill and bit-9 selector mutants must fail named comparisons.
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
    start = source.index("  KL_render_setpoint #(\n")
    end = source.index("  //! the whole render map", start)
    outputs = (
        "rsp_tdata_w", "rsp_tvalid_w", "rsp_tlast_w", "rsp_tuser_w",
        "rsp_wire_chans_w", "rsp_render_tick_p_w", "rsp_pop_p_w",
        "rsp_fill_w", "rsp_prefill_w", "rsp_converged_w", "rsp_underruns_w",
        "rsp_overruns_w", "rsp_rails_w", "rsp_recentres_w",
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
    pattern = "rsp_fill_w[s*8 +: 8]};"
    if source.count(pattern) != 1:
        print("[FAIL] wrong-fill mutation anchor must occur exactly once")
        return 1
    csr_source = CSR_RTL.read_text()
    selector = "if (!strm_dir_r && (32'(strm_idx_r) == s))"
    if csr_source.count(selector) != 1:
        print("[FAIL] selector mutation anchor must occur exactly once")
        return 1
    cases = (
        ("wrong_fill", "DP_SRC", source.replace(pattern, "8'd0};"),
         "--render-csr-only", "RENDER-CSR: filling mirrors taps"),
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
