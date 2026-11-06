#!/usr/bin/env bash
# Concurrent spot-checks in an exported tree: srp_top, srp_stream_fsms (suite+walk),
# pp_top suites, HDL lint, and area at 2x2/8x8. usage: run_spot.sh <tree> <receipts>
set -u
T=$1; R=$2; H=$(cd "$(dirname "$0")" && pwd)
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR=${TMPDIR:-$T/../tmp}
mkdir -p "$R"
job() { n=$1; shift; ( "$@" ) > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc"; }
job srp_top make -C "$T/tb/srp_top" -j4 &
job srp_stream_fsms make -C "$T/tb/srp_stream_fsms" -j4 &
job pp_top make -C "$T/tb/pp_top" -j6 &
job lint bash -c "cd '$T' && bash scripts/lint_hdl.sh" &
job area bash "$H/area_some.sh" "$T" "$R/area" srp_top_2x2 srp_top_8x8 &
wait
for f in "$R"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
