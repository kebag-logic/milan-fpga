#!/usr/bin/env bash
# Focused donor/consumer suites, lint, docs gates and the #134 new-arm mutation
# campaign at the exact head, each detached with its own log and rc file.
# Usage: run_campaigns.sh <packet_dir>
set -u
P=$1; S=$P/scratch; R=$P/receipts/suites; mkdir -p "$R"
export PATH=$S/bin:$PATH VERILATOR=$S/bin/verilator
E=$S/exp-head
launch() { # name dir cmd...
  local n=$1 d=$2; shift 2
  ( cd "$d" && "$@" ) > "$R/$n.log" 2>&1 && echo 0 > "$R/$n.rc" || echo $? > "$R/$n.rc" &
}
verilator --version > "$R/verilator-identity.txt"; command -v verilator >> "$R/verilator-identity.txt"
for t in originator rx_validator srp_stream_fsms srp_top maap ca_originator; do
  launch "suite-$t" "$E/tb/$t" make
done
launch suite-pp_top "$E/tb/pp_top" make -j4
launch lint_hdl "$E" ./scripts/lint_hdl.sh
launch make-check "$S/clone-head" make check
launch mut134 "$S/clone-head" python3 tb/srp_top/mutants.py --output "$S/mut134" \
  --only lv-second-lv-ends,lv-never-ends,lv-expiry-masked,lv-expiry-last,lv-expiry-dropped,lv-sweep-misses-collision \
  --jobs 4
wait
