#!/bin/sh
# Execute selected production CI pieces at the reviewed head, concurrently, one
# disposable checkout copy each. Usage: run_exact_head_legs.sh <scratch> <python> <receipts>
#   pieces: milan_dp_render__1 (probe-render), pp_shadow__0 (probe-pp), maap__0 (probe-maap)
set -u
s=$1; py=$2; out=$3; mkdir -p "$out"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export VERILATOR_JOBS=5 CI_BUILD_JOBS=5 CI_CAMPAIGN_JOBS=4 SIM_JOBS=4 MAKEFLAGS="-j1 --no-print-directory"
go() { dir=$1; piece=$2; ( cd "$s/$dir" && start=$(date +%s); "$py" scripts/ci_suite_pieces.py run "$piece" --receipts "$out/$piece" >"$out/$piece.log" 2>&1; echo $? >"$out/$piece.rc"; echo $(( $(date +%s) - start )) >"$out/$piece.seconds" ) & }
go probe-render milan_dp_render__1
go probe-pp pp_shadow__0
go probe-maap maap__0
wait
for f in "$out"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") s=$(cat "${f%.rc}.seconds")"; done
