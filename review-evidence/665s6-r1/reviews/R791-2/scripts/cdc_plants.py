#!/usr/bin/env python3
"""Reviewer plants against split_cdc_check.py: crossings its four tracked plants do not cover.

Usage: python3 cdc_plants.py <repo-root>
Each arm edits a COPY of KL_mbx_cdc.sv (the tracked file is never written) and
runs split_cdc_check.run() on it, printing whether the check refuses it:
  R1  the held settings bus sampled every datapath cycle (its capture enable
      removed): a raw multi-bit crossing of a bus that moves
  R2  a primitive's destination reset taken from the other domain (u_pub's
      dest_rst_n from sys_rst_n): a synchronous reset crossing raw
  R3  the held bus's capture enabled by a sys-domain level instead of the
      dp-side pulse (m_fw_send_i): a raw enable crossing
A control arm (a comment) must pass the check.
"""
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tb/verilator/milan_dp"))
import split_cdc_check as scc  # noqa: E402

CDC = root / "hdl/milan/mailbox/KL_mbx_cdc.sv"
ARMS = (
    ("control: a comment", "  end : fw_take\n", "  end : fw_take  // planted comment\n", False),
    ("R1 the held bus sampled every dp cycle", "    else if (fw_take_p_w) fw_r <= fw_bus_w;",
     "    else                  fw_r <= fw_bus_w;", True),
    ("R2 u_pub's dest reset from the sys domain",
     "    .dest_clk(dp_clk_i), .dest_rst_n(dp_rst_n), .dest_out(pub_dst_w), .dest_req());",
     "    .dest_clk(dp_clk_i), .dest_rst_n(sys_rst_n), .dest_out(pub_dst_w), .dest_req());", True),
    ("R3 the held bus captured on a sys-domain level", "    else if (fw_take_p_w) fw_r <= fw_bus_w;",
     "    else if (m_fw_send_i) fw_r <= fw_bus_w;", True),
)
text = CDC.read_text()
gaps = 0
for name, old, new, raw in ARMS:
    assert text.count(old) == 1, f"anchor for {name} not found once"
    with tempfile.TemporaryDirectory(prefix="r791-cdc-") as tmp:
        copy = Path(tmp) / "KL_mbx_cdc.sv"
        copy.write_text(text.replace(old, new))
        n, found = scc.run(copy, scc.WIN)
    refused = bool(found)
    verdict = ("refused" if refused else "PASSED the check")
    print(f"{name}: {verdict} ({n} sinks){''.join(chr(10) + '    ' + f for f in found)}")
    if raw and not refused:
        gaps += 1
    if not raw and refused:
        gaps += 1
print(f"raw crossings the check let through: {gaps}")
