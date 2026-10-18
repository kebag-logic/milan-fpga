#!/bin/bash
# Reviewer probe mutants: for each patch in scripts/mutations, copy the exact-head
# tree to a scratch dir of its own, apply it, then run tb/srp_encoder, tb/srp_top
# group domjoin and the reviewer's KL_srp_domain bench, and record every FAIL line.
# usage: probe_campaign.sh <exact-head-tree> <scratch-dir> <receipt-dir>
set -u
SRC=$1; SCR=$2; OUT=$3; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$SCR" "$OUT"
one() {
  m=$1; t="$SCR/$m"; rm -rf "$t"; mkdir -p "$t"
  cp -a "$SRC/hdl" "$t/hdl"; mkdir -p "$t/tb"
  for n in common srp_top srp_encoder; do
    rsync -a --exclude 'obj_*' "$SRC/tb/$n/" "$t/tb/$n/"; done
  ( cd "$t" && git init -q && git apply "$HERE/mutations/$m.patch" ) || { echo "$m APPLY-FAIL"; return; }
  ( cd "$t/tb/srp_encoder" && make ) > "$OUT/$m.srp_encoder.log" 2>&1; e=$?
  ( cd "$t/tb/srp_top" && make run RUN_ARGS=domjoin ) > "$OUT/$m.srp_top-domjoin.log" 2>&1; j=$?
  "$HERE/domprobe/run.sh" "$t" "$t/domprobe" > "$OUT/$m.domprobe.log" 2>&1; b=$?
  {
    echo "$m: srp_encoder rc=$e $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$OUT/$m.srp_encoder.log" | tail -1)"
    grep -E '^FAIL' "$OUT/$m.srp_encoder.log" | sed 's/^/    /'
    echo "$m: srp_top domjoin rc=$j $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$OUT/$m.srp_top-domjoin.log" | tail -1)"
    grep -E '^FAIL' "$OUT/$m.srp_top-domjoin.log" | sed 's/^/    /'
    echo "$m: reviewer bench rc=$b $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$OUT/$m.domprobe.log" | tail -1)"
    grep -E '^FAIL' "$OUT/$m.domprobe.log" | sed 's/^/    /'
  } > "$OUT/$m.summary"
}
for p in "$HERE"/mutations/*.patch; do m=$(basename "$p" .patch); one "$m" & done
wait
cat "$OUT"/*.summary
