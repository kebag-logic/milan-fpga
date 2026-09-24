#!/bin/sh
# Elaborate KL_crf_rx at two revisions and print RATE_DRIFT_NS_C / TS_JUMP_NS_C.
# usage: elab_params.sh <repo> <verilator> <workdir> <rev>...
set -e
repo=$1; V=$2; w=$3; shift 3
mkdir -p "$w"
for rev in "$@"; do
  git -C "$repo" show "$rev:hdl/ieee1722/crf/KL_crf_rx.sv" > "$w/rx_$rev.sv"
  "$V" --json-only --json-only-output "$w/rx_$rev.json" -Wno-fatal -Wno-lint -Wno-style \
       --top-module KL_crf_rx "$w/rx_$rev.sv" >/dev/null 2>&1
  python3 - "$w/rx_$rev.json" "$rev" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); out = {}
def consts(m, acc):
    if isinstance(m, dict):
        if m.get("type") == "CONST": acc.append(m.get("name"))
        for v in m.values(): consts(v, acc)
    elif isinstance(m, list):
        for v in m: consts(v, acc)
def walk(n):
    if isinstance(n, dict):
        if n.get("type") == "VAR" and n.get("name") in ("TS_JUMP_NS_C", "RATE_DRIFT_NS_C"):
            acc = []; consts(n.get("valuep"), acc)
            out[n["name"]] = [int(c.split("h")[1], 16) for c in acc]
        for v in n.values(): walk(v)
    elif isinstance(n, list):
        for v in n: walk(v)
walk(d); print(sys.argv[2], out)
PY
done
