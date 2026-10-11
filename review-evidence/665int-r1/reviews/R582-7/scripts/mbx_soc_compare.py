#!/usr/bin/env python3
"""mbx_soc_compare.py DIR - compare mbx_soc_probe.py's on/off records.

For every config: --ctrl-mailbox adds exactly the ctrl_mbx region, CSR bank
and interrupt and moves none of the others; the storage arrays (the M2 MAC
and CSR crossings among them) are identical on and off; the M2 split is
present (the 72-bit MAC payloads and the CSR W/R payloads in block RAM, the
framing flags in distributed RAM, every split array read READ_FIRST); and the
KL_mbx publication outputs have the widths the contract states.
Exit 1 on any difference.
"""
import json
import os
import sys

d = sys.argv[1]
sys.path.insert(0, os.path.join(sys.argv[2], "sw/mailbox"))
from mailbox_model import load  # noqa: E402

contract = load()
n_if = contract.interfaces
pub_w = {(r.name, f.name): f.width for r in contract.pub_registers for f in r.fields}
want_pub = {
    "pub_da_gate_o": n_if * contract.pub_sources,
    "pub_licence_o": n_if * contract.pub_sources,
    "pub_idle_slope_bps_o": n_if * pub_w[("IDLE_SLOPE", "BPS")],
    "pub_dom_vid_o": n_if * pub_w[("SR_DOMAIN", "VID")],
    "pub_dom_prio_o": n_if * pub_w[("SR_DOMAIN", "PRIORITY")],
    "pub_dom_adopted_o": n_if * pub_w[("SR_DOMAIN", "ADOPTED")],
    "pub_talker_decl_o": n_if * contract.pub_sources,
    "pub_bound_o": n_if * contract.pub_sinks,
    "pub_sid_valid_o": n_if * contract.pub_sinks,
    "pub_started_o": n_if * contract.pub_sinks,
    "pub_sid_o": n_if * contract.pub_sinks * 64,
}
bad = []
configs = sorted({f.split(".")[0] for f in os.listdir(d) if f.endswith(".json")})
for c in configs:
    on = json.load(open(os.path.join(d, f"{c}.on.json")))
    off = json.load(open(os.path.join(d, f"{c}.off.json")))
    if not on["has_ctrl_mbx"] or off["has_ctrl_mbx"]:
        bad.append(f"{c}: ctrl_mbx presence on={on['has_ctrl_mbx']} off={off['has_ctrl_mbx']}")
    for key in ("regions", "csr", "irq"):
        a = {k: v for k, v in on[key].items() if k != "ctrl_mbx"}
        if a != off[key]:
            bad.append(f"{c}: {key} other than ctrl_mbx differ on/off")
        if key != "irq" or on["irq"]:
            if "ctrl_mbx" not in on[key]:
                bad.append(f"{c}: no ctrl_mbx in {key} with the switch on")
    for o in (on, off):
        if o["overlaps"]:
            bad.append(f"{c}: overlapping regions {o['overlaps']}")
    if on["arrays"] != off["arrays"]:
        bad.append(f"{c}: storage arrays differ with the mailbox on")
    split = [a for a in on["arrays"] if a["attr"]]
    shape = sorted((a["path"].split(".")[2], a["width"], a["depth"], a["attr"][0]) for a in split)
    want = sorted([
        ("mac_rx_cdc", 72, 16, "('ram_style', 'block')"), ("mac_rx_cdc", 2, 16, "('ram_style', 'distributed')"),
        ("mac_tx_cdc", 72, 16, "('ram_style', 'block')"), ("mac_tx_cdc", 2, 16, "('ram_style', 'distributed')"),
        ("milan_axil_cdc", 34, 4, "('ram_style', 'block')"), ("milan_axil_cdc", 2, 4, "('ram_style', 'distributed')"),
        ("milan_axil_cdc", 36, 4, "('ram_style', 'block')"), ("milan_axil_cdc", 2, 4, "('ram_style', 'distributed')"),
    ])
    if shape != want:
        bad.append(f"{c}: M2 split arrays {shape}")
    # migen: READ_FIRST == 0; ports are [write, read]
    if any(a["ports"][1]["mode"] != 0 or a["ports"][1]["we"] or a["ports"][1]["async"] for a in split):
        bad.append(f"{c}: a split array's read port is not synchronous READ_FIRST")
    ports = {p[0]: (p[1], p[2]) for p in on["mbx_instances"]["KL_mbx"]}
    if any(p[3] and p[1] != "Input" for p in on["mbx_instances"]["KL_mbx"]):
        bad.append(f"{c}: an output bound to a constant")
    for name, w in want_pub.items():
        if ports.get(name) != ("Output", w):
            bad.append(f"{c}: KL_mbx.{name} {ports.get(name)} want Output {w}")
    region = on["regions"]["ctrl_mbx"]
    print(f"{c}: ctrl_mbx region 0x{region[0]:08x}+0x{region[1]:x}, csr {on['csr'].get('ctrl_mbx')}, "
          f"irq {on['irq'].get('ctrl_mbx')}, {len(on['arrays'])} arrays identical on/off, "
          f"M2 split arrays {len(split)}, KL_mbx {len(ports)} ports")
print(f"{len(configs)} config(s); {len(bad)} difference(s)")
for b in bad:
    print("  BAD", b)
sys.exit(1 if bad or len(configs) != 5 else 0)
