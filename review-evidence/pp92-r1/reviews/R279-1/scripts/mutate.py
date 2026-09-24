#!/usr/bin/env python3
"""Reviewer mutation probe: copy an extracted head tree, apply ONE exact
string replacement (it must match exactly once), build and run one suite
target, and record the tally and FAIL lines.

usage: mutate.py <head_tree> <scratch_root> <log_dir> <mutant_id>
The mutant table is MUTANTS below; every entry is (file, old, new, suite, target).
Needs PIN_VERILATOR (Verilator 5.050). The head tree itself is never edited.
"""
import os
import re
import shutil
import subprocess
import sys
import time

MUTANTS = {
    # the top's restore_done_o no longer waits for the admission release
    "R1": ("hdl/top/protocol_processor_top.sv",
           "assign restore_done_o = nvm_walk_done_w && lsn_released_w;",
           "assign restore_done_o = nvm_walk_done_w;",
           "tb/pp_top", "run"),
    # the top's restore_busy_o no longer covers the terminal-to-release gap
    "R2": ("hdl/top/protocol_processor_top.sv",
           "assign restore_busy_o = nvm_walk_busy_w\n"
           "                          || (nvm_walk_done_w && !lsn_released_w);",
           "assign restore_busy_o = nvm_walk_busy_w;",
           "tb/pp_top", "run"),
    # the read deadline counts CUMULATIVE stall inside the read phase: progress
    # no longer clears it (a slow but moving device now trips it)
    "R3": ("hdl/acmp/KL_acmp_nvm_shadow.sv",
           "    else if (rs_stall_w && !rs_tmo_w) rs_wd_r <= rs_wd_r + 32'd1;\n"
           "    else                              rs_wd_r <= 32'd0;",
           "    else if (rs_stall_w && !rs_tmo_w) rs_wd_r <= rs_wd_r + 32'd1;\n"
           "    else if (!((hs_r == H_RS_REQ) || (hs_r == H_RS_STREAM)) || rs_tmo_w)"
           " rs_wd_r <= 32'd0;",
           "tb/acmp_nvm", "run"),
    # the deadline one cycle late
    "R4": ("hdl/acmp/KL_acmp_nvm_shadow.sv",
           "(rs_wd_r >= 32'(RS_TMO_CYC_P - 1))",
           "(rs_wd_r >= 32'(RS_TMO_CYC_P))",
           "tb/acmp_nvm", "run"),
    # H_RS_REQ's stall no longer counts the port's done/err pulse cycle
    "R5": ("hdl/acmp/KL_acmp_nvm_shadow.sv",
           "((hs_r == H_RS_REQ) && (nvm_busy_i || nvm_done_i || nvm_err_i))",
           "((hs_r == H_RS_REQ) && nvm_busy_i)",
           "tb/acmp_nvm", "run"),
    # the port's UNFRAMED refusal no longer excludes a same-cycle device error
    "R6": ("hdl/packet_engine/KL_pp_nvm_port.sv",
           "assign refuse_w = ((state_r == S_RHWAIT) && !dev_err_i",
           "assign refuse_w = ((state_r == S_RHWAIT)",
           "tb/nvm_port", "run"),
    # the port names a short header (done before 8 bytes) UNFRAMED
    "R7": ("hdl/packet_engine/KL_pp_nvm_port.sv",
           "  assign refuse_w = ((state_r == S_RHWAIT) && !dev_err_i",
           "  assign refuse_w = ((state_r == S_RHCOLL) && !dev_err_i && dev_done_i"
           " && !(dev_rvalid_i && (hidx_r == 3'd7)))\n"
           "                  || ((state_r == S_RHWAIT) && !dev_err_i",
           "tb/nvm_port", "run"),
    # the top bypasses the gate for the talker-event valid only
    "R8": ("hdl/top/protocol_processor_top.sv",
           ".evt_tk_valid_i        (lsn_evt_tk_valid_w),",
           ".evt_tk_valid_i        (lstn_evt_tk_valid_w),",
           "tb/pp_top", "run"),
    # the top bypasses the gate for the START/STOP valid only
    "R9": ("hdl/top/protocol_processor_top.sv",
           ".strm_set_valid_i      (lsn_strm_valid_w),",
           ".strm_set_valid_i      (strm_set_valid_w),",
           "tb/pp_top", "run"),
    # the top bypasses the gate for the timer expiry only
    "R10": ("hdl/top/protocol_processor_top.sv",
            ".tmr_exp_valid_i       (lsn_exp_valid_w),",
            ".tmr_exp_valid_i       (exp_valid_w),",
            "tb/pp_top", "run"),
    # the arbiter's drain also ends when the port merely reads not-busy
    "R11": ("hdl/packet_engine/KL_pp_nvm_mgr_arb.sv",
            "    end else if (end_w) begin\n      drain_r <= 1'b0;",
            "    end else if (end_w || !p_busy_i) begin\n      drain_r <= 1'b0;",
            "tb/acmp_nvm", "run"),
    # reproductions of the author's nvm_port cause arms (logs not published)
    "C1r": ("hdl/packet_engine/KL_pp_nvm_port.sv",
            "assign nvm_err_cause_o = nvm_err_o ? cause_r : 2'd0;",
            "assign nvm_err_cause_o = 2'd0;",
            "tb/nvm_port", "run"),
    "C2r": ("hdl/packet_engine/KL_pp_nvm_port.sv",
            "    end else if (refuse_w) begin\n      cause_r <= CAUSE_UNFRAMED_C;",
            "    end else if (1'b0) begin\n      cause_r <= CAUSE_UNFRAMED_C;",
            "tb/nvm_port", "run"),
    "C3r": ("hdl/packet_engine/KL_pp_nvm_port.sv",
            "      cause_r <= CAUSE_DEVICE_C;",
            "      cause_r <= CAUSE_UNFRAMED_C;",
            "tb/nvm_port", "run"),
    "C4r": ("hdl/packet_engine/KL_pp_nvm_port.sv",
            "assign nvm_err_cause_o = nvm_err_o ? cause_r : 2'd0;",
            "assign nvm_err_cause_o = cause_r;",
            "tb/nvm_port", "run"),
}


def main():
    head, sroot, logs, mid = sys.argv[1:5]
    f, old, new, suite, target = MUTANTS[mid]
    tree = os.path.join(sroot, "mut-" + mid)
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(head, tree, symlinks=True,
                    ignore=shutil.ignore_patterns("obj_*"))
    path = os.path.join(tree, f)
    src = open(path, encoding="utf-8").read()
    n = src.count(old)
    os.makedirs(logs, exist_ok=True)
    log = os.path.join(logs, mid + ".log")
    if n != 1:
        open(log, "w").write("MATCH COUNT %d, mutant not applied\n" % n)
        print("%s NOT APPLIED (matches=%d)" % (mid, n))
        return 3
    open(path, "w", encoding="utf-8").write(src.replace(old, new))
    t0 = time.time()
    with open(log, "w") as fh:
        fh.write("mutant %s: %s\n--- old\n%s\n+++ new\n%s\n\n" % (mid, f, old, new))
        fh.flush()
        rc = subprocess.call(["make", "VERILATOR=" + os.environ["PIN_VERILATOR"],
                              target], cwd=os.path.join(tree, suite),
                             stdout=fh, stderr=subprocess.STDOUT)
    text = open(log, encoding="utf-8", errors="replace").read()
    tallies = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL|\d+ checks, \d+ failures", text)
    fails = [ln for ln in text.splitlines() if ln.startswith("FAIL")]
    verdict = "KILLED" if rc != 0 else "SURVIVED"
    print("%s %s rc=%d secs=%d %s | %d FAIL lines%s" % (
        mid, verdict, rc, time.time() - t0, " / ".join(tallies), len(fails),
        "".join("\n    " + x[:150] for x in fails[:6])))
    shutil.rmtree(tree, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
