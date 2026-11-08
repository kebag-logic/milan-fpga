#!/usr/bin/env python3
"""Compare milan_soc.py's split crossing maps with tb_split_top.sv's instance wiring.

Usage: python3 -I soc_vs_tb_wiring.py <repo-root>
Reads (never imports) sw/litex/milan_soc.py's literal tables _CTRL_CDC_DP,
_CTRL_CDC_MBX, _CTRL_CDC_RESTORE, _CTRL_CDC_NVM and CTRL_SPLIT_PORTS, and the
three instances in tb/verilator/milan_dp/tb_split_top.sv (KL_mbx u_mbx,
KL_mbx_cdc u_cdc, milan_datapath u_dp). For every KL_mbx_cdc port it composes
the net the testbench joins it to with the KL_mbx or milan_datapath port on that
net, and reports every disagreement with the SoC's table. Exit 1 on any.
"""
import ast
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
soc_src = (root / "sw/litex/milan_soc.py").read_text()
tb_src = (root / "tb/verilator/milan_dp/tb_split_top.sv").read_text()

tree = ast.parse(soc_src)
tables = {}
for node in tree.body:
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        tgt = node.targets[0] if isinstance(node, ast.Assign) else node.target
        if isinstance(tgt, ast.Name) and tgt.id in ("_CTRL_CDC_DP", "_CTRL_CDC_MBX", "_CTRL_CDC_RESTORE",
                                                       "_CTRL_CDC_NVM"):
            tables[tgt.id] = ast.literal_eval(node.value)


def instance(text, mod, inst):
    m = re.search(r"\b%s\s+%s\s*\((.*?)\);" % (mod, inst), text, re.S)
    if not m:
        m = re.search(r"\b%s\s*#\(.*?\)\s*%s\s*\((.*?)\);" % (mod, inst), text, re.S)
    body = m.group(1)
    conns = {}
    for pm in re.finditer(r"\.(\w+)\s*(\((?:[^()]|\([^()]*\))*\))?", body):
        port, expr = pm.group(1), pm.group(2)
        conns[port] = expr[1:-1].strip() if expr else port  # .name implicit
    return conns


mbx = instance(tb_src, "KL_mbx", "u_mbx")
cdc = instance(tb_src, "KL_mbx_cdc", "u_cdc")
dp = instance(tb_src, "milan_datapath", "u_dp")
net_to_mbx = {}
for p, n in mbx.items():
    net_to_mbx.setdefault(n, []).append(p)
net_to_dp = {}
for p, n in dp.items():
    net_to_dp.setdefault(n, []).append(p)

bad, checked = [], 0
for cport, mport in tables["_CTRL_CDC_MBX"].items():
    checked += 1
    net = cdc.get(cport)
    tbm = net_to_mbx.get(net, [])
    if mport not in tbm:
        bad.append(f"mailbox side {cport}: SoC binds KL_mbx.{mport}, testbench joins net {net} to {tbm}")
for cport, dport in tables["_CTRL_CDC_DP"].items():
    checked += 1
    net = cdc.get(cport)
    tbd = net_to_dp.get(net, [])
    if dport not in tbd:
        bad.append(f"datapath side {cport}: SoC binds milan_datapath.{dport}, testbench joins net {net} to {tbd}")
# the packed status buses: SoC Cat() is low bit first, the testbench concatenation high bit first
for cport, key in (("m_fw_restore_i", "_CTRL_CDC_RESTORE"), ("m_fw_nvm_i", "_CTRL_CDC_NVM")):
    checked += 1
    nets = [x.strip() for x in cdc[cport].strip("{}").split(",")]
    tb_low_first = [net_to_mbx.get(n, ["?"])[0] for n in reversed(nets)]
    if list(tables[key]) != tb_low_first:
        bad.append(f"{cport}: SoC packs {tables[key]} low bit first, testbench {tb_low_first}")
cdc_ports_tb = {p for p in cdc if p not in ("sys_clk_i", "sys_rst_n", "dp_clk_i", "dp_rst_n")}
soc_named = set(tables["_CTRL_CDC_MBX"]) | set(tables["_CTRL_CDC_DP"]) | {"m_fw_restore_i", "m_fw_nvm_i"}
# the publication inputs and the GM/LINK outputs are bound inline in CtrlMailbox._split
inline = {p for p in cdc_ports_tb if p.startswith("m_pub_") or p in ("m_link_up_o", "m_gm_change_p_o",
                                                                       "m_gm_id_o", "m_gptp_domain_o")}
missing = sorted(cdc_ports_tb - soc_named - inline)
for p in missing:
    bad.append(f"KL_mbx_cdc port {p}: bound in the testbench, named by no SoC table")
print(f"checked {checked} SoC bindings against the testbench; {len(inline)} bound inline in _split (not compared)")
for b in bad:
    print("DISAGREE", b)
print(f"disagreements: {len(bad)}")
sys.exit(1 if bad else 0)
