#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned mutation probes for PR #107 (issue #106) at fc155c3c.

Each mutant is applied to a fresh copy of the exported head tree (never to
the review clone), the four SRP suites are built and run with the pinned
simulator, and the per-suite tallies are recorded. A mutant whose planted
string does not occur exactly once is refused, not run.

Usage: 03_mutate.py <head-tree> <scratch-dir> <verilator> <out.txt> [ids...]
"""
import concurrent.futures as cf
import pathlib
import re
import shutil
import subprocess
import sys

SUITES = ["srp_decoder", "srp_encoder", "srp_stream_fsms", "srp_top"]

MUTANTS = {
    # decoder: an unflagged vector of type T consumes T's once-per-MRPDU
    # budget, so a LeaveAll on a LATER vector of T in the same MRPDU is lost
    "R1": ("hdl/srp/KL_srp_decoder.sv",
           "              if (la_first_w) begin\n"
           "                la_done_r[la_lane_w] <= 1'b1;\n",
           "              la_done_r[la_lane_w] <= 1'b1;\n"
           "              if (la_first_w) begin\n"),
    # talker FSM: a lane landing on a busy applicant is deferred whatever
    # its type (the deferral ignores the per-type routing)
    "R2": ("hdl/srp/KL_srp_talker_fsm.sv",
           "        if (la_rx_app_w[s] && !rla_grant_w[s]",
           "        if ((|leaveall_rx_i) && !rla_grant_w[s]"),
    # listener FSM: the same deferral, any lane
    "R3": ("hdl/srp/KL_srp_listener_fsm.sv",
           "        if (la_rx_app_w && !rla_grant_w[s]",
           "        if ((|leaveall_rx_i) && !rla_grant_w[s]"),
    # top: the Domain participant takes every MSRP lane
    "R4": ("hdl/srp/KL_srp_top.sv",
           ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
           ".leaveall_tick_i     ((|dec_la_msrp_w) || p_la_msrp_r),"),
    # top: the VLAN (MVRP) participant also takes the MSRP lanes
    "R5": ("hdl/srp/KL_srp_top.sv",
           ".leaveall_tick_i (dec_la_mvrp_w || p_la_mvrp_r),",
           ".leaveall_tick_i (dec_la_mvrp_w || (|dec_la_msrp_w) || p_la_mvrp_r),"),
    # encoder: a LeaveAll on the drain's start cycle is taken AND re-latched
    "R6": ("hdl/srp/KL_srp_encoder.sv",
           "      if (leaveall_i[0] && !start0_w) la_pend_r[0] <= 1'b1;",
           "      if (leaveall_i[0]) la_pend_r[0] <= 1'b1;"),
    # encoder: LeaveAll-only messages in DESCENDING AttributeType order
    "R7": ("hdl/srp/KL_srp_encoder.sv",
           "    for (int i = 3; i >= 0; i--) begin\n"
           "      if (la_need_w[i]) la_next_w = 8'(i + 1);",
           "    for (int i = 0; i <= 3; i++) begin\n"
           "      if (la_need_w[i]) la_next_w = 8'(i + 1);"),
    # decoder: the once-per-MRPDU gate re-armed only by a clean dual EndMark,
    # not at every new MRPDU (a malformed PDU leaves the gate closed)
    "R8": ("hdl/srp/KL_srp_decoder.sv",
           "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n",
           "\n"),
    # encoder: the LeaveAll-only vector's NumberOfValues-0 path writes one
    # (zero) ThreePacked octet
    "R9": ("hdl/srp/KL_srp_encoder.sv",
           "            if (run_len_r == '0) st_r <= E_MSGCLOSE;\n"
           "            else                 st_r <= E_V3PK;",
           "            st_r <= E_V3PK;"),
    # talker FSM: an own LeaveAll ages the Listener registrar only through
    # the received Listener lane (own LeaveAll dropped from the registrar)
    "R10": ("hdl/srp/KL_srp_talker_fsm.sv",
            "  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;",
            "  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C];"),
    # listener FSM: an own LeaveAll no longer ages the talker registrars
    "R11": ("hdl/srp/KL_srp_listener_fsm.sv",
            "      leaveall_any_w[s] = leaveall_own_i\n                       || ",
            "      leaveall_any_w[s] = 1'b0\n                       || "),
}

# R8 also needs the gate cleared at the clean close so the decoder still
# works for well-formed traffic: plant it next to pdu_ok_o <= 1
R8_EXTRA = ("hdl/srp/KL_srp_decoder.sv",
            "              pdu_ok_o        <= 1'b1;\n",
            "              pdu_ok_o        <= 1'b1;\n              la_done_r       <= 4'd0;\n")


def plant(tree, path, old, new):
    f = tree / path
    s = f.read_text()
    n = s.count(old)
    if n != 1:
        raise SystemExit("refused: %s occurs %d times in %s" % (old[:60], n, path))
    f.write_text(s.replace(old, new))


def run_suite(tree, vl, s):
    d = tree / "tb" / s
    subprocess.run(["make", "clean"], cwd=d, capture_output=True)
    p = subprocess.run(["make", "VERILATOR=%s" % vl], cwd=d, capture_output=True, text=True)
    log = p.stdout + p.stderr
    (tree / ("%s.log" % s)).write_text(log)
    m = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", log)
    if m:
        return s, "%s/%s FAIL" % (m[-1][2], m[-1][0])
    return s, "NO-TALLY rc=%d" % p.returncode


def main():
    head = pathlib.Path(sys.argv[1])
    scratch = pathlib.Path(sys.argv[2])
    vl = sys.argv[3]
    out = pathlib.Path(sys.argv[4])
    ids = sys.argv[5:] or list(MUTANTS)
    lines = []
    for mid in ids:
        tree = scratch / ("mut-" + mid)
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(head, tree, symlinks=True)
        path, old, new = MUTANTS[mid]
        plant(tree, path, old, new)
        if mid == "R8":
            plant(tree, *R8_EXTRA)
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            res = dict(ex.map(lambda s: run_suite(tree, vl, s), SUITES))
        killed = any(not v.startswith("0/") for v in res.values())
        line = "%-4s %-8s %s" % (mid, "KILLED" if killed else "SURVIVED",
                                 "  ".join("%s=%s" % (s, res[s]) for s in SUITES))
        print(line, flush=True)
        lines.append(line)
    out.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
