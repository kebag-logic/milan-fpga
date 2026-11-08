#!/usr/bin/env python3
"""Reviewer probe: every port name milan_soc.py's split binding uses exists on its module.

Usage: python3 -I split_port_names.py <repo checkout>

Reads (never imports) sw/litex/milan_soc.py and collects:
  - each name in CTRL_SPLIT_PORTS, which must be a milan_datapath port;
  - each key of _CTRL_CDC_DP, _CTRL_CDC_MBX, _CTRL_CDC_RESTORE and _CTRL_CDC_NVM and each
    i_/o_ keyword of the KL_mbx_cdc Instance, which must be KL_mbx_cdc ports;
  - each value of _CTRL_CDC_DP, which must be a milan_datapath port.
Prints every name that is not a port, and the unit-bearing names found. Exit 1 on any miss.
"""
import ast
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
soc = (root / "sw/litex/milan_soc.py").read_text()
PORT = re.compile(r"^\s*(?:input|output|inout)\s+(?:wire|logic|reg)?\s*(?:signed\s+)?(?:\[[^\]]*\]\s*)*(\w+)", re.M)


def ports(path: str) -> set:
    """The port names a module's ANSI header declares."""
    return set(PORT.findall((root / path).read_text()))


dp = ports("hdl/milan/milan_datapath.sv")
cdc = ports("hdl/milan/mailbox/KL_mbx_cdc.sv")
tables = {}
for node in ast.parse(soc).body:
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        tgt = node.targets[0] if isinstance(node, ast.Assign) else node.target
        if isinstance(tgt, ast.Name) and tgt.id in ("CTRL_SPLIT_PORTS", "_CTRL_CDC_DP", "_CTRL_CDC_MBX",
                                                     "_CTRL_CDC_RESTORE", "_CTRL_CDC_NVM"):
            v = node.value
            if isinstance(v, ast.Dict):
                tables[tgt.id] = {k.value: x.value for k, x in zip(v.keys, v.values)
                                  if isinstance(k, ast.Constant) and isinstance(x, ast.Constant)}
            else:
                tables[tgt.id] = [(e.elts[0].value,) for e in v.elts if isinstance(e, ast.Tuple)]
miss = []
split_names = [t[0] for t in tables["CTRL_SPLIT_PORTS"]]
miss += [f"CTRL_SPLIT_PORTS {n} is not a milan_datapath port" for n in split_names if n not in dp]
for name in ("_CTRL_CDC_DP", "_CTRL_CDC_MBX", "_CTRL_CDC_RESTORE", "_CTRL_CDC_NVM"):
    for k in tables.get(name, {}):
        if k not in cdc:
            miss.append(f"{name} key {k} is not a KL_mbx_cdc port")
for k, v in tables.get("_CTRL_CDC_DP", {}).items():
    if v not in dp:
        miss.append(f"_CTRL_CDC_DP value {v} (for {k}) is not a milan_datapath port")
inst = soc[soc.index('Instance("KL_mbx_cdc"'):]
inst = inst[:inst.index("\n        )")] if "\n        )" in inst else inst[:6000]
kw = re.findall(r"\b([io]_(?:[md]_\w+?))=", inst)
for k in kw:
    if k[2:] not in cdc:
        miss.append(f"KL_mbx_cdc Instance keyword {k} names no KL_mbx_cdc port")
units = sorted(n for n in split_names + list(tables.get("_CTRL_CDC_DP", {})) + [k[2:] for k in kw]
               if "idle_slope" in n or "pt_offset" in n)
print(f"datapath ports {len(dp)}, KL_mbx_cdc ports {len(cdc)}; CTRL_SPLIT_PORTS {len(split_names)}, "
      f"Instance keywords {len(kw)}")
print("unit-bearing names:", ", ".join(units))
print("\n".join(miss) if miss else "every name is a port")
print(f"misses: {len(miss)}")
sys.exit(1 if miss else 0)
