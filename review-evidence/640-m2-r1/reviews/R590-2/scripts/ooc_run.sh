#!/usr/bin/env bash
# R590-2: serial OOC syntheses of the emitted benches, all under the host
# Vivado lock, one Vivado at a time. Usage: ooc_run.sh VIVADO EMITDIR OUTDIR WORKDIR LOCK
set -u
VIVADO="$1"; EMIT="$2"; OUT="$3"; WORK="$4"; LOCK="$5"
TCL="$(cd "$(dirname "$0")" && pwd)/ooc_bench.tcl"
mkdir -p "$OUT" "$WORK"
cd "$WORK" || exit 2
date -u +%FT%TZ >"$OUT/lock_wait_start.txt"
exec 9>"$LOCK"
flock 9
date -u +%FT%TZ >"$OUT/lock_acquired.txt"
for tag in head-litex-csr_aw head-migen-csr_aw reverted-migen-csr_aw head-litex-mac_tx head-migen-mac_tx; do
  "$VIVADO" -mode batch -nojournal -log "$OUT/$tag.vivado.log" -source "$TCL" \
    -tclargs "$EMIT/$tag.v" "$OUT" "$tag" >/dev/null 2>&1
  echo $? >"$OUT/$tag.rc"
done
date -u +%FT%TZ >"$OUT/done.txt"
