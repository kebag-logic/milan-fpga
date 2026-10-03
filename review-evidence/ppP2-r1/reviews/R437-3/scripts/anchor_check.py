#!/usr/bin/env python3
"""Report, for each probe of a spec, whether every edit's anchor occurs exactly once at the head."""
import subprocess, sys
repo, spec = sys.argv[1], sys.argv[2]
HEAD = "527662d659b4ead97675744d12a43af1ea92b9b3"
F = {"RTL": "hdl/packet_engine/KL_pp_nvm_port.sv", "SIM": "tb/nvm_port/sim_main.cpp", "FUZZ": "tb/nvm_port/fuzz_main.cpp"}
src = {k: subprocess.run(["git", "-C", repo, "show", f"{HEAD}:{v}"], capture_output=True, text=True, check=True).stdout for k, v in F.items()}
ns = {}; exec(open(spec).read(), ns)
for name, edits in ns["PROBES"].items():
    counts = []
    for tag, old, new in edits:
        counts.append(src[tag].count(old))
        src_t = src[tag]
    print(f"{name}: {counts} {'OK' if all(c == 1 for c in counts) else 'ANCHOR MISSING'}")
