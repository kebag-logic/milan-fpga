#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R276-6 reviewer probe: negative controls for the round-3 RENDER-SETTIME
checks of the true-ratio leg (sim_aclk.cpp). Each control plants one defect
into a private copy of milan_datapath.sv, builds the SAME leg through the
suite's own recipe (`make aclk-build` with DP_SRC and ACLK_MDIR overridden),
runs it with --render-only (RENDER-SETTIME runs before that early return) and
requires the named RENDER-SETTIME check(s) among the [FAIL] lines. Nothing in
the tree is edited.

Usage: aclk_settime_controls.py <milan_dp dir> <workdir> <verilator>
Exit 0 when every control is caught by its named check.
"""
import subprocess
import sys
from pathlib import Path

TRIGGER = "       media_rebase_p_w\n       | src_recentre_p_r;"
LATE = ("  logic [18:0] rv_late_cnt_r;\n"
        "  logic        rv_late_arm_r;\n"
        "  always_ff @(posedge axis_clk) begin : rv_late\n"
        "    if (!axis_resetn) begin rv_late_cnt_r <= '0; rv_late_arm_r <= 1'b0; end\n"
        "    else if (cfg_ptp_cmd_load) begin rv_late_cnt_r <= 19'd375000; rv_late_arm_r <= 1'b1; end\n"
        "    else if (rv_late_arm_r && rv_late_cnt_r != 0) rv_late_cnt_r <= rv_late_cnt_r - 1'b1;\n"
        "    else rv_late_arm_r <= 1'b0;\n"
        "  end : rv_late\n"
        "  wire rv_late_p_w = rv_late_arm_r && (rv_late_cnt_r == 19'd1);\n")
ANCHOR = "  wire render_recentre_p_w /* verilator public_flat_rd */ =\n"
CONTROLS = [
    # the lane's own round-3 control: settime removed from the render trigger only
    ("settime removed from the render trigger", TRIGGER,
     "       eff_ptp_adjust_w\n       | src_recentre_p_r;",
     ["RENDER-SETTIME: the settime reaches the stage as one pulse",
      "RENDER-SETTIME: the settime executes one render re-base"]),
    # reviewer control: the settime re-bases the stage a second time 30 PDUs later
    ("settime re-bases the render stage again 30 PDUs later", ANCHOR + TRIGGER,
     LATE + ANCHOR + "       media_rebase_p_w | rv_late_p_w\n       | src_recentre_p_r;",
     ["RENDER-SETTIME: no later re-base pulse",
      "RENDER-SETTIME: the render re-base remains counted once"]),
]


def main() -> int:
    here = Path(sys.argv[1]).resolve()
    work = Path(sys.argv[2]).resolve()
    vl = sys.argv[3]
    work.mkdir(parents=True, exist_ok=True)
    base = (here / "../../../hdl/milan/milan_datapath.sv").resolve()
    text = base.read_text()
    ok = True
    for i, (name, anchor, repl, must) in enumerate(CONTROLS):
        if text.count(anchor) != 1:
            print(f"[FAIL] {name}: anchor count {text.count(anchor)}")
            ok = False
            continue
        planted = work / f"c{i}_milan_datapath.sv"
        planted.write_text(text.replace(anchor, repl))
        mdir = work / f"obj_aclk_c{i}"
        b = subprocess.run(["make", "-s", "-C", str(here), "aclk-build", f"VERILATOR={vl}",
                            "VERILATOR_JOBS=8", f"DP_SRC={planted}", f"ACLK_MDIR={mdir}"],
                           capture_output=True, text=True)
        exe = mdir / "Vmilan_dp_aclk"
        if b.returncode != 0 or not exe.is_file():
            print(f"[FAIL] {name}: did not build\n{b.stderr[-1500:]}")
            ok = False
            continue
        r = subprocess.run([str(exe), "--render-only"], cwd=str(here), capture_output=True, text=True)
        out = r.stdout + r.stderr
        (work / f"c{i}_run.log").write_text(out)
        fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
        tally = [ln.strip() for ln in out.splitlines() if "checks:" in ln]
        hit = all(any(m in f for f in fails) for m in must)
        print(f"[{'PASS' if hit and r.returncode != 0 else 'FAIL'}] control {name}: rc={r.returncode} "
              f"{tally[-1] if tally else 'no tally'}")
        for f in fails:
            print(f"    {f}")
        ok &= hit and r.returncode != 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
