#!/usr/bin/env bash
# Enumerate protocol_processor_top's overridable (GPARAM) parameters with the
# elaborator itself, independently of scripts/check-integrator-params.py.
# Usage: elab-params.sh <clone-dir> <scratch-dir> <verilator>
set -euo pipefail
cd "$1"; s="$2"; v="$3"; mkdir -p "$s"
"$v" --version
pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
# shellcheck disable=SC2086
"$v" --json-only -Wno-fatal -Wno-lint -Wno-style --top-module protocol_processor_top \
    --Mdir "$s/obj" $pkgs $all >"$s/json.log" 2>&1 || { tail "$s/json.log"; exit 1; }
python3 - "$s/obj" <<'PY'
import json, sys, glob
tree = json.load(open(glob.glob(sys.argv[1] + "/*.tree.json")[0]))
def walk(n, mod=None):
    if isinstance(n, dict):
        if n.get("type") == "MODULE": mod = n.get("origName") or n.get("name")
        if n.get("type") == "VAR" and mod == "protocol_processor_top" and n.get("varType") == "GPARAM":
            yield n.get("origName") or n.get("name")
        for v in n.values(): yield from walk(v, mod)
    elif isinstance(n, list):
        for v in n: yield from walk(v, mod)
names = list(dict.fromkeys(walk(tree)))
print(len(names)); print("\n".join(names))
PY
