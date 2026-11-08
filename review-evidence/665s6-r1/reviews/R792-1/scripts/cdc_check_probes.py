#!/usr/bin/env python3
"""Reviewer probes of tb/verilator/milan_dp/split_cdc_check.py: does it refuse raw crossings
beyond its own four plants?  Usage: cdc_check_probes.py <repo checkout>

Each probe rewrites one line of a copy of KL_mbx_cdc.sv (never the tracked file), runs the
check's own run() on the copy, and reports whether any finding was raised.  'expect' is what a
check that holds the docstring's rule ("one reading is allowed by name: the settings capture
... enabled by u_fw_req's dest_pulse") would do.
"""
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import split_cdc_check as chk  # noqa: E402

CDC = repo / "hdl/milan/mailbox/KL_mbx_cdc.sv"
TAKE = "    else if (fw_take_p_w) fw_r <= fw_bus_w;"
PROBES = (
    ("control: the tracked text", None, None, "clean"),
    ("fw_r captured every dp cycle, no qualifier at all", TAKE,
     "    else                  fw_r <= fw_bus_w;", "refused"),
    ("fw_r enabled by the raw sys-domain m_fw_send_i", TAKE,
     "    else if (m_fw_send_i) fw_r <= fw_bus_w;", "refused"),
    ("fw_r enabled by the raw sys-domain request pulse", TAKE,
     "    else if (fw_req_p_w) fw_r <= fw_bus_w;", "refused"),
    ("a dp flop not named fw_r sampling the held bus", "      ev_dom_r  <= d_gptp_domain_i;",
     "      ev_dom_r  <= m_fw_identify_i;", "refused"),
)

text = CDC.read_text()
bad = 0
for name, old, new, expect in PROBES:
    src = text
    if old is not None:
        if text.count(old) != 1:
            print(f"ANCHOR-MISSING {name}")
            bad += 1
            continue
        src = text.replace(old, new)
    with tempfile.TemporaryDirectory(prefix="cdc-probe-") as tmp:
        copy = Path(tmp) / "KL_mbx_cdc.sv"
        copy.write_text(src)
        n, found = chk.run(copy, chk.WIN)
    got = "refused" if found else "clean"
    verdict = "as-expected" if got == expect else "HOLE" if expect == "refused" else "SPURIOUS"
    print(f"{verdict:12s} {name}: {got} ({n} sinks)" + "".join(f"\n             {f}" for f in found))
    bad += verdict != "as-expected"
print(f"probes: {len(PROBES)}   departures from the docstring's rule: {bad}")
