#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer fault probes for PR #107 (disposable; never a fix).

Usage: mutation_probes.py <donor clone> <rev> <scratch dir> <verilator dir> [ID ...]

Each probe exports <rev> with `git archive` into <scratch>/mut-<ID>, applies
one textual mutation (asserting it matches exactly once), runs the named
suites through run_srp_suites.sh (serial, Verilator build capped at 8 jobs)
and prints the tallies. The review clone itself is never written.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PROBES = {
    # decoder: the once-per-MRPDU gate is armed by ANY VectorHeader of the
    # type, so a flagged vector after an unflagged one of the same type in
    # one MRPDU never strobes (the documented DLSDU-order layout, 10 §6.5)
    "X1": ("hdl/srp/KL_srp_decoder.sv",
           "              if (la_first_w) begin\n"
           "                la_done_r[la_lane_w] <= 1'b1;\n",
           "              la_done_r[la_lane_w] <= 1'b1;\n"
           "              if (la_first_w) begin\n",
           ["srp_decoder", "srp_top"]),
    # top: the Domain participant takes every MSRP lane
    "X2": ("hdl/srp/KL_srp_top.sv",
           ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
           ".leaveall_tick_i     ((|dec_la_msrp_w) || p_la_msrp_r),",
           ["srp_top"]),
    # listener FSM: the Listener applicant is deaf to the Listener lane
    "X3": ("hdl/srp/KL_srp_listener_fsm.sv",
           "assign la_rx_app_w = leaveall_rx_i[SRP_LA_LISTENER_C];",
           "assign la_rx_app_w = leaveall_rx_i[SRP_LA_DOMAIN_C];",
           ["srp_stream_fsms", "srp_top"]),
    # talker FSM: the Advertise applicant takes the Listener lane
    "X4": ("hdl/srp/KL_srp_talker_fsm.sv",
           "                                 : leaveall_rx_i[SRP_LA_TALKER_ADV_C];",
           "                                 : leaveall_rx_i[SRP_LA_LISTENER_C];",
           ["srp_stream_fsms"]),
    # encoder: LeaveAll-only messages in descending AttributeType order
    "X5": ("hdl/srp/KL_srp_encoder.sv",
           "    for (int i = 3; i >= 0; i--) begin\n      if (la_need_w[i])",
           "    for (int i = 0; i <= 3; i++) begin\n      if (la_need_w[i])",
           ["srp_encoder"]),
    # decoder: the gate is cleared only by a well-formed MRPDU's dual
    # EndMark, not at every MRPDU's first byte (a LeaveAll after a
    # malformed MRPDU)
    "X7": ("hdl/srp/KL_srp_decoder.sv",
           "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n",
           "",
           ["srp_decoder"]),
    # replays of three author arms (own textual equivalents)
    # D2: once-per-MRPDU gate removed
    "A-D2": ("hdl/srp/KL_srp_decoder.sv",
             "(vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) && !la_done_r[la_lane_w];",
             "(vhdr1_r[7:5] == SRP_LEAVEALL_EV_C);",
             ["srp_decoder"]),
    # P2: Domain participant deaf to the Domain lane
    "A-P2": ("hdl/srp/KL_srp_top.sv",
             ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
             ".leaveall_tick_i     (p_la_msrp_r),",
             ["srp_top"]),
    # T2: talker registrar deaf to the Listener lane (takes the Domain lane)
    "A-T2": ("hdl/srp/KL_srp_talker_fsm.sv",
             "assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;",
             "assign leaveall_any_w = leaveall_rx_i[SRP_LA_DOMAIN_C] || leaveall_own_i;",
             ["srp_stream_fsms"]),
}
X7_EXTRA = ("hdl/srp/KL_srp_decoder.sv",
            "              pdu_malformed_o <= 1'b0;\n",
            "              pdu_malformed_o <= 1'b0;\n              la_done_r       <= 4'd0;\n")


def mutate(root, path, old, new):
    p = root / path
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"{path}: pattern matched {n} times")
    p.write_text(s.replace(old, new))


def main():
    clone, rev, scratch, vdir = sys.argv[1:5]
    ids = sys.argv[5:] or list(PROBES)
    for pid in ids:
        path, old, new, suites = PROBES[pid]
        root = Path(scratch) / f"mut-{pid}"
        subprocess.run(["rm", "-rf", str(root)], check=True)
        root.mkdir(parents=True)
        arch = subprocess.run(["git", "-C", clone, "archive", rev],
                              check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(root)], input=arch, check=True)
        mutate(root, path, old, new)
        if pid == "X7":
            mutate(root, *X7_EXTRA)
        out = subprocess.run([str(HERE / "run_srp_suites.sh"), str(root), vdir, *suites],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            if not line.startswith("Verilator"):
                print(f"{pid} {line}")
        for s in suites:
            log = (root / "tb" / s / "run.log").read_text(errors="replace")
            fails = [l for l in log.splitlines() if "FAIL" in l and "checks:" not in l]
            for l in fails[:6]:
                print(f"{pid}   {s}: {l.strip()[:160]}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
