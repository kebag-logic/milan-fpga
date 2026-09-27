#!/usr/bin/env python3
"""Compare a reviewer 8x8 export against the committed 50 MHz input manifest.

Usage: compare_inputs.py REPO WORK CPU_PACKAGE_ROOT
Hashes every recorded image and source input under the reviewer's own roots,
normalizes build-root strings in the generated Tcl, and prints one line per
mismatch plus a summary. Exit 1 on any mismatch.
"""
import hashlib, json, sys
from pathlib import Path

repo, work, cpu = (Path(a) for a in sys.argv[1:4])
man = json.loads((repo / "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json").read_text())
roots = {"repository": repo, "protocol_processor": repo / "protocol-processor",
         "gptp_processor": repo / "gptp-processor", "axis_library": repo / "third_party/verilog-axis",
         "cpu_package": cpu}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def resolve(rec):
    if rec["root"] == "work":
        # manifest work paths start with the variant directory (default/ or attribution/)
        rel = Path(*Path(rec["path"]).parts[1:])
        return work / rel
    return roots[rec["root"]] / rec["path"]

bad = checked = skipped = 0
m = man["measurements"]["default"]
for group in ("images", "source_inputs"):
    for rec in m[group]:
        p = resolve(rec)
        if not p.exists():
            print(f"MISSING {group} {rec['root']}:{rec['path']}"); bad += 1; continue
        h = sha(p)
        checked += 1
        if h != rec["sha256"] or p.stat().st_size != rec["bytes"]:
            print(f"DIFF {group} {rec['root']}:{rec['path']} manifest={rec['sha256'][:16]}/{rec['bytes']} reviewer={h[:16]}/{p.stat().st_size}")
            bad += 1
print(f"checked={checked} mismatched_or_missing={bad}")
sys.exit(1 if bad else 0)
