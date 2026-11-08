#!/usr/bin/env python3
"""Reviewer probes of split_cdc_check.py's held-bus allowance at the round 2 head.

Usage: python3 -I cdc_allowance_probes.py <repo checkout>

Each probe rewrites one anchor of a COPY of KL_mbx_cdc.sv (the tracked file is
never written), runs the check's own run() on the copy and compares the result
with what the check's docstring rule says it must be:
  "refused" - a reading of the held bus, or a clock, the rule does not admit;
  "clean"   - a restructure the rule admits (no false refusal).
A departure is a HOLE (an admitted raw crossing) or SPURIOUS (a refused legal form).
"""
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import split_cdc_check as chk  # noqa: E402

CDC = repo / "hdl/milan/mailbox/KL_mbx_cdc.sv"
TAKE = "    else if (fw_take_p_w) fw_r <= fw_bus_w;"
OUT = "          d_restore_cause_o, d_nvm_o, d_nvm_verdict_o} = fw_r;"
EV = "      ev_dom_r  <= d_gptp_domain_i;"
PROBES = (
    ("control: the tracked text", None, None, "clean"),
    ("legal: the hold written out as an else branch", TAKE,
     "    else if (fw_take_p_w) fw_r <= fw_bus_w;\n    else                  fw_r <= fw_r;", "clean"),
    ("legal: the taken bus mixed with a datapath flop", TAKE,
     "    else if (fw_take_p_w) fw_r <= fw_bus_w ^ {FW_W_C{ev_dom_r[0]}};", "clean"),
    ("the held bus on the gated mux's untaken input", TAKE,
     "    else                  fw_r <= fw_take_p_w ? fw_r : fw_bus_w;", "refused"),
    ("the taken bus mixed with a sys flop", TAKE,
     "    else if (fw_take_p_w) fw_r <= fw_bus_w ^ {FW_W_C{fw_send_q_r}};", "refused"),
    ("an output reading the held bus through the gated mux", OUT,
     "          d_restore_cause_o, d_nvm_o, d_nvm_verdict_o} = fw_take_p_w ? fw_bus_w : fw_r;", "refused"),
    ("the capture selected by the acknowledgement's pulse", TAKE,
     "    else if (m_fw_ack_p_o) fw_r <= fw_bus_w;", "refused"),
    ("the capture selected by a one-cycle-late copy of the pulse",
     (TAKE, "  logic fw_send_q_r, fw_req_p_w, fw_take_p_w;"),
     ("    else if (ev_late_p_r) fw_r <= fw_bus_w;",
      "  logic fw_send_q_r, fw_req_p_w, fw_take_p_w, ev_late_p_r;\n"
      "  always_ff @(posedge dp_clk_i) ev_late_p_r <= fw_take_p_w;"), "refused"),
    ("the capture selected by the pulse AND a datapath level", TAKE,
     "    else if (fw_take_p_w && d_link_up_i) fw_r <= fw_bus_w;", "refused"),
    ("another datapath flop taking the held bus on the gate", EV,
     "      ev_dom_r  <= fw_take_p_w ? m_fw_identify_i : d_gptp_domain_i;", "refused"),
    ("a flop clocked by a gated datapath clock", "  always_ff @(posedge dp_clk_i) begin : fw_take",
     "  wire gclk_w = dp_clk_i & dp_rst_n;\n  always_ff @(posedge gclk_w) begin : fw_take", "refused"),
)

text = CDC.read_text()
bad = 0
for name, old, new, expect in PROBES:
    src = text
    pairs = [] if old is None else list(zip(old, new)) if isinstance(old, tuple) else [(old, new)]
    if any(text.count(o) != 1 for o, _ in pairs):
        print(f"ANCHOR-MISSING {name}")
        bad += 1
        continue
    for o, n_ in pairs:
        src = src.replace(o, n_)
    with tempfile.TemporaryDirectory(prefix="r792-2-cdc-") as tmp:
        copy = Path(tmp) / "KL_mbx_cdc.sv"
        copy.write_text(src)
        try:
            n, found = chk.run(copy, chk.WIN)
        except Exception as exc:  # an elaboration failure is reported, not hidden
            print(f"ERROR        {name}: {type(exc).__name__}: {str(exc)[:300]}")
            bad += 1
            continue
    got = "refused" if found else "clean"
    verdict = "as-expected" if got == expect else "HOLE" if expect == "refused" else "SPURIOUS"
    print(f"{verdict:12s} {name}: {got} ({n} sinks)" + "".join(f"\n             {f}" for f in found))
    bad += verdict != "as-expected"
print(f"probes: {len(PROBES)}   departures from the docstring's rule: {bad}")
