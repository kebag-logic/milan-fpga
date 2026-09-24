#!/usr/bin/env python3
"""Disposable hang probes for the three runners whose host deadlines PR #117 drops.

Usage: hang_probe.py <processor-tree> <scratch-dir> <out-dir> <probe-name>

Each probe copies the processor tree, applies ONE exact source edit chosen to
starve the harness of the progress it waits for, then runs the same bench
command the runner would run. The run is wrapped in an OUTER safety-net
`timeout` only so a hang is observable (exit 124) instead of wedging the
review; the runners themselves carry no deadline at the reviewed head.

Probes named *-stall must TERMINATE (exit != 124): they are inside each
runner's mutation surface (or, for GSI, anywhere), so the head's comments
claim termination by construction. The probe named srp-top-timer-scope edits
the timer service, which the SRP runner never mutates: it shows the scope of
that runner's argument (its waits on the timer cadence are real).
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

GUARD = "hdl/aecp/KL_aecp_desc_mem_guard.sv"
TOP = "hdl/top/protocol_processor_top.sv"
ADM = "hdl/srp/KL_srp_admission.sv"
TMR = "hdl/common/KL_pp_timer_service.sv"

PROBES = {
    # memory is never asked for anything: every store read starves
    "desc-guard-no-request-stall": (GUARD,
        "assign m_req_valid_o = s_req_valid_i && !owed_r;",
        "assign m_req_valid_o = 1'b0;",
        "tb/desc_mem_guard", ["make", "run", "GUARD_SRC=../../" + GUARD,
                              "OBJ_DIR=obj_probe", "ARGS=--late-only"]),
    # the binding walk never completes: boot and every later wait starve
    "gsi-restore-never-done-stall": (TOP,
        "assign restore_done_o = nvm_walk_done_w && lsn_released_w;",
        "assign restore_done_o = 1'b0;",
        "tb/pp_top", ["sh", "-c", "make gsi-build && ./obj_dir/Vpp_top_sim --gsi-internal-only"]),
    # the ms timebase never advances inside the whole processor
    "gsi-timer-frozen-stall": (TMR,
        "now_ms_r <= now_ms_r + 32'd1;",
        "now_ms_r <= now_ms_r;",
        "tb/pp_top", ["sh", "-c", "make gsi-build && ./obj_dir/Vpp_top_sim --gsi-internal-only"]),
    # admission never publishes a round: no grant ever rises, no strobe
    "srp-adm-never-publish-stall-admission": (ADM,
        "if (!(pend_acc_r || pend_w)) begin",
        "if (1'b0) begin",
        "tb/srp_admission", ["make", "run", "N=8"]),
    "srp-adm-never-publish-stall-top": (ADM,
        "if (!(pend_acc_r || pend_w)) begin",
        "if (1'b0) begin",
        "tb/srp_top", ["make", "run"]),
    # admission flips every grant each published round: a Failed/Advertise storm
    "srp-adm-grant-flap-stall-top": (ADM,
        "grant_r      <= wgrant_now_w;",
        "grant_r      <= ~grant_r;",
        "tb/srp_top", ["make", "run"]),
    # OUTSIDE the SRP runner's surface: frozen timebase stops the join cadence
    "srp-top-timer-scope": (TMR,
        "now_ms_r <= now_ms_r + 32'd1;",
        "now_ms_r <= now_ms_r;",
        "tb/srp_top", ["make", "run"]),
}


def main() -> int:
    src, scratch, out, name = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    path, old, new, suite, cmd = PROBES[name]
    tree = scratch / f"probe-{name}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(src, tree, ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    text = (tree / path).read_text()
    if text.count(old) != 1:
        raise SystemExit(f"{name}: anchor count {text.count(old)} != 1")
    (tree / path).write_text(text.replace(old, new))
    out.mkdir(parents=True, exist_ok=True)
    log = out / f"{name}.log"
    limit = 540
    start = time.monotonic()
    with log.open("w") as stream:
        rc = subprocess.run(["timeout", str(limit)] + cmd, cwd=tree / suite,
                            stdout=stream, stderr=subprocess.STDOUT).returncode
    wall = round(time.monotonic() - start, 1)
    tally = [ln for ln in log.read_text().splitlines() if "checks" in ln][-3:]
    rec = {"probe": name, "file": path, "edit": [old, new], "suite": suite,
           "command": cmd, "safety_net_s": limit, "exit": rc, "wall_s": wall,
           "hung": rc == 124, "tally": tally}
    (out / f"{name}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(json.dumps(rec))
    shutil.rmtree(tree)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
