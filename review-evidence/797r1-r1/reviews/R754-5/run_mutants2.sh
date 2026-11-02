#!/bin/sh
# Two further srp_fresh_r clear mutants at head ef7dc985, swept with the head page.
# m4: the clear on a provisioning STRMW_CTRL write removed (milan_csr.sv:3128).
# m5: the clear on a STRM_SEL write removed (milan_csr.sv:3119).
# Usage: run_mutants2.sh <packet-dir>   (want rc 1 each)
set -u
P=$1; S=$P/scratch; R=$P/receipts
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
for m in m4 m5; do
  ( python3 -I "$S/$m/scripts/register_read_sweep.py" --work "$S/w/$m" > "$R/sweep_$m.log" 2>&1; echo $? > "$R/sweep_$m.rc" ) &
done
wait
for m in m4 m5; do echo "sweep_$m rc=$(cat "$R/sweep_$m.rc")"; tail -1 "$R/sweep_$m.log"; done
