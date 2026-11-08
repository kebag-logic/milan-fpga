#!/usr/bin/env python3
"""Reviewer plants for split_cdc_check.py beyond its own twelve.

usage: python3 -I cdc_extra_plants.py <clone root>
Each plant edits a temporary copy of KL_mbx_cdc.sv and must be refused
(expect "refused") or, for the control, accepted (expect "clean").
Needs sv2v v0.0.12 and Yosys v0.66 on PATH.
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("scc", root / "tb/verilator/milan_dp/split_cdc_check.py")
scc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scc)

TAKE = "    else if (fw_take_p_w) fw_r <= fw_bus_w;"
PLANTS = [
    ("control: the tracked capture rewritten as a ternary on the pulse", TAKE,
     "    else fw_r <= fw_take_p_w ? fw_bus_w : fw_r;", "clean"),
    ("mux inputs swapped: held bus taken while the pulse is low", TAKE,
     "    else fw_r <= fw_take_p_w ? fw_r : fw_bus_w;", "refused"),
    ("held bus ANDed with the pulse instead of a mux", TAKE,
     "    else fw_r <= fw_bus_w & {FW_W_C{fw_take_p_w}};", "refused"),
    ("held bus captured on a datapath level that is not the pulse", TAKE,
     "    else if (d_link_up_i) fw_r <= fw_bus_w;", "refused"),
    ("held bus captured on the pulse OR a datapath level", TAKE,
     "    else if (fw_take_p_w | d_link_up_i) fw_r <= fw_bus_w;", "refused"),
    ("another dp flop sampling the held bus through the gated mux", "      ev_dom_r  <= d_gptp_domain_i;",
     "      ev_dom_r  <= fw_take_p_w ? m_fw_identify_i : ev_dom_r;", "refused"),
    ("the commit level m_fw_send_i folded into the captured data", TAKE,
     "    else if (fw_take_p_w) fw_r <= fw_bus_w ^ {FW_W_C{m_fw_send_i}};", "refused"),
]

bad = 0
src = scc.CDC
text = src.read_text()
for name, old, new, expect in PLANTS:
    if text.count(old) != 1:
        print(f"ANCHOR-MISSING {name}")
        bad += 1
        continue
    with tempfile.TemporaryDirectory(prefix="r791-cdc-") as tmp:
        cp = Path(tmp) / src.name
        cp.write_text(text.replace(old, new))
        n, got = scc.run(cp, scc.WIN)
    verdict = "refused" if got else "clean"
    ok = verdict == expect
    bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {verdict} (expected {expect}), {n} sinks")
    for g in got:
        print(f"       {g[:300]}")
print(f"extra plants: {len(PLANTS)}   unexpected: {bad}")
sys.exit(1 if bad else 0)
