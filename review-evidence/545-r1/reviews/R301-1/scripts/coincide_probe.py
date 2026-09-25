#!/usr/bin/env python3
"""Probe: a PHC step staged on the boundary sample while the slew level is held.

Adds a scratch-only mode (+coincide) to a COPY of sim_phc_step.cpp at the head:
lock, hold the level, stage a 150 us step so the boundary fires on the stepped
sample (the same arming checks as P2a), and read the discard tally delta across
that boundary. The documented contract (REGISTER_MAP 0x8F8, TIME_SYNC) is one
count for that window. Built against the head servo and against the mutant that
drops `&& !step_hit_w`; no tracked file is modified.
"""
import os
import subprocess
from pathlib import Path

PKT = Path(os.environ.get("PKT", "$REVIEWS/545-r301-1-packet"))
TREE = PKT / "scratch/tree"
MS = TREE / "tb/verilator/mmcm_servo"
VER = os.environ.get("VERILATOR", "$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator")
W = PKT / "scratch/coincide"
W.mkdir(parents=True, exist_ok=True)

src = (MS / "sim_phc_step.cpp").read_text()
case = r'''
    int coincide() {
        prove_lock_at_the_silicon_scale();
        held_slew_ = true;
        run_to_tick(kWinTicks / 2);
        run_to_edges_before_t0(2);
        const int d0 = disc_cnt();
        ptp_step_ns += 150'000.0;
        clk_edge();
        check_.that("[C1] arm: stepped sample staged, T0 next edge", ptp_jump() && edges_to_t0() == 1);
        clk_edge();
        check_.that("[C1] arm: boundary fired on the stepped sample", pp_seq() == 1);
        for (int e = 0; e < 4; e++) clk_edge();
        within("[C1] coincident step+slew window counted once", disc_cnt() - d0, 1, 1);
        held_slew_ = false;
        return check_.report();
    }
'''
anchor = "    int trace(Disturbance kind, int64_t amount_ns) {"
assert src.count(anchor) == 1
src = src.replace(anchor, case + anchor)
hook = '    if (Verilated::commandArgsPlusMatch("slew_suite")[0] != \'\\0\') {'
assert src.count(hook) == 1
src = src.replace(hook, '    if (Verilated::commandArgsPlusMatch("coincide")[0] != \'\\0\') {\n'
                  '        return PhcStepHarness(kHalfPsSuite).coincide();\n    }\n' + hook)
probe_cpp = MS / "sim_phc_coincide_probe.cpp"     # scratch tree only
probe_cpp.write_text(src)

rtl0 = (TREE / "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv").read_text()
variants = {"head": rtl0,
            "mutant_no_step_exclusion": rtl0.replace("slewed_window_w_unused", "")}
a = "slew_window_w && !step_hit_w;"
assert rtl0.count(a) == 1
variants["mutant_no_step_exclusion"] = rtl0.replace(a, "slew_window_w;")
for name, text in variants.items():
    d = W / name
    d.mkdir(exist_ok=True)
    (d / "servo.sv").write_text(text)
    cmd = [VER, "--cc", "--exe", "--build", "-j", "0", "-Wall", "-Wno-fatal",
           "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
           "-Wno-UNUSEDPARAM", "-Wno-EOFNEWLINE", "-Wno-PINCONNECTEMPTY",
           "-CFLAGS", "-std=c++17 -O2", "--public-flat-rw", "--top-module", "KL_mmcm_drp_servo",
           "-Mdir", str(d / "obj"), str(TREE / "hdl/common/cdc_pulse.sv"),
           str(TREE / "hdl/common/cdc_handshake.sv"), str(d / "servo.sv"),
           str(probe_cpp), "-o", "Vprobe"]
    b = subprocess.run(cmd, cwd=MS, capture_output=True, text=True)
    if b.returncode:
        print(name, "BUILD FAIL", b.stderr[-1500:])
        continue
    r = subprocess.run([str(d / "obj/Vprobe"), "+coincide"], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if "[C1]" in l or "RESULT" in l]
    print(f"== {name}: rc={r.returncode}")
    print("\n".join(lines), flush=True)
