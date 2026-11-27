#!/bin/bash
# Reviewer reproduction recipe for R961-1 (PR #1024 at 75db86a9).
# Usage: run_review_campaigns.sh <clone-at-head> <verilator-5.050> <out-dir> <packet-scripts-dir>
# Every build writes under <out-dir>; nothing is written into the clone.
set -u
repo=$1; engine=$2; out=$3; probes=$4
tb=$repo/tb/verilator/usbaudio
mkdir -p "$out"
cd "$tb" || exit 2
# Independent campaigns run concurrently, each with its own log and status file.
( python3 -B check.py --engine "$engine" --out "$out/default" --jobs 4 > "$out/default.log" 2>&1; echo $? > "$out/default.rc" ) &
( python3 -B transport_mutations.py --engine "$engine" --out "$out/transport" --jobs 4 \
    --cleanup-ledger "$out/transport-ledger.log" --temporary-suffix __ALL.verilator_deplist.tmp \
    --discard-builds > "$out/transport.log" 2>&1; echo $? > "$out/transport.rc" ) &
( python3 -B mutations.py --engine "$engine" --out "$out/protocol" --jobs 2 > "$out/protocol.log" 2>&1
  echo $? > "$out/protocol.rc" ) &
( make -C "$tb" duplex-build MDIR="$out/duplex13" RTL_SIMULATOR="$engine" JOBS=4 WINDOW_LOG2=13 \
    > "$out/duplex13-build.log" 2>&1 && "$out/duplex13/VKL_usbaudio_bridge" 1000000 > "$out/duplex13.log" 2>&1
  echo $? > "$out/duplex13.rc" ) &
# Bridge-level epoch-fence and acknowledgement plants (finding F2).
x=$probes/probe_bridge_mutants.sh
( "$x" "$repo" "$engine" "$out/bridge" baseline x x ) > "$out/bridge-baseline.result" 2>&1 &
( "$x" "$repo" "$engine" "$out/bridge" no_published_gate ' && published_epoch_r == bus_capture_epoch_r' '' ) \
  > "$out/bridge-no_published_gate.result" 2>&1 &
( "$x" "$repo" "$engine" "$out/bridge" no_applied_gate '&& applied_epoch_r == bus_capture_epoch_r && published' '&& published' ) \
  > "$out/bridge-no_applied_gate.result" 2>&1 &
( "$x" "$repo" "$engine" "$out/bridge" no_capture_abort \
    'assign capture_abort_o = apply_w && capture_epoch_w != bus_capture_epoch_r;' "assign capture_abort_o = 1'b0;" ) \
  > "$out/bridge-no_capture_abort.result" 2>&1 &
( "$x" "$repo" "$engine" "$out/bridge" status_unapplied_epoch '.capture_epoch_i(applied_epoch_r)' '.capture_epoch_i(bus_capture_epoch_r)' ) \
  > "$out/bridge-status_unapplied_epoch.result" 2>&1 &
# Media grid coincidence probe (finding F3).
( "$engine" --binary --timing --top-module probe_media_grid_tb -Wno-fatal -Wno-lint -Wno-style \
    --Mdir "$out/probe_media" "$repo/hdl/milan/usbaudio/KL_usbaudio_media.sv" "$probes/probe_media_grid_tb.sv" \
    > "$out/probe_media-build.log" 2>&1 && "$out/probe_media/Vprobe_media_grid_tb" > "$out/probe_media.log" 2>&1 ) &
wait
# Repository gates named in finding F1 (run from the clone; read-only).
cd "$repo" || exit 2
python3 -B scripts/check_solution_docs.py > "$out/solution_docs.log" 2>&1; echo "rc=$?" >> "$out/solution_docs.log"
python3 -B scripts/docs_inventory.py --check > "$out/docs_inventory.log" 2>&1; echo "rc=$?" >> "$out/docs_inventory.log"
( cd sw/builder && python3 -B -c 'import test_clock_contract as t; t.test_tap_clock_docs()' ) \
  > "$out/tap_clock_docs.log" 2>&1; echo "rc=$?" >> "$out/tap_clock_docs.log"
# Afterwards confirm the clone is still exact: git status --porcelain --ignored must be empty.
