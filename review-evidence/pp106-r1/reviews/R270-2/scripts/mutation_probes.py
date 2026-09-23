#!/usr/bin/env python3
"""Reviewer-owned mutation probes for PP PR #107 (issue #106), round R270-2.

Each arm is one exact-text substitution (asserted to match exactly once)
planted into a fresh copy of a `git archive` export; the named SRP suites are
built and run with the pinned simulator (-j 8, one build at a time) and the
FAIL count per suite is recorded. The export itself is never modified.

usage: mutation_probes.py <export-dir> <label> <out-dir> [arm-id ...]
"""
import os
import re
import shutil
import subprocess
import sys

# this round ran with VERILATOR=<pinned 5.050 wrapper> (receipts/00)
VERILATOR = os.environ.get("VERILATOR", "verilator")

DEC = "hdl/srp/KL_srp_decoder.sv"
TOP = "hdl/srp/KL_srp_top.sv"
TFSM = "hdl/srp/KL_srp_talker_fsm.sv"
LFSM = "hdl/srp/KL_srp_listener_fsm.sv"
ENC = "hdl/srp/KL_srp_encoder.sv"

ALL = ["srp_decoder", "srp_encoder", "srp_stream_fsms", "srp_top"]

# (id, class, description, [(file, old, new)], suites)
ARMS = [
    ("A1", "X1-class", "any VectorHeader of the type closes the gate",
     [(DEC,
       "              if (la_first_w) begin\n"
       "                la_done_r[la_lane_w] <= 1'b1;\n",
       "              la_done_r[la_lane_w] <= 1'b1;\n"
       "              if (la_first_w) begin\n")], ALL),
    ("A2", "X1-class", "an MSRP lane fires only at the first VectorHeader "
     "of its message (list octet count 1 at VectorHeader byte 2)",
     [(DEC,
       "  assign la_first_w = (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) && !la_done_r[la_lane_w];\n",
       "  assign la_first_w = (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) && !la_done_r[la_lane_w]\n"
       "                   && (!app_msrp_r || (listlen_cnt_r == 16'd1));\n")],
     ["srp_decoder"]),
    ("A3", "X7-class", "gate re-armed only by a clean dual EndMark",
     [(DEC,
       "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n",
       ""),
      (DEC,
       "              pdu_ok_o        <= 1'b1;\n",
       "              pdu_ok_o        <= 1'b1;\n"
       "              la_done_r       <= 4'd0;\n")], ALL),
    ("A4", "X7-class", "gate re-armed only when a PDU closes malformed",
     [(DEC,
       "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n",
       ""),
      (DEC,
       "    pdu_malformed_o <= 1'b1;\n",
       "    pdu_malformed_o <= 1'b1;\n"
       "    la_done_r       <= 4'd0;\n")], ["srp_decoder"]),
    ("A5", "gate scope", "one gate bit for every type (shared gate)",
     [(DEC,
       "&& !la_done_r[la_lane_w];\n",
       "&& !(|la_done_r);\n")], ALL),
    ("A6", "lane position", "lane fires at FirstValue completion, not at the "
     "VectorHeader",
     [(DEC,
       "              if (la_first_w) begin\n"
       "                la_done_r[la_lane_w] <= 1'b1;\n",
       "              if (1'b0) begin\n"
       "                la_done_r[la_lane_w] <= 1'b1;\n"),
      (DEC,
       "            if (fv_idx_r == (attr_len_r[5:0] - 6'd1)) begin\n"
       "              // FirstValue complete\n",
       "            if (fv_idx_r == (attr_len_r[5:0] - 6'd1)) begin\n"
       "              // FirstValue complete\n"
       "              if (la_first_w) begin\n"
       "                la_done_r[la_lane_w] <= 1'b1;\n"
       "                if (app_msrp_r) la_msrp_o[la_lane_w] <= 1'b1;\n"
       "                else            la_mvrp_o            <= 1'b1;\n"
       "              end\n")], ["srp_decoder", "srp_top"]),
    ("A7", "gate scope", "gate re-armed at every new message",
     [(DEC,
       "              attr_type_r <= mrp_data_i;\n",
       "              attr_type_r <= mrp_data_i;\n"
       "              la_done_r   <= 4'd0;\n")], ["srp_decoder"]),
    ("A8", "gate scope", "an MVRP LeaveAll never closes the gate",
     [(DEC,
       "                la_done_r[la_lane_w] <= 1'b1;\n"
       "                if (app_msrp_r)",
       "                if (app_msrp_r) la_done_r[la_lane_w] <= 1'b1;\n"
       "                if (app_msrp_r)")], ["srp_decoder"]),
    ("A9", "X7-class", "gate re-armed at a new MRPDU only when it is MSRP",
     [(DEC,
       "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n",
       "            if (mrp_msrp_i) la_done_r <= 4'd0;\n")], ["srp_decoder"]),
    ("B1", "Domain routing", "Domain participant takes every MSRP lane",
     [(TOP,
       ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
       ".leaveall_tick_i     ((|dec_la_msrp_w) || p_la_msrp_r),")], ALL),
    ("B2", "Domain routing", "Domain participant takes the Listener lane only",
     [(TOP,
       ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
       ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_LISTENER_C] || p_la_msrp_r),")],
     ["srp_top"]),
    ("B3", "VLAN routing", "VLAN participant also takes every MSRP lane",
     [(TOP,
       ".leaveall_tick_i (dec_la_mvrp_w || p_la_mvrp_r),",
       ".leaveall_tick_i (dec_la_mvrp_w || (|dec_la_msrp_w) || p_la_mvrp_r),")],
     ALL),
    ("B4", "Domain routing", "Domain participant deaf to the Domain lane",
     [(TOP,
       ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
       ".leaveall_tick_i     (p_la_msrp_r),")], ["srp_top"]),
    ("C1", "own LeaveAll", "talker registrar no longer aged by an own LeaveAll",
     [(TFSM,
       "  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;\n",
       "  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C];\n")], ALL),
    ("C2", "own LeaveAll", "listener registrar no longer aged by an own LeaveAll",
     [(LFSM,
       "      leaveall_any_w[s] = leaveall_own_i\n"
       "                       || (rtype_r[s]",
       "      leaveall_any_w[s] = 1'b0\n"
       "                       || (rtype_r[s]")], ALL),
    ("C3", "registrar routing", "listener registrar always takes the "
     "Talker Advertise lane",
     [(LFSM,
       "(rtype_r[s] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]",
       "(1'b0 ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]")],
     ["srp_stream_fsms", "srp_top"]),
    ("C4", "applicant routing", "talker applicant always takes the "
     "Talker Advertise lane",
     [(TFSM,
       "      la_rx_app_w[s] = fail_r[s] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]",
       "      la_rx_app_w[s] = 1'b0 ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]")],
     ["srp_stream_fsms", "srp_top"]),
    ("C5", "applicant routing", "listener applicant takes the Domain lane",
     [(LFSM,
       "  assign la_rx_app_w = leaveall_rx_i[SRP_LA_LISTENER_C];\n",
       "  assign la_rx_app_w = leaveall_rx_i[SRP_LA_DOMAIN_C];\n")],
     ["srp_stream_fsms", "srp_top"]),
    ("E1", "encoder", "LeaveAllEvent only on the PDU's first VectorHeader",
     [(ENC,
       "  assign la3_w      = (la_act_r && ((la_types_w & la_bit_w & ~la_seen_r) != '0))\n",
       "  assign la3_w      = (la_act_r && (la_seen_r == 4'b0000))\n")],
     ["srp_encoder", "srp_top"]),
    ("E2", "encoder", "no LeaveAll-only message for an undrained type",
     [(ENC,
       "  assign la_need_w  = la_act_r ? (la_types_w & ~la_seen_r) : 4'b0000;\n",
       "  assign la_need_w  = 4'b0000;\n")], ["srp_encoder", "srp_top"]),
    ("E3", "encoder", "Domain type left out of the MSRP LeaveAll set",
     [(ENC,
       "  localparam logic [3:0]  LA_TYPES_MSRP_C    = 4'b1111;\n",
       "  localparam logic [3:0]  LA_TYPES_MSRP_C    = 4'b0111;\n")],
     ["srp_encoder", "srp_top"]),
]

TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def run_suite(tree, suite):
    d = os.path.join(tree, "tb", suite)
    mk = os.path.join(d, "Makefile")
    with open(mk) as f:
        txt = f.read()
    with open(mk, "w") as f:
        f.write(txt.replace("--build -j 0", "--build -j 8"))
    shutil.rmtree(os.path.join(d, "obj_dir"), ignore_errors=True)
    p = subprocess.run(["make", "VERILATOR=" + VERILATOR], cwd=d,
                       capture_output=True, text=True)
    out = p.stdout + p.stderr
    m = TALLY.findall(out)
    fails = [ln for ln in out.splitlines() if ln.startswith("FAIL")]
    if not m:
        return p.returncode, None, None, fails, out[-1500:]
    n, _, nf = m[-1]
    return p.returncode, int(n), int(nf), fails, ""


def main():
    src, label, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    want = set(sys.argv[4:])
    os.makedirs(outdir, exist_ok=True)
    for aid, cls, desc, subs, suites in ARMS:
        if want and aid not in want:
            continue
        work = os.path.join(outdir, f"{label}-{aid}")
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(src, work, symlinks=True)
        ok = True
        for rel, old, new in subs:
            path = os.path.join(work, rel)
            with open(path) as f:
                txt = f.read()
            cnt = txt.count(old)
            if cnt != 1:
                print(f"{label} {aid} NOT-PLANTED ({rel}: {cnt} matches)")
                ok = False
                break
            with open(path, "w") as f:
                f.write(txt.replace(old, new))
        if not ok:
            shutil.rmtree(work, ignore_errors=True)
            continue
        parts = []
        for s in suites:
            rc, n, nf, fails, tail = run_suite(work, s)
            if n is None:
                parts.append(f"{s}=NO-TALLY(rc={rc})")
                print(f"  {aid} {s} build/run tail:\n{tail}")
            else:
                parts.append(f"{s}={nf}/{n}")
                for ln in fails[:12]:
                    print(f"    {aid} {s} {ln}")
        killed = any(("NO-TALLY" in p) or (not p.endswith(f"=0/{p.split('/')[-1]}"))
                     for p in parts)
        verdict = "KILLED" if killed else "SURVIVES"
        print(f"{label} {aid} [{cls}] {desc}: {' '.join(parts)} -> {verdict}")
        sys.stdout.flush()
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
