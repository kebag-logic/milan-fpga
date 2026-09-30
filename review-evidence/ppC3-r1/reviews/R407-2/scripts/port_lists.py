#!/usr/bin/env python3
"""Compare comment-stripped module headers (parameters + ports) of named modules
between two commits of the processor clone. Read-only (git show)."""
import re, subprocess, sys
CLONE = sys.argv[1]; A, B = sys.argv[2], sys.argv[3]
MODS = {"protocol_processor_top": "hdl/top/protocol_processor_top.sv",
        "KL_aecp_engine": "hdl/aecp/KL_aecp_engine.sv",
        "KL_aecp_dyn_state": "hdl/aecp/KL_aecp_dyn_state.sv",
        "KL_acmp_nvm_shadow": "hdl/acmp/KL_acmp_nvm_shadow.sv",
        "KL_pp_nvm_port": "hdl/packet_engine/KL_pp_nvm_port.sv",
        "KL_pp_nvm_mgr_arb": "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv",
        "KL_aecp_nvm_writer": "hdl/aecp/KL_aecp_nvm_writer.sv",
        "KL_adp_engine": "hdl/adp/KL_adp_engine.sv"}
def header(rev, path, mod):
    s = subprocess.run(["git", "-C", CLONE, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S); s = re.sub(r"//[^\n]*", " ", s)
    m = re.search(r"\bmodule\s+" + mod + r"\b(.*?\));", s, flags=re.S)
    return re.findall(r"\S+", m.group(1)) if m else None
rc = 0
for mod, path in MODS.items():
    a, b = header(A, path, mod), header(B, path, mod)
    if a == b: print(f"{mod}: identical ({len(a)} tokens)")
    else:
        rc = 1
        import difflib
        print(f"{mod}: DIFFERS"); print("  " + "\n  ".join(l for l in difflib.unified_diff(a, b, lineterm="", n=2) if l[:1] in "+-" and l[:3] not in ("+++", "---")))
sys.exit(rc)
