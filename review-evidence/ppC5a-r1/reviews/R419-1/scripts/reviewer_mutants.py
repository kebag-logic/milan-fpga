#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer (R419-1) mutation probes on the C5a deadline seam.

Each arm replaces one exact source fragment (it must match exactly once) in a
fresh scratch copy of hdl/ + tb/{common,ucpu,pp_top} taken from <tree>, runs
the named make targets, and reports every FAIL line. An arm is KILLED when a
completed run (a tally printed) exits non-zero with at least one FAIL line.

Usage: reviewer_mutants.py <tree> <out-dir> [arm,...]
Environment: VERILATOR on PATH; TMPDIR for the scratch copies.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

ENG = "hdl/aecp/KL_aecp_engine.sv"
TOP = "hdl/top/protocol_processor_top.sv"
UCPU = "hdl/aecp/KL_aecp_ucpu.sv"

ARMS = {
    # the design exempts REGISTER/DEREGISTER and LOCK_ENTITY from preemption
    # (registry face = point of no return); only the map edit is graded (DL6)
    "r-registry-lock-preempted": (
        ENG, "&& !regun_r && !lockc_r && !amap_edit_r;",
        "&& !amap_edit_r;",
        [("pp_top", "deadline"), ("ucpu", "run")]),
    # effect-op list without COMMIT, NVM_MARK and NOTIFY_ENQ
    "r-effects-short": (
        UCPU,
        "assign pre_eff_w = uop_e_r.op inside {OP_WRITE_ST, OP_NAME_WR, OP_COMMIT,\n"
        "                                        OP_NVM_MARK, OP_NOTIFY_ENQ,\n"
        "                                        OP_SEND_RESP, OP_END};",
        "assign pre_eff_w = uop_e_r.op inside {OP_WRITE_ST, OP_NAME_WR,\n"
        "                                        OP_SEND_RESP, OP_END};",
        [("pp_top", "deadline"), ("ucpu", "run")]),
    # the owner block no longer ends the AECP owner on an honoured kill
    "r-kill-ack-keeps-owner": (
        TOP, "if (sb_rel_aecp_w || sb_kill_ack_w) begin",
        "if (sb_rel_aecp_w) begin",
        [("pp_top", "deadline")]),
    # an unsolicited hand-off counts as the forced response's hand-off
    "r-queued-counts-unsolicited": (
        ENG, "assign dl_queued_o    = (a_st_r == A_TXW) && !uns_r && txreq_ready_i;",
        "assign dl_queued_o    = (a_st_r == A_TXW) && txreq_ready_i;",
        [("pp_top", "deadline")]),
    # the kill is latched during an unsolicited job too
    "r-kill-latched-unsolicited": (
        ENG, "else if (dl_kill_i && !uns_r) dl_kill_r <= 1'b1;",
        "else if (dl_kill_i) dl_kill_r <= 1'b1;",
        [("pp_top", "deadline")]),
    # a preempted MVU command keeps status 10's header-only form, no echo
    "r-mvu-no-echo": (
        ENG,
        "                status_r <= ST_NOT_IMPLEMENTED_C;\n"
        "                echo_r   <= 1'b1;\n"
        "                pld_r    <= pld_cmd_r;",
        "                status_r <= ST_NOT_IMPLEMENTED_C;",
        [("pp_top", "deadline")]),
}


def main() -> int:
    src = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]).resolve()
    only = sys.argv[3].split(",") if len(sys.argv) > 3 else list(ARMS)
    out.mkdir(parents=True, exist_ok=True)
    worst = 0
    for arm in only:
        path, old, new, targets = ARMS[arm]
        with tempfile.TemporaryDirectory(prefix="r419-mut-") as tmp:
            tree = pathlib.Path(tmp)
            shutil.copytree(src / "hdl", tree / "hdl")
            for s in ("common", "ucpu", "pp_top"):
                shutil.copytree(src / "tb" / s, tree / "tb" / s,
                                ignore=shutil.ignore_patterns("obj_*", "*.hex"))
            f = tree / path
            text = f.read_text()
            n = text.count(old)
            if n != 1:
                print(f"{arm}: fragment matched {n} times, arm NOT RUN")
                worst = 2
                continue
            f.write_text(text.replace(old, new, 1))
            for suite, target in targets:
                log = out / f"{arm}-{suite}-{target}.log"
                with log.open("w") as fh:
                    rc = subprocess.run(["make", "-C", str(tree / "tb" / suite),
                                         target], stdout=fh,
                                        stderr=subprocess.STDOUT).returncode
                body = log.read_text()
                fails = [l for l in body.splitlines() if l.startswith("FAIL:")]
                done = "checks" in body
                verdict = ("KILLED" if rc != 0 and done and fails
                           else "SURVIVED" if rc == 0 and done
                           else "INCOMPLETE")
                print(f"{arm} [{suite} {target}]: rc={rc} failures={len(fails)} {verdict}")
                for l in fails[:12]:
                    print(f"    {l}")
    return worst


if __name__ == "__main__":
    sys.exit(main())
