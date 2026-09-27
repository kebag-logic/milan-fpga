#!/usr/bin/env python3
"""R357-1: from a Verilator --json-only tree of KL_pp_shadow, report the
elaborated values of N_AUDIO_UNIT_P / N_CLK_DOMAIN_P / N_CONTROL_P in every
specialized KL_aecp_dyn_state, KL_aecp_engine and protocol_processor_top
module, and N_AUDIO_UNIT_P / N_CLK_DOM_P / N_CONTROL_P on the KL_pp_shadow top.
Usage: probe_json_params.py <VKL_pp_shadow.tree.json>"""
import json, sys
tree = json.load(open(sys.argv[1]))
WANT = {"N_AUDIO_UNIT_P", "N_CLK_DOMAIN_P", "N_CONTROL_P", "N_CLK_DOM_P"}
MODS = ("KL_aecp_dyn_state", "KL_aecp_engine", "protocol_processor_top", "KL_pp_shadow")
def const_of(node):
    stack = [node]
    while stack:
        n = stack.pop()
        if isinstance(n, dict):
            if n.get("type") == "CONST":
                return n.get("name")
            stack.extend(v for v in n.values() if isinstance(v, (dict, list)))
        elif isinstance(n, list):
            stack.extend(n)
    return None
def walk_mod(mod):
    found = {}
    stack = [mod.get("stmtsp", [])]
    while stack:
        n = stack.pop()
        if isinstance(n, list):
            stack.extend(n); continue
        if not isinstance(n, dict):
            continue
        if n.get("type") == "VAR" and n.get("name") in WANT and n.get("varType") in ("GPARAM", "LPARAM"):
            found[n["name"]] = const_of(n.get("valuep"))
        if n.get("type") != "MODULE":
            stack.extend(v for k, v in n.items() if isinstance(v, (dict, list)))
    return found
rows = []
for m in tree.get("modulesp", []):
    name = m.get("name", "")
    orig = m.get("origName", name)
    if any(orig == x or name.startswith(x) for x in MODS):
        rows.append((orig, name, walk_mod(m)))
for orig, name, vals in sorted(rows):
    print(f"{orig:24s} {name:60s} {vals}")
