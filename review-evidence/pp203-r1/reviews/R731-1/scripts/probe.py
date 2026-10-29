#!/usr/bin/env python3
"""Reviewer probes: plant one defect per probe in a private copy of the exact-head tree,
run `make -C tb/pp_top reboot`, and record the RBT tally and the failing checks.

usage: probe.py HEAD_TREE SCRATCH_DIR RECEIPT_DIR VERILATOR NAME[,NAME...]
"""
import shutil, subprocess, sys
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
ADP = "hdl/adp/KL_adp_engine.sv"
PROBES = {
    # the gate re-opens once the request is up (quiet only while RB_DEP)
    "p1-quiet-reopens-at-request": (TOP,
        "  assign rbt_quiet_w = ((rbt_st_r == RB_DEP) && !adp_tx_busy_w)\n"
        "                     || (rbt_st_r == RB_REQ);\n",
        "  assign rbt_quiet_w = ((rbt_st_r == RB_DEP) && !adp_tx_busy_w);\n"),
    # the RX gate cuts the frame that is arriving at the acceptance
    "p2-rx-gate-cuts-mid-frame": (TOP,
        "  assign rx_take_w = rx_valid_i && (rx_mid_r ? rx_adm_r : !aecp_reboot_w);\n",
        "  assign rx_take_w = rx_valid_i && !aecp_reboot_w;\n"),
    # ADP's busy level forgets the builder: only the pend bits count
    "p3-adp-busy-without-builder": (ADP,
        "  assign tx_busy_o     = (bld_st_r != B_IDLE) || (|pend_dep_r) || (|pend_avail_r);\n",
        "  assign tx_busy_o     = (|pend_dep_r) || (|pend_avail_r);\n"),
    # the gate closes at RB_DEP's entry, while ADP may still be building
    "p4-quiet-at-dep-entry": (TOP,
        "  assign rbt_quiet_w = ((rbt_st_r == RB_DEP) && !adp_tx_busy_w)\n",
        "  assign rbt_quiet_w = (rbt_st_r == RB_DEP)\n"),
    # RB_DEP forgets the lane queue (only the builder and the flight)
    "p5-dep-without-lane-queue": (TOP,
        "        RB_DEP:  if (!adp_tx_busy_w && (laneq_adp_cnt_r == 4'd0)\n",
        "        RB_DEP:  if (!adp_tx_busy_w\n"),
    # the request is not held: RB_REQ returns to RB_RUN on any rx_* byte
    "p6-request-drops-on-rx": (TOP,
        "        RB_REQ:  ;\n",
        "        RB_REQ:  if (rx_valid_i) rbt_st_r <= RB_RUN;\n"),
    # REBOOT loses its CFG_BARRIER class and global key (the classifier default)
    "p7-reboot-not-a-barrier": (TOP,
        "        16'h0006, 16'h002A: begin\n",
        "        16'h0006: begin\n"),
    # ACQUIRE_ENTITY served by the LOCK program, so it can succeed
    "p8-acquire-served": ("hdl/aecp/KL_aecp_engine.sv",
        "            if (acq_r) begin\n              upc_r <= UPC_NSUPPE_C;\n            end\n",
        "            if (acq_r) begin\n              upc_r <= UPC_LOCKEN_C;\n              echo_r <= 1'b0;\n            end\n"),
}
#: probes graded on more than section RBT
TARGETS = {"p7-reboot-not-a-barrier": ["reboot", "hazards"]}


def main():
    head, scratch, rec, ver, names = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5].split(",")
    for name in names:
        path, old, new = PROBES[name]
        tree = scratch / f"probe_{name}"
        shutil.rmtree(tree, ignore_errors=True)
        shutil.copytree(head, tree, symlinks=True)
        src = tree / path
        text = src.read_text()
        assert text.count(old) == 1, f"{name}: anchor matches {text.count(old)} times"
        src.write_text(text.replace(old, new))
        for d in ("obj_dir",):
            shutil.rmtree(tree / "tb/pp_top" / d, ignore_errors=True)
        log, rc = "", 0
        for target in TARGETS.get(name, ["reboot"]):
            r = subprocess.run(["make", "-C", str(tree / "tb/pp_top"), target, f"VERILATOR={ver}"],
                               capture_output=True, text=True)
            log += f"### make {target}: rc={r.returncode}\n" + r.stdout + r.stderr
            rc = rc or r.returncode
        if name in TARGETS:
            r = subprocess.run(["python3", "-B", "scripts/check_aecp_commands.py"], cwd=tree,
                               capture_output=True, text=True)
            log += f"### check_aecp_commands: rc={r.returncode}\n" + r.stdout + r.stderr
            rc = rc or r.returncode
        r.returncode = rc
        (rec / f"probe_{name}.log").write_text(log)
        tally = [l for l in log.splitlines() if l.startswith(("RBT:", "HZ:", "### "))]
        fails = [l for l in log.splitlines() if l.startswith("FAIL")]
        verdict = "DETECTED" if (r.returncode != 0 and tally and fails) else (
            "SURVIVED" if (r.returncode == 0 and tally) else "NO-TALLY")
        print(f"{name}: rc={r.returncode} {' | '.join(tally) if tally else 'no tally'} {verdict}")
        for l in fails[:6]:
            print("    " + l)
        shutil.rmtree(tree, ignore_errors=True)

if __name__ == "__main__":
    main()
