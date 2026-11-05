#!/usr/bin/env python3
"""Write the native-shards spec for the full sweep at <head>, the environment of the
discovery sweep: pinned Verilator 5.050, sv2v 0.0.12, Make 4.3, MAKEFLAGS with
--no-print-directory. Usage: sweep_spec.py <head> <spec.json> <tmpdir>"""
import json
import sys
from pathlib import Path

head, spec, tmp = sys.argv[1:4]
Path(tmp).mkdir(parents=True, exist_ok=True)
Path(spec).write_text(json.dumps({
    "cwd": "$LANES/840-identity-link",
    "head": head,
    "base": "604899c08ff1cd1830e1dd08b733109ef852400c",
    "commands": [[
        "env",
        "PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:"
        "$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
        "VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator",
        "TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c",
        f"TMPDIR={tmp}",
        "MAKEFLAGS=-j4 --no-print-directory",
        "bash", "scripts/run_all_suites.sh", "$VALIDATION_STORAGE/840-a732/unused/logs", "--wait",
    ]],
}, indent=1) + "\n")
print(spec)
