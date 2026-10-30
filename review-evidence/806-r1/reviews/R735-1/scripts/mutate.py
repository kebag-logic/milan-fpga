#!/usr/bin/env python3
"""Apply one reviewer probe to a disposable copy of the reviewed tree.

Usage: mutate.py <tree-root> <probe-id>

Each probe is an exact text replacement that must match exactly once, so
a probe that no longer applies fails loudly instead of running clean.
Probes C0 (clean) apply nothing.
"""

import pathlib
import sys

DP = "hdl/milan/milan_datapath.sv"
SH = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
GEN = "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
ENG = "gptp-processor/hdl/top/KL_gptp_engine.sv"
SIM = "tb/verilator/milan_dp/sim_gptp.cpp"

DP_PORT = "        .port_enabled_i  (eff_link_w),\n"


def dp(expr):
    return [(DP, DP_PORT, f"        .port_enabled_i  ({expr}),\n")]


EDGE = "      if (port_ref_r && (port_enabled_i != port_en_r)) begin\n"
CANCEL = "      .cancel_i   (!port_en_r),\n"
CREDIT = "          st_rd_mux_w = {63'd0, tx_credit_i && port_en_r};\n"

# Diagnostic: print the measured quantities the #94 checks grade.
DIAG = [
    (SIM,
     "    expect(\"#94 a link loss inside the cease ends it: a Pdelay_Req within \"\n",
     "    std::printf(\"DIAG toggle last=%llu back=%llu req=%llu req-back=%lld\\n\",\n"
     "                (unsigned long long)last, (unsigned long long)back,\n"
     "                (unsigned long long)req, (long long)(req - back));\n"
     "    expect(\"#94 a link loss inside the cease ends it: a Pdelay_Req within \"\n"),
    (SIM,
     "    expect(\"#94 the cease countdown exit is unchanged: 5 s from the last \"\n",
     "    std::printf(\"DIAG countdown last=%llu req=%llu req-last=%lld\\n\",\n"
     "                (unsigned long long)last, (unsigned long long)req,\n"
     "                (long long)(req - last));\n"
     "    expect(\"#94 the cease countdown exit is unchanged: 5 s from the last \"\n"),
]

PROBES = {
    "C0": [],
    "C0_lat": [],
    # ---- parent wiring ----
    "W1_tie_high": dp("1'b1"),
    "W2_phy_only": dp("i_link_up"),
    "W3_no_guard": dp("i_link_up & cfg_sw_link"),
    "W4_no_linkctrl": dp("i_link_up & (cfg_linkg_dis | linkg_est_w)"),
    "W5_no_phy": dp("cfg_sw_link & (cfg_linkg_dis | linkg_est_w)"),
    "W6_tie_low": dp("1'b0"),
    "W7_shadow_ignores": [(SH, "      .port_enabled_i     (port_enabled_i),\n",
                           "      .port_enabled_i     (1'b1),\n")],
    # ---- engine, the donor's planted texts ----
    "E1_edge_keeps_cease": [(GEN,
        "    for s in (S_CEASE, S_CEASECNT, S_MULTI, S_RSPSEQ):\n",
        "    for s in (S_CEASECNT, S_MULTI, S_RSPSEQ):\n")],
    "E2_fall_no_event": [(ENG, EDGE,
        "      if (port_ref_r && port_enabled_i && !port_en_r) begin\n")],
    "E3_countdown_short": [(GEN,
        "    p.emit(\"MOVE\", rd=RT, ra=0,"
        " imm=max(1, RUNTIME[\"cease_ms\"] // 1000))\n",
        "    p.emit(\"MOVE\", rd=RT, ra=0,"
        " imm=max(1, RUNTIME[\"cease_ms\"] // 1000 - 1))\n")],
    "E4_slot6_no_leg": [(GEN, "    p.emit(\"BR\", label=LB[\"NOTEN\"])\n",
                         "    p.emit(\"END\")\n")],
    "E5_rise_no_request": [(ENG, "        pe_beat_r  <= port_enabled_i;\n",
                            "        pe_beat_r  <= 1'b0;\n")],
    "E6_disabled_sends": [(ENG, CREDIT, "          st_rd_mux_w = {63'd0, tx_credit_i};\n"),
                          (ENG, CANCEL, "      .cancel_i   (1'b0),\n")],
    # ---- tautology probe: the toggle phase without its toggle ----
    "T1_no_toggle": [(SIM,
        "    dut->i_link_up = 0;\n    run_peer(dut, 500 * kGptpMsCyc);\n",
        "    run_peer(dut, 500 * kGptpMsCyc);\n")],
    "D0_diag": DIAG,
}


def main():
    root = pathlib.Path(sys.argv[1])
    for rel, old, new in PROBES[sys.argv[2]]:
        path = root / rel
        text = path.read_text()
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{sys.argv[2]}: {rel}: pattern matched {n} times")
        path.write_text(text.replace(old, new))
        print(f"applied {sys.argv[2]} to {rel}")


if __name__ == "__main__":
    main()
