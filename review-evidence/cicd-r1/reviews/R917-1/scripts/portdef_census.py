#!/usr/bin/env python3
"""Census of input ports with a default value (the #996 hazard) in a Verilator model.

usage: portdef_census.py OUTDIR NAME -- <verilator args: --top-module X sources/-G...>
Runs the pinned Verilator with --json-only (no C++), walks the elaborated tree and
prints every INPUT variable that carries a user initialiser (hasUserInit or a
non-empty valuep). Exit 0 = none found, 3 = found, 2 = tool error.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

VERILATOR = os.environ.get("PINNED_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")


def walk(node, module, hits, ports):
    if isinstance(node, dict):
        if node.get("type") == "MODULE":
            module = node.get("name")
        if node.get("type") == "VAR" and node.get("direction") in ("INPUT", "INOUT"):
            ports.append((module, node.get("name")))
            if node.get("hasUserInit") or node.get("valuep"):
                hits.append((module, node.get("name")))
        for value in node.values():
            walk(value, module, hits, ports)
    elif isinstance(node, list):
        for value in node:
            walk(value, module, hits, ports)


def main() -> int:
    out, name = Path(sys.argv[1]), sys.argv[2]
    args = sys.argv[sys.argv.index("--") + 1:]
    mdir = out / f"json_{name}"
    mdir.mkdir(parents=True, exist_ok=True)
    run = subprocess.run([VERILATOR, "--json-only", "-Wno-fatal", "-Wno-lint", "-Wno-style",
                          "-Mdir", str(mdir), *args], capture_output=True, text=True)
    trees = list(mdir.glob("*.tree.json"))
    if run.returncode or not trees:
        print(f"{name}: verilator rc={run.returncode}\n{run.stderr[-2000:]}")
        return 2
    hits, ports = [], []
    walk(json.loads(trees[0].read_text()), None, hits, ports)
    modules = sorted({m for m, _ in ports})
    print(f"{name}: {len(ports)} input ports in {len(modules)} modules {modules}; defaulted: {hits or 'none'}")
    return 3 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
