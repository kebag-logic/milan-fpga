#!/usr/bin/env python3
"""Rewrite a disposable gptp_txts copy so the PHC-load arm runs alone at a chosen
pad index (env PROBE_IDX) with a chosen guard. usage: guard_probe.py <copy> <guard|keep>"""
import sys
root, guard = sys.argv[1:3]
sim = f"{root}/tb/verilator/gptp_txts/sim_main.cpp"
t = open(sim).read()
old = "if (!loaded && pad_open_ && pad_cur_.gptp && pad_idx_ == 22) {"
assert t.count(old) == 1
# pad_cur_.gptp is only known at octet 21, so before that the arm keys on the frame count alone
t = t.replace(old, 'if (!loaded && pad_open_ && pad_idx_ == kProbeIdx) {')
t = t.replace("void TxtsHarness::prove_phc_load_inside_the_window() {",
              'static const size_t kProbeIdx = std::strtoull(std::getenv("PROBE_IDX"), nullptr, 10);\nvoid TxtsHarness::prove_phc_load_inside_the_window() {')
old = "  prove_launch_reference();\n"
assert t.count(old) == 1
t = t.replace(old, "")
for arm in ("prove_queue_invariance", "prove_bias_over_many_frames", "prove_pads_are_byte_exact", "prove_fragment_aborts",
            "prove_recovery_over_the_production_mac", "prove_full_run_laws"):
    line = f"  {arm}();\n"
    assert t.count(line) == 1, arm
    t = t.replace(line, "")
open(sim, "w").write(t)
if guard != "keep":
    ret = f"{root}/hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
    t = open(ret).read()
    old = "(RECON_NEED_CYC_C > RECON_GUARD_CYC_P) ? RECON_NEED_CYC_C : RECON_GUARD_CYC_P;"
    assert t.count(old) == 1
    open(ret, "w").write(t.replace(old, f"{guard};  // REVIEW PROBE"))
