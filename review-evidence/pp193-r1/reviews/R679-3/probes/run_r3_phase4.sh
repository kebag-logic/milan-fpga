#!/bin/sh
# Round-3 reviewer spot-check, phase 4: the suites the manager merge of
# processor main touched, at the merged head (the author's gates predate it).
# usage: run_r3_phase4.sh <clone> <head> <outdir>
# Needs Verilator 5.050 as `verilator` on PATH.
#   pp_top     tb/pp_top `make` (the seven builds, one canonical tally)
#   aecp_cmds  tb/aecp_cmds `make run` (the decode sweep against decode.json)
set -u
clone=$1; head=$2; out=$3
mkdir -p "$out"
rm -rf "$out/tree"; mkdir -p "$out/tree"; git -C "$clone" archive "$head" | tar -x -C "$out/tree"
( cd "$out/tree/tb/aecp_cmds" && timeout 1800 make run > "$out/aecp_cmds.log" 2>&1; echo $? > "$out/aecp_cmds.rc" ) &
( cd "$out/tree/tb/pp_top" && timeout 3000 make > "$out/pp_top.log" 2>&1; echo $? > "$out/pp_top.rc" ) &
wait
for n in aecp_cmds pp_top; do printf '%-10s rc=%s  %s\n' "$n" "$(cat "$out/$n.rc")" "$(tail -1 "$out/$n.log")"; done
