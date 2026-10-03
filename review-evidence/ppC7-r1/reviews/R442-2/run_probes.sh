#!/bin/sh
# Run the two reviewer probes (each a patched copy of hdl/, tb/common/, tb/pp_top/)
# on the cycle-bounded `counters` target. Usage: run_probes.sh <scratch-dir> <receipts-dir>
S=$1; R=$2
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
for p in probe1 probe2; do
  ( make -C "$S/$p/tb/pp_top" counters > "$R/$p.log" 2>&1; echo "rc=$?" > "$R/$p.rc" ) &
done
wait
